import solver
from instance import ProblemInstance

if __name__ == '__main__':
	test_file_name = 'instances1_24/instance1.txt'
	problem = ParseRoster(test_file_name)
	print (vars(problem))