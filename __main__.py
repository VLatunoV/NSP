import solver
import validator
from roster_parser import ParseRoster

if __name__ == '__main__':
	test_file_name = 'instances1_24/instance1.txt'
	problem = ParseRoster(test_file_name)
	solution = solver.instance1_optimal_solution
	#solution = solver.Anneal(problem, 10.0)
	'''
	print(vars(problem.cover[5]['D']))
	solution = solver.SolutionInstance()
	solution.horizon = 14
	solution.schedule['A'] = [' ', 'D', 'D', 'D', 'D', ' ', ' ', 'D', 'D', ' ', ' ', 'D', 'D', 'D']
	solution.schedule['B'] = ['D', 'D', 'D', 'D', 'D', ' ', ' ', 'D', 'D', ' ', ' ', 'D', 'D', ' ']
	solution.schedule['C'] = ['D', 'D', 'D', ' ', ' ', 'D', 'D', ' ', ' ', 'D', 'D', 'D', ' ', ' ']
	solution.schedule['D'] = ['D', 'D', ' ', ' ', ' ', 'D', 'D', 'D', 'D', ' ', ' ', 'D', ' ', ' ']
	solution.schedule['E'] = [' ', 'D', 'D', 'D', 'D', ' ', ' ', 'D', 'D', ' ', ' ', 'D', 'D', 'D']
	solution.schedule['F'] = ['D', 'D', 'D', 'D', 'D', ' ', ' ', 'D', 'D', ' ', ' ', ' ', 'D', 'D']
	solution.schedule['G'] = [' ', ' ', 'D', 'D', 'D', ' ', ' ', 'D', 'D', ' ', ' ', 'D', 'D', 'D']
	solution.schedule['H'] = ['D', 'D', ' ', ' ', ' ', ' ', ' ', ' ', 'D', 'D', 'D', 'D', 'D', ' ']'''
	solution.score = validator.CalculatePenalty(solution, problem)
	solution.isValid = validator.ValidateSolution(solution, problem)
	
	print('Score:', solution.score)
	print('Valid: ', solution.isValid)
	solution.Show()
	solution.PrintDebug()
