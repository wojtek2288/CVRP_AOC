import DataReader
import AntFactory
import random
import CVRPSolver as cvrp
import networkx as nx
import matplotlib.pyplot as plt

random.seed(10)
graph22, capacity22 = DataReader.readInputFile("inputs/15.txt")
best_solution, best_distance = cvrp.solve(AntFactory.EliteAntFactory(), graph22, capacity22, 2000, 50, 500)

print("Distance: " + str(round(best_distance, 2)))
print("Best solution: " + str(best_solution))