import DataReader
import AntFactory
import random
import CVRPSolver as cvrp

sum = 0
numExperiments = 5

for i in range(numExperiments):
    random.seed(i)
    graph, capacity = DataReader.readInputFile("inputs/E-n22-k4.txt")
    solution, distance, distances = cvrp.solve(AntFactory.BasicAntFactory(), graph, capacity, 1000, 50, 500)
    sum += distance

avgDist = sum / numExperiments
print("Avarage distance: " + str(avgDist))
