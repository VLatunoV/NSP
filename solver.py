import random
import math
import time
from roster_parser import ParseRoster

class SolutionInstance:
	'''
	schedule = {staffId: list(shiftId)}
	'''
	def __init__(self):
		self.horizon = 0
		self.score = 0
		self.schedule = dict()

def CreateEmptySolution(problem):
	result = SolutionInstance()
	result.horizon = problem.horizon

	for staffId in problem.staff.keys():
		result.schedule[staffId] = [' '] * horizon

	return result

# Instance 1
exact_solution = SolutionInstance()
exact_solution.horizon = 14
exact_solution.score = 607
exact_solution.schedule['A'] = [' ', 'D', 'D', 'D', 'D', ' ', ' ', 'D', 'D', ' ', ' ', 'D', 'D', 'D']
exact_solution.schedule['B'] = ['D', 'D', 'D', 'D', 'D', ' ', ' ', 'D', 'D', ' ', ' ', 'D', 'D', ' ']
exact_solution.schedule['C'] = ['D', 'D', 'D', ' ', ' ', 'D', 'D', ' ', ' ', 'D', 'D', ' ', ' ', ' ']
exact_solution.schedule['D'] = ['D', 'D', ' ', ' ', ' ', 'D', 'D', 'D', 'D', 'D', ' ', ' ', ' ', ' ']
exact_solution.schedule['E'] = [' ', 'D', 'D', 'D', 'D', ' ', ' ', 'D', 'D', ' ', ' ', 'D', 'D', 'D']
exact_solution.schedule['F'] = ['D', 'D', 'D', ' ', ' ', ' ', ' ', 'D', 'D', 'D', ' ', ' ', 'D', 'D']
exact_solution.schedule['G'] = [' ', ' ', 'D', 'D', 'D', ' ', ' ', 'D', 'D', ' ', ' ', 'D', 'D', 'D']
exact_solution.schedule['H'] = ['D', 'D', ' ', ' ', 'D', 'D', ' ', ' ', 'D', 'D', 'D', 'D', ' ', ' ']

solution = SolutionInstance()
solution.horizon = 14
solution.score = 708
solution.schedule['A'] = [' ', 'D', 'D', 'D', 'D', ' ', ' ', 'D', 'D', ' ', ' ', 'D', 'D', 'D']
solution.schedule['B'] = ['D', 'D', 'D', 'D', 'D', ' ', ' ', 'D', 'D', ' ', ' ', 'D', 'D', ' ']
solution.schedule['C'] = ['D', 'D', 'D', ' ', ' ', 'D', 'D', ' ', ' ', 'D', 'D', 'D', ' ', ' ']
solution.schedule['D'] = ['D', 'D', ' ', ' ', ' ', 'D', 'D', 'D', 'D', 'D', ' ', ' ', ' ', ' ']
solution.schedule['E'] = [' ', 'D', 'D', 'D', 'D', ' ', ' ', 'D', 'D', ' ', ' ', 'D', 'D', 'D']
solution.schedule['F'] = ['D', 'D', 'D', 'D', 'D', ' ', ' ', 'D', 'D', ' ', ' ', ' ', 'D', 'D']
solution.schedule['G'] = [' ', ' ', 'D', 'D', 'D', ' ', ' ', 'D', 'D', ' ', ' ', 'D', 'D', 'D']
solution.schedule['H'] = ['D', 'D', ' ', ' ', ' ', ' ', ' ', ' ', 'D', 'D', 'D', 'D', 'D', ' ']

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
	#staffId = random.choice(list(solution.schedule.keys()))
	staffId = 'A'
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

	print(startIndex)

	seq1, seq2 = 0, 0
	while seq1 == seq2:
		seq1 = random.randint(0, len(startIndex))
		seq2 = random.randint(0, len(startIndex))

	print(seq1, seq2)
	startIndex.append(solution.horizon)



def Anneal(problem, maxTime = float('inf'), instances = 1):
	'''
	Try to solve the given problem while not exceeding 'maxTime'.
	'instances' is the number of tries to solve the problem. Each try should start from
	a different random configuration.
	'''
	# Solution variables
	timePerInstance = maxTime / instances
	bestSolution = CreateEmptySolution(problem)
	bestSolution.score = Score(bestSolution)

	# Annealing variables
	mu = -math.exp(1.0) / float(bestSolution.score)
	
	for _ in range(instances):
		solution = GenerateRandomSolution(problem)
		endTime = time.time() + timePerInstance

		while True:
			if (time.time() > endTime):
				break

			FindNeighbour(solution)
			score = Score(solution)
			valid = Validate(solution)

NeighbourMove_PartialReorder(exact_solution)
