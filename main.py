import DataReader
import AntFactory
import random
import CVRPSolver as cvrp

sum = 0
numExperiments = 5
optimal = 521

for i in range(numExperiments):
    random.seed(i)
    graph, capacity = DataReader.readInputFile("inputs/E-n51-k5.txt")
    solution, distance, distances = cvrp.solve(AntFactory.EliteAntFactory(), graph, capacity, 2*optimal, 50, 500)
    sum += distance

avgDist = sum / numExperiments
print("Avarage distance: " + str(avgDist))
