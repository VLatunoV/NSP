import random
import math
import time
import copy

import validator
from roster_parser import ParseRoster

class SolutionInstance:
	'''
	schedule = {staffId: list(shiftId)}
	'''
	def __init__(self):
		self.horizon = 0
		self.score = 0
		self.hardViolations = 0
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
		result.schedule[staffId] = [' '] * problem.horizon

	return result

'''
Simulated Annealing has 4 major parts:
	1. A valid start configuration
	2. A random rearrangement scheme
	3. An objective function
	4. An annealing schedule
'''

def calcAvrMinutes(problem):
    return sum([x.length for k, x in problem.shifts.items()])/len(problem.shifts.items())
    
def calcDaysOff(problem, staff):
    avrMin = calcAvrMinutes(problem)
    maxMinStaff = max([x.maxTotalMinutes for k, x in problem.staff.items()])
    maxDaysOff = (problem.horizon * avrMin - maxMinStaff) / avrMin
    return maxDaysOff - len(problem.staff[staff].daysOff)

def GenerateInitialConfiguration(problem):
    result = CreateEmptySolution(problem)
    for key in result.schedule.keys():
        currentMinutes = 0
        staffMaxShifts = problem.staff[key].maxShifts
        impossible_shifts = [shift for shift, count in staffMaxShifts.items() if count == 0]
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
                
                if consecutiveOn == problem.staff[key].maxConsecutiveShifts or \
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

    validator.CalculatePenalty(result, problem)
    return result

def NeighbourMove_TotalReorder(solution, **kw):
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

def NeighbourMove_PartialReorder(solution, **kw):
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

	# Edge case: whole schedule is only one shift
	if len(startIndex) == 1:
		return

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

def NeighbourMove_SegmentShift(solution, annealCoeff = 0.25, **kw):
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

def NeighbourMove_SwitchShift(solution, **kw):
	staffId = random.choice(list(solution.schedule.keys()))
	newShift = random.choice(kw['shiftTypes'])
	day = random.randint(0, solution.horizon - 1)
	solution.schedule[staffId][day] = newShift

def NeighbourMove_SwapShifts(solution, **kw):
	staffId = random.choice(list(solution.schedule.keys()))
	day1, day2 = 0, 0
	while day1 == day2:
		day1 = random.randint(0, solution.horizon - 1)
		day2 = random.randint(0, solution.horizon - 1)
	schedule = solution.schedule[staffId]
	schedule[day1], schedule[day2] = schedule[day2], schedule[day1]

# Moves with their relative weight
neighbourMoves = [
	[NeighbourMove_TotalReorder, 1],
	[NeighbourMove_PartialReorder, 3],
	[NeighbourMove_SegmentShift, 5],
	[NeighbourMove_SwitchShift, 55],
	[NeighbourMove_SwapShifts, 15]
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

def FixDaysOff(solution, problem):
	for staffId, staffMember in problem.staff.items():
		schedule = solution.schedule[staffId]
		for idx in staffMember.daysOff:
			if schedule[idx] != ' ':
				otherIdx = idx
				while otherIdx in staffMember.daysOff:
					otherIdx = random.randint(0, problem.horizon - 1)
				schedule[idx], schedule[otherIdx] = schedule[otherIdx], schedule[idx]

def FixSolution(solution, problem):
	FixDaysOff(solution, problem)

def AnnealingSchedule(mu):
	return mu * 1.05

def Anneal(problem, maxTime = float('inf'), runs = 1):
	'''
	Try to solve the given problem while not exceeding 'maxTime'.
	'runs' is the number of tries to solve the problem. Each try should start from
	a different random configuration.
	'''
	# Solution variables
	timePerInstance = maxTime / runs
	bestSolution = None
	bestValidSolution = None

	# Annealing variables
	mu = -0.005
	totalIterations = 0
	accept = 0

	# Initialization
	MakeAccum(neighbourMoves)
	allShiftTypes = list(problem.shifts.keys())
	allShiftTypes.append(' ')

	for r in range(runs):
		solution = GenerateInitialConfiguration(problem)
		validator.CalculatePenalty(solution, problem)

		print ('Starting run<{}> with score {}'.format(r, solution.score))

		endTime = time.time() + timePerInstance

		if bestSolution is None:
			bestSolution = solution

		while True:
			if (time.time() > endTime):
				break

			if accept == 1000:
				mu = AnnealingSchedule(mu)
				accept = 0

			totalIterations += 1

			newSolution = copy.deepcopy(solution)
			ChooseMove(neighbourMoves)(newSolution, shiftTypes=allShiftTypes)
			FixSolution(newSolution, problem)
			validator.CalculatePenalty(newSolution, problem)

			if solution.hardViolations == 0 and (bestValidSolution is None or bestValidSolution.score > solution.score):
					bestValidSolution = solution
					print('Found better valid solution:', bestValidSolution.score)

			if newSolution.score <= solution.score or random.random() < math.exp(mu * (newSolution.score - solution.score)):
				solution = newSolution
				accept += 1
				if bestSolution.score > solution.score:
					bestSolution = solution
					print('Found better solution:', bestSolution.score)

	print('Total iterations:', totalIterations)
	if bestValidSolution is None:
		return bestSolution
	else:
		return bestValidSolution
