import solver
import validator
from roster_parser import ParseRoster

if __name__ == '__main__':
	problem = ParseRoster('instances1_24/instance1.txt')
	solution = solver.Anneal(problem, 10.0)
	
	print('Score:', solution.score)
	print('Hard violations:', solution.hardViolations)
	solution.Show()
