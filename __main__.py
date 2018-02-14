import solver
import validator
import pylab
from roster_parser import ParseRoster

if __name__ == '__main__':
	problem = ParseRoster('instances1_24/instance4.txt')
	solution, graphData = solver.Anneal(problem, 100.0)
	solution2, graphData2 = solver.Anneal(problem, 100.0, useAnnealing = False)
	
	print('Score:', solution.score)
	print('Hard violations:', solution.hardViolations)
	solution.Show()

	print('Score:', solution2.score)
	print('Hard violations:', solution2.hardViolations)
	solution2.Show()

	for idx, _ in enumerate(graphData):
		x = [k[0] for k in graphData[idx]]
		y = [k[1] for k in graphData[idx]]
		y2 = [k[2] for k in graphData[idx]]
		pylab.plot(x, y, 'r')
		pylab.plot(x, y2, 'r--')

		x = [k[0] for k in graphData2[idx]]
		y = [k[1] for k in graphData2[idx]]
		y2 = [k[2] for k in graphData2[idx]]
		pylab.plot(x, y, 'b')
		pylab.plot(x, y2, 'b--')

		pylab.yscale('log')
		pylab.legend(['Annealing', 'Annealing valid', 'Hill climb', 'Hill climb valid'])
		pylab.show()
