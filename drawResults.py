import DataReader
import AntFactory
import random
import CVRPSolver as cvrp
import matplotlib.pyplot as plt

iterationCount = 500
random.seed(0)
graph, capacity = DataReader.readInputFile("inputs/E-n101-k8.txt")
_, _, basicDistances = cvrp.solve(AntFactory.BasicAntFactory(), graph, capacity, 10000, 50, iterationCount)
_, _, greedyDistances = cvrp.solve(AntFactory.GreedyAntFactory(), graph, capacity, 10000, 50, iterationCount)
_, _, eliteDistances = cvrp.solve(AntFactory.EliteAntFactory(), graph, capacity, 10000, 50, iterationCount)
_, _, closestDistances = cvrp.solve(AntFactory.ClosestOnlyAntFactory(), graph, capacity, 10000, 50, iterationCount)

x_values = list(range(1, iterationCount + 1))
plt.scatter(x_values, basicDistances, s = 20, color = 'green', label = 'Basic Ants')
plt.scatter(x_values, greedyDistances, s = 20, color = 'orange', label = 'Greedy Ants')
plt.scatter(x_values, eliteDistances, s = 20, color = 'violet', label = 'Elite Ants')
plt.scatter(x_values, closestDistances, s = 20, color = 'blue', label = 'Closest Only Ants')

# Set the optimal distance
optimal_distance = 817

# Add a horizontal line for the optimal distance
plt.axhline(y=optimal_distance, color='r', linestyle='-', label = 'Optimal Distance')

# Set the axis labels and title
plt.xlabel('Iteration')
plt.ylabel('Distance')
plt.title('E-n101-k8')
plt.legend()

# Show the plot
plt.show()
