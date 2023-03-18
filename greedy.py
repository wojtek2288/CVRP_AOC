import dataReader
import networkx as nx

def cvrp_greedy(graph : nx.Graph, capacity, num_ants=100, max_iterations=1000):
    best_solution = None
    best_distance = float('inf')

    for iteration in range(max_iterations):
        # Construct solutions with ants
        solutions = []
        for _ in range(num_ants):
            # Initialize ant
            ant = {'visited': set(), 'current_node': 1, 'path': []}
            capacity_left = capacity
            ant['visited'].add(1)
            ant['path'].append(1)

            # Build solution
            while len(ant['visited']) < len(graph.nodes()):
                # Get unvisited nodes
                unvisited_nodes = [node_id for node_id in graph.nodes() if node_id not in ant['visited']]
                reachable_nodes = []

                for node_id in unvisited_nodes:
                    if graph.nodes[node_id]['demand'] <= capacity_left:
                        reachable_nodes.append((node_id, graph[ant['current_node']][node_id]['weight']))

                if len(reachable_nodes) == 0:
                    next_node = 1
                    capacity_left = capacity
                else:
                    next_node = min(reachable_nodes, key=lambda x: x[1])[0]

                # Choose node to visit next
                ant['visited'].add(next_node)
                ant['current_node'] = next_node
                ant['path'].append(next_node)
                capacity_left -= graph.nodes[next_node]['demand']

            # Add return to depot
            ant['path'].append(1)

            # Calculate distance and update solutions
            distance = 0
            solution = []
            for i in range(len(ant['path']) - 1):
                node1, node2 = ant['path'][i], ant['path'][i+1]
                if node1 != node2:
                    solution.append((node1, node2))
                    distance += graph[node1][node2]['weight']
            solutions.append({'path': solution, 'distance': distance})

        best_ant = min(solutions, key=lambda x: x['distance'])

        if best_ant['distance'] < best_distance:
            best_solution = best_ant
            best_distance = best_ant['distance']

        print(str(iteration) + ": " + str(best_ant['distance']))

    return best_solution['path'], best_distance

graph, capacity = dataReader.read_input_file("22.txt")
best_solution, best_distance = cvrp_greedy(graph, capacity)

print("Best solution:")
print("distance: " + str(best_distance) + str(best_solution))