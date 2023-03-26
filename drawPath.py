import DataReader
import networkx as nx
import matplotlib.pyplot as plt
import AntFactory
import CVRPSolver as cvrp
import random

random.seed(0)
# Read input file and extract node attributes
graph, capacity = DataReader.readInputFile("inputs/E-n22-k4.txt")
pos = nx.get_node_attributes(graph, 'pos')
demands = nx.get_node_attributes(graph, 'demand')

# Get solution
iterationCount = 500
bestSolution, bestDistance, distances = cvrp.solve(AntFactory.EliteAntFactory(), graph, capacity, 10000, 50, iterationCount)

# Set the color of the labels based on the demands
node_colors = ['red' if demand == 0 else '#ADD8E6' for demand in demands.values()]

graph.remove_edges_from(list(graph.edges()))
# Draw the graph with the node demands as colored labels
i = 1
for (node1, node2) in bestSolution:
    graph.add_edge(node1, node2, weight = i)
    i += 1
labels = nx.get_edge_attributes(graph, 'weight')

plt.figure()  
plt.title('E-n22-k4, distance: ' + str(bestDistance))

nx.draw(graph, pos=pos, node_size=800, node_color=node_colors)
nx.draw_networkx_edge_labels(graph, pos,edge_labels=labels)
nx.draw_networkx_labels(graph, pos=pos, labels=demands, font_color='black')

plt.show()
