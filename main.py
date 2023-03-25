import DataReader
import AntFactory
import random
import CVRPSolver as cvrp

sum = 0
numExperiments = 5

for i in range(numExperiments):
    random.seed(i)
    graph, capacity = DataReader.readInputFile("inputs/E-n101-k8.txt")
    solution, distance, distances = cvrp.solve(AntFactory.EliteAntFactory(), graph, capacity, 10000, 50, 500, alpha=2, beta=1)
    sum += distance

avgDist = sum / numExperiments
print("Avarage distance: " + str(avgDist))
