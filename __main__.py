import solver
import validator
from roster_parser import ParseRoster

if __name__ == '__main__':
	test_file_name = 'instances1_24/instance1.txt'
	problem = ParseRoster(test_file_name)
	print(validator.calculatePenalty(solver.optimal_solution, problem))
