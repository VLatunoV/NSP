# NSP
A group project trying to solve the popular nurse scheduling/rostering problem.

The problem definition and test cases can be found [here](http://www.schedulingbenchmarks.org/)

## Model
We differentiate between valid and invalid configurations, but also use a penalty for validity to make them comparable. This penalty is ```k * max(all soft penalties), k > 1``` to impel removing as many hard constraint violations as possible.

## Implementation
We are using a **Simulated Annealing** approach:

+ Generate a random starting configuration based on the employee's contracts
+ Mininize the modified penalty function
+ Exponential cooling based on number of accepted moves
+ Different weighted move strategies chosen via their cumulative distribution

## Result
The approach is very dependant on the move strategies. Our implementation is not very effective, because the random changes disturb the structure of a feasible solution.