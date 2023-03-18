import networkx as nx
import random
from abc import ABC, abstractmethod

class Ant(ABC):
    pheromones = {}

    def __init__(self, currentNode: int, capacity: int, graph: nx.Graph):
        self.visited = set([currentNode])
        self.currentNode = currentNode
        self.path = [currentNode]
        self.distance = 0
        self.capacity = capacity
        self.capacityLeft = capacity

    def goToNextNode(self, nextNode: int, graph: nx.Graph):
        self.distance += graph[self.currentNode][nextNode]['weight']
        self.visited.add(nextNode)
        self.currentNode = nextNode
        self.path.append(nextNode)
        self.capacityLeft -= graph.nodes[nextNode]['demand']

    def returnToDepot(self, depot: int, graph: nx.Graph):
        self.path.append(depot)
        if self.currentNode != depot:
            self.distance += graph[depot][self.currentNode]['weight']

    @staticmethod
    def initPheromones(graph: nx.Graph):
        for node1_id in graph.nodes():
            for node2_id in graph.nodes():
                Ant.pheromones[(node1_id, node2_id)] = 1

    @staticmethod
    def updatePheromones(evaporFactor: float, bestAntDistance: float, bestAntPath: list):
        # Update pheromones
        pheromoneDelta = 1 / bestAntDistance
        for node1_id, node2_id in bestAntPath:
            BasicAnt.pheromones[(node1_id, node2_id)] += pheromoneDelta
        # Evaporate pheromones
        for key in BasicAnt.pheromones.keys():
            BasicAnt.pheromones[key] *= (1 - evaporFactor)

    @abstractmethod
    def chooseNextNode(self, graph: nx.Graph, alpha: float, beta: float):
        pass

class BasicAnt(Ant):
    def __init__(self, currentNode: int, capacity: int, graph: nx.Graph):
        super().__init__(currentNode, capacity, graph)

    def chooseNextNode(self, graph: nx.Graph, alpha: float, beta: float):
        # Get unvisited nodes
        unvisited_nodes = [node_id for node_id in graph.nodes() if node_id not in self.visited]
        
        # Calculate probabilities of visiting each unvisited node
        probabilities = {}
        for node_id in unvisited_nodes:
            if graph.nodes[node_id]['demand'] <= self.capacityLeft:
                pheromone = BasicAnt.pheromones[(self.currentNode, node_id)]
                heuristic = 1 / graph[self.currentNode][node_id]['weight']
                probabilities[node_id] = (pheromone ** alpha) * (heuristic ** beta)
        probabilities = {node_id: prob / sum(probabilities.values()) for node_id, prob in probabilities.items()}

        if len(probabilities) == 0 and len(self.visited) < len(graph.nodes()):
            nextNode = 1
            self.capacityLeft = self.capacity
        else:
            nextNode = random.choices(list(probabilities.keys()), list(probabilities.values()))[0]

        self.goToNextNode(nextNode, graph)

class GreedyAnt(Ant):
    def __init__(self, currentNode: int, capacity: int, graph: nx.Graph):
        super().__init__(currentNode, capacity, graph)

    def chooseNextNode(self, graph: nx.Graph, alpha: float, beta: float):
        # Get unvisited nodes
        unvisited_nodes = [node_id for node_id in graph.nodes() if node_id not in self.visited]
        reachable_nodes = []

        for node_id in unvisited_nodes:
            if graph.nodes[node_id]['demand'] <= self.capacityLeft:
                reachable_nodes.append((node_id, graph[self.currentNode][node_id]['weight']))

        if len(reachable_nodes) == 0:
            nextNode = 1
            self.capacityLeft = self.capacity
        else:
            reachable_nodes = sorted(reachable_nodes, key=lambda x: x[1])
            smallest_nodes = [node[0] for node in reachable_nodes[:3]]
            nextNode = random.choice(smallest_nodes)

        self.goToNextNode(nextNode, graph)