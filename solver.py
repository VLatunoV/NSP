from roster_parser import ParseRoster

class SolutionInstance:
	'''
	schedule = {staffId: list(shiftId)}
	'''
	def __init__(self):
		self.horizon = 0
		self.score = 0
		self.schedule = dict()

# Instance 1
exact_solution = SolutionInstance()
exact_solution.horizon = 14
exact_solution.schedule['A'] = [' ', 'D', 'D', 'D', 'D', ' ', ' ', 'D', 'D', ' ', ' ', 'D', 'D', 'D']
exact_solution.schedule['B'] = ['D', 'D', 'D', 'D', 'D', ' ', ' ', 'D', 'D', ' ', ' ', 'D', 'D', ' ']
exact_solution.schedule['C'] = ['D', 'D', 'D', ' ', ' ', 'D', 'D', ' ', ' ', 'D', 'D', 'D', ' ', ' ']
exact_solution.schedule['D'] = ['D', 'D', ' ', ' ', ' ', 'D', 'D', 'D', 'D', 'D', ' ', ' ', ' ', ' ']
exact_solution.schedule['E'] = [' ', 'D', 'D', 'D', 'D', ' ', ' ', 'D', 'D', ' ', ' ', 'D', 'D', 'D']
exact_solution.schedule['F'] = ['D', 'D', 'D', 'D', 'D', ' ', ' ', 'D', 'D', ' ', ' ', ' ', 'D', 'D']
exact_solution.schedule['G'] = [' ', ' ', 'D', 'D', 'D', ' ', ' ', 'D', 'D', ' ', ' ', 'D', 'D', 'D']
exact_solution.schedule['H'] = ['D', 'D', ' ', ' ', ' ', ' ', ' ', ' ', 'D', 'D', 'D', 'D', 'D', ' ']
exact_solution.optimal_score = 607

'''
Simulated Annealing has 4 major parts:
	1. A valid start configuration
	2. A random rearrangement scheme
	3. An objective function
	4. An annealing schedule
'''
