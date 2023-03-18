import math
import networkx as nx

def readInputFile(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]

    # Get capacity
    capacityLine = [line for line in lines if line.startswith('CAPACITY')][0]
    capacity = int(capacityLine.split()[-1])

    # Get node coordinates
    coordSectionStart = lines.index('NODE_COORD_SECTION') + 1
    coordSectionEnd = lines.index('DEMAND_SECTION')
    coordinates = {}
    for i in range(coordSectionStart, coordSectionEnd):
        node_id, x, y = lines[i].split()
        coordinates[int(node_id)] = (int(x), int(y))

    # Get demands
    demandSectionStart = coordSectionEnd + 1
    demandSectionEnd = lines.index('DEPOT_SECTION')
    demands = {}
    for i in range(demandSectionStart, demandSectionEnd):
        node_id, demand = lines[i].split()
        demands[int(node_id)] = int(demand)

    # Create graph with euclidean distances
    graph = nx.Graph()
    for node1 in coordinates:
        for node2 in coordinates:
            if node1 < node2:
                dist = math.sqrt((coordinates[node1][0] - coordinates[node2][0])**2 + 
                                 (coordinates[node1][1] - coordinates[node2][1])**2)
                graph.add_edge(node1, node2, weight=dist)

    # Add capacities as node attributes
    for node in graph.nodes:
        if node == 1:
            graph.nodes[node]['demand'] = 0
        else:
            graph.nodes[node]['demand'] = demands[node]

    return graph, capacity
