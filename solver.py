import random
import math
import time

import validator
from roster_parser import ParseRoster

class SolutionInstance:
	'''
	schedule = {staffId: list(shiftId)}
	'''
	def __init__(self):
		self.horizon = 0
		self.score = 0
		self.isValid = False
		self.schedule = dict()

	def ShallowCopy(self):
		result = SolutionInstance()
		result.horizon = self.horizon
		result.score = self.score
		result.schedule = {x: y for x, y in self.schedule.items()}
		return result

	def PrintDebug(self):
		for staff, schedule in self.schedule.items():
			print('solution.schedule[\'{}\'] ='.format(staff), schedule)

	def Show(self):
		for schedule in self.schedule.values():
			print('\t'.join(schedule).replace(' ', ''))

def CreateEmptySolution(problem):
	result = SolutionInstance()
	result.horizon = problem.horizon

	for staffId in problem.staff.keys():
		result.schedule[staffId] = [' '] * horizon

	return result

instance1_optimal_solution = SolutionInstance()
instance1_optimal_solution.horizon = 14
instance1_optimal_solution.score = 607
instance1_optimal_solution.schedule['A'] = [' ', 'D', 'D', 'D', 'D', ' ', ' ', 'D', 'D', ' ', ' ', 'D', 'D', 'D']
instance1_optimal_solution.schedule['B'] = ['D', 'D', 'D', 'D', 'D', ' ', ' ', 'D', 'D', ' ', ' ', 'D', 'D', ' ']
instance1_optimal_solution.schedule['C'] = ['D', 'D', 'D', ' ', ' ', 'D', 'D', ' ', ' ', 'D', 'D', ' ', ' ', ' ']
instance1_optimal_solution.schedule['D'] = ['D', 'D', ' ', ' ', ' ', 'D', 'D', 'D', 'D', 'D', ' ', ' ', ' ', ' ']
instance1_optimal_solution.schedule['E'] = [' ', 'D', 'D', 'D', 'D', ' ', ' ', 'D', 'D', ' ', ' ', 'D', 'D', 'D']
instance1_optimal_solution.schedule['F'] = ['D', 'D', 'D', ' ', ' ', ' ', ' ', 'D', 'D', 'D', ' ', ' ', 'D', 'D']
instance1_optimal_solution.schedule['G'] = [' ', ' ', 'D', 'D', 'D', ' ', ' ', 'D', 'D', ' ', ' ', 'D', 'D', 'D']
instance1_optimal_solution.schedule['H'] = ['D', 'D', ' ', ' ', 'D', 'D', ' ', ' ', 'D', 'D', 'D', 'D', ' ', ' ']

instance1_solution = SolutionInstance()
instance1_solution.horizon = 14
instance1_solution.score = 708
instance1_solution.schedule['A'] = [' ', 'D', 'D', 'D', 'D', ' ', ' ', 'D', 'D', ' ', ' ', 'D', 'D', 'D']
instance1_solution.schedule['B'] = ['D', 'D', 'D', 'D', 'D', ' ', ' ', 'D', 'D', ' ', ' ', 'D', 'D', ' ']
instance1_solution.schedule['C'] = ['D', 'D', 'D', ' ', ' ', 'D', 'D', ' ', ' ', 'D', 'D', 'D', ' ', ' ']
instance1_solution.schedule['D'] = ['D', 'D', ' ', ' ', ' ', 'D', 'D', 'D', 'D', 'D', ' ', ' ', ' ', ' ']
instance1_solution.schedule['E'] = [' ', 'D', 'D', 'D', 'D', ' ', ' ', 'D', 'D', ' ', ' ', 'D', 'D', 'D']
instance1_solution.schedule['F'] = ['D', 'D', 'D', 'D', 'D', ' ', ' ', 'D', 'D', ' ', ' ', ' ', 'D', 'D']
instance1_solution.schedule['G'] = [' ', ' ', 'D', 'D', 'D', ' ', ' ', 'D', 'D', ' ', ' ', 'D', 'D', 'D']
instance1_solution.schedule['H'] = ['D', 'D', ' ', ' ', ' ', ' ', ' ', ' ', 'D', 'D', 'D', 'D', 'D', ' ']

'''
Simulated Annealing has 4 major parts:
	1. A valid start configuration
	2. A random rearrangement scheme
	3. An objective function
	4. An annealing schedule
'''

#print (list(exact_solution.schedule.keys()))
#print (random.choice(list(exact_solution.schedule.keys())))

def NeighbourMove_TotalReorder(solution):
	staffId = random.choice(list(solution.schedule.keys()))
	schedule = solution.schedule[staffId]
	startIndex = [0]

	prevShift = schedule[0]
	currShift = ''

	# Find all bounds between different shifts
	for idx in range(1, solution.horizon):
		currShift = schedule[idx]
		if currShift != prevShift:
			startIndex.append(idx)
		prevShift = currShift

	reorderIndex = random.choice(startIndex)
	solution.schedule[staffId] = schedule[reorderIndex:] + schedule[:reorderIndex]

def NeighbourMove_PartialReorder(solution):
	staffId = random.choice(list(solution.schedule.keys()))
	schedule = solution.schedule[staffId]
	startIndex = [0]

	prevShift = schedule[0]
	currShift = ''

	# Find all bounds between different shifts
	for idx in range(1, solution.horizon):
		currShift = schedule[idx]
		if currShift != prevShift:
			startIndex.append(idx)
		prevShift = currShift

	seq1, seq2 = 0, 0
	while seq1 == seq2:
		seq1 = random.randint(0, len(startIndex) - 1)
		seq2 = random.randint(0, len(startIndex) - 1)

	if seq1 > seq2:
		seq1, seq2 = seq2, seq1

	startIndex.append(solution.horizon)

	start1 = startIndex[seq1]
	end1 = startIndex[seq1 + 1]
	start2 = startIndex[seq2]
	end2 = startIndex[seq2 + 1]

	# [0, 1, 5, 7, 9, 11]
	# 4 1 => [1, 5), [9, 11)
	#
	# solution.schedule['A'] = [' ', <'D', 'D', 'D', 'D'>, ' ', ' ', 'D', 'D', <' ', ' '>, 'D', 'D', 'D']
	# solution.result  ['A'] = [' ', <' ', ' '>, ' ', ' ', 'D', 'D', <'D', 'D', 'D', 'D'>, 'D', 'D', 'D']

	solution.schedule[staffId] = \
		schedule[:start1] + \
		schedule[start2:end2] + \
		schedule[end1:start2] + \
		schedule[start1:end1] + \
		schedule[end2:]

def NeighbourMove_SegmentShift(solution, annealCoeff = 0.25):
	staffId = random.choice(list(solution.schedule.keys()))
	schedule = solution.schedule[staffId]

	segmentLength = max(int(len(schedule) * annealCoeff), 1)
	segmentStart = random.randint(0, len(schedule) - segmentLength)

	shiftDist = 0
	while shiftDist == 0:
		shiftDist = random.randint(-segmentStart, len(schedule) - segmentStart + segmentLength)

	if shiftDist < 0:
		solution.schedule[staffId] = \
			schedule[: segmentStart + shiftDist] + \
			schedule[segmentStart : segmentStart + segmentLength] + \
			schedule[segmentStart + shiftDist : segmentStart] + \
			schedule[segmentStart + segmentLength:]
	else:
		solution.schedule[staffId] = \
			schedule[: segmentStart] + \
			schedule[segmentStart + segmentLength : segmentStart + segmentLength + shiftDist] + \
			schedule[segmentStart : segmentStart + segmentLength] + \
			schedule[segmentStart + segmentLength + shiftDist :]

# Moves with their relative weight
neighbourMoves = [
	[NeighbourMove_TotalReorder, 2],
	[NeighbourMove_PartialReorder, 5],
	[NeighbourMove_SegmentShift, 7]
]

def MakeAccum(moves):
	totalWeight = sum([x[1] for x in neighbourMoves])
	accum = 0.0
	for idx, x in enumerate(neighbourMoves):
		accum += x[1] / totalWeight
		moves[idx][1] = accum
	moves[-1][1] = 1.0

def ChooseMove(moves):
	p = random.random()
	idx = 0
	while moves[idx][1] < p:
		idx += 1
	return moves[idx][0]

def Anneal(problem, maxTime = float('inf'), instances = 1):
	'''
	Try to solve the given problem while not exceeding 'maxTime'.
	'instances' is the number of tries to solve the problem. Each try should start from
	a different random configuration.
	'''
	# Solution variables
	timePerInstance = maxTime / instances
	bestSolution = instance1_solution
	#bestSolution.score = validator.CalculatePenalty(bestSolution, problem)

	# Annealing variables
	mu = -math.exp(1.0) / float(bestSolution.score)

	MakeAccum(neighbourMoves)
	
	for _ in range(instances):
		# solution = GenerateRandomSolution(problem)
		solution = instance1_solution
		endTime = time.time() + timePerInstance

		while True:
			if (time.time() > endTime):
				break

			newSolution = solution.ShallowCopy()
			ChooseMove(neighbourMoves)(newSolution)

			newSolution.score = validator.CalculatePenalty(newSolution, problem)
			newSolution.isValid = validator.ValidateSolution(newSolution, problem)

			if newSolution.isValid:
				return newSolution
			else:
				continue

			if newSolution.score < bestSolution.score or \
				random.random() < math.exp(mu * (newSolution.score - solution.score)):
				solution = newSolution
				if bestSolution.score > solution.score:
					bestSolution = solution

	return bestSolution

def calcAvrMinutes(problem):
    return sum([x.length for k, x in problem.shifts.items()])/len(problem.shifts.items())
    
def calcDaysOff(problem, staff):
    avrMin = calcAvrMinutes(problem)
    maxMinStaff = max([x.maxTotalMinutes for k, x in problem.staff.items()])
    maxDaysOff = (problem.horizon * avrMin - maxMinStaff) / avrMin
    return maxDaysOff - len(problem.staff[staff].daysOff)

import random

def GenerateInitialConfiguration(problem):
    result = CreateEmptySolution(problem)
    for key in result.schedule.keys():
        currentMinutes = 0
        staffMaxShifts = problem.staff[key].maxShifts
        impossible_shifts = [shift for shift, count in staffMaxShifts if count == 0]
        avaliable_shifts = (set(problem.shifts.keys()) - set(impossible_shifts)).union(set([' ']))
        last_shift = ' '
        weekends = 0
        consecutiveOn = 0
        daysOff = 0
        maxDays = calcDaysOff(problem, key)
        for day in range(problem.horizon):
            if not day in problem.staff[key].daysOff:
                if last_shift in problem.shifts:
                    prohibitShifts = avaliable_shifts.intersection(problem.shifts[last_shift].prohibitNext)
                else:
                    prohibitShifts = set()
                
                avaliable_shifts -= prohibitShifts
                
                if  consecutiveOn == problem.staff[key].maxConsecutiveShifts or \
                    ((day > 2 and ((day + 1) % 7 == 0 or (day + 2) % 7 == 0) \
                    and weekends == problem.staff[key].maxWeekends)):
                    curr_shift = ' '
                else:
                    curr_shift = random.choice(list(avaliable_shifts))
                
                if curr_shift == ' ':
                    consecutiveOn = 0
                else:
                    consecutiveOn += 1
    
                if(curr_shift != ' '):
                    currentMinutes += problem.shifts[curr_shift].length
                if currentMinutes > problem.staff[key].maxTotalMinutes :
                    break
                
                if curr_shift == ' ':
                    daysOff += 1
                    
                if daysOff < maxDays:
                    avaliable_shifts -= set([' '])
                
                result.schedule[key][day] = curr_shift;

                if (day > 2 and (day + 1) % 7 == 0) and \
                   (result.schedule[key][day] != ' ' or  result.schedule[key][day - 1] != ' '):
                        weekends += 1
                
                avaliable_shifts.union(prohibitShifts)
                last_shift = curr_shift
                if curr_shift in staffMaxShifts:
                    if staffMaxShifts[curr_shift] == 1:
                        avaliable_shifts -= set([curr_shift])
                    else:
                        staffMaxShifts[curr_shift] -= 1
    result.score = calculatePenalty(result, problem)
    return result
