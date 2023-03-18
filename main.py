import DataReader
import AntFactory
import CVRPSolver as cvrp

graph22, capacity22 = DataReader.readInputFile("inputs/22.txt")
best_solution, best_distance = cvrp.solve(AntFactory.BasicAntFactory(), graph22, capacity22, 1000)

print("Distance: " + str(round(best_distance, 2)))
print("Best solution: " + str(best_solution))