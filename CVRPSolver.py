import networkx as nx
import AntFactory
import AntFactory

def solve(
        antFactory: AntFactory.AntFactory,
        graph : nx.Graph,
        capacity: int,
        sMax: int,
        numAnts=50,
        maxIterations=500,
        evaporFactor=0.1,
        alpha=2,
        beta=3):

    antFactory.initPheromones(graph)
    bestSolution = None
    bestDistance = float('inf')

    for iteration in range(maxIterations):
        # Construct solutions with ants
        solutions = []
        for _ in range(numAnts):
            # Initialize ant
            ant = antFactory.createAnt(1, capacity, graph)

            # Build solution
            while len(ant.visited) < len(graph.nodes()):
                # Choose node to visit next
                ant.chooseNextNode(graph, alpha, beta)
                if ant.distance >= sMax:
                    break

            ant.returnToDepot(depot=1, graph=graph)
            if ant.distance > sMax:
                break

            # Update solutions
            solution = []
            for i in range(len(ant.path) - 1):
                node1, node2 = ant.path[i], ant.path[i+1]
                if node1 != node2:
                    solution.append((node1, node2))
            solutions.append({'path': solution, 'distance': ant.distance})

        if len(solutions) > 0:
            bestAnt = min(solutions, key=lambda x: x['distance'])

            if bestAnt['distance'] < bestDistance:
                bestSolution = bestAnt['path']
                bestDistance = bestAnt['distance']

            antFactory.updatePheromones(evaporFactor, bestDistance, bestSolution)

            print(str(iteration) + ": " + str(round(bestAnt['distance'], 2)))
        else:
            print(str(iteration) + ": No solution found")

    return bestSolution, bestDistance