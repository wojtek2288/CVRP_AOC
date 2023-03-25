import heapq
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
        for node1Id in graph.nodes():
            for node2Id in graph.nodes():
                Ant.pheromones[(node1Id, node2Id)] = 1

    @abstractmethod
    def updatePheromones(self):
        pass

    @staticmethod
    def evaporatePheromones(evaporFactor: float):
        pass

    def chooseNextNode(self, graph: nx.Graph, alpha: float, beta: float):
        # Get unvisited nodes
        unvisitedNodes = [nodeId for nodeId in graph.nodes() if nodeId not in self.visited]
        
        # Calculate probabilities of visiting each unvisited node
        probabilities = {}
        for node_id in unvisitedNodes:
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

class BasicAnt(Ant):
    def __init__(self, currentNode: int, capacity: int, graph: nx.Graph):
        super().__init__(currentNode, capacity, graph)

    def chooseNextNode(self, graph: nx.Graph, alpha: float, beta: float):
        super().chooseNextNode(graph, alpha, beta)

    def updatePheromones(self):
        pheromoneDelta = 1 / self.distance
        for i in range(len(self.path) - 1):
            node1, node2 = self.path[i], self.path[i+1]
            if node1 != node2:
                BasicAnt.pheromones[(node1, node2)] += pheromoneDelta

    def evaporatePheromones(evaporFactor: float):
        for key in BasicAnt.pheromones.keys():
            BasicAnt.pheromones[key] *= (1 - evaporFactor)

class ClosestOnlyAnt(Ant):
    def __init__(self, currentNode: int, capacity: int, graph: nx.Graph):
        super().__init__(currentNode, capacity, graph)

    def chooseNextNode(self, graph: nx.Graph, alpha: float, beta: float):
        # Get unvisited nodes
        unvisitedNodes = [nodeId for nodeId in graph.nodes() if nodeId not in self.visited]

        closestNodes = heapq.nsmallest(5, unvisitedNodes, key=lambda nodeId: graph[self.currentNode][nodeId]['weight'])
        
        # Calculate probabilities of visiting each unvisited node
        probabilities = {}
        for node_id in closestNodes:
            if graph.nodes[node_id]['demand'] <= self.capacityLeft:
                pheromone = ClosestOnlyAnt.pheromones[(self.currentNode, node_id)]
                heuristic = 1 / graph[self.currentNode][node_id]['weight']
                probabilities[node_id] = (pheromone ** alpha) * (heuristic ** beta)
        probabilities = {node_id: prob / sum(probabilities.values()) for node_id, prob in probabilities.items()}

        if len(probabilities) == 0 and len(self.visited) < len(graph.nodes()):
            nextNode = 1
            self.capacityLeft = self.capacity
        else:
            nextNode = random.choices(list(probabilities.keys()), list(probabilities.values()))[0]

        self.goToNextNode(nextNode, graph)

    def updatePheromones(self):
        pheromoneDelta = 1 / self.distance
        for i in range(len(self.path) - 1):
            node1, node2 = self.path[i], self.path[i+1]
            if node1 != node2:
                ClosestOnlyAnt.pheromones[(node1, node2)] += pheromoneDelta

    def evaporatePheromones(evaporFactor: float):
        for key in ClosestOnlyAnt.pheromones.keys():
            ClosestOnlyAnt.pheromones[key] *= (1 - evaporFactor)

class EliteAnt(Ant):
    def __init__(self, currentNode: int, capacity: int, graph: nx.Graph):
        super().__init__(currentNode, capacity, graph)

    def chooseNextNode(self, graph: nx.Graph, alpha: float, beta: float):
        super().chooseNextNode(graph, alpha, beta)

    def updatePheromones(self):
        pass

    @staticmethod
    def updateBestPheromones(bestSolution: list, bestDistance: float):
        pheromoneDelta = 1 / bestDistance
        for i in range(len(bestSolution) - 1):
            for node1_id, node2_id in bestSolution:
                if node1_id != node2_id:
                    EliteAnt.pheromones[(node1_id, node2_id)] += pheromoneDelta

    def evaporatePheromones(evaporFactor: float):
        for key in EliteAnt.pheromones.keys():
            EliteAnt.pheromones[key] *= (1 - evaporFactor)

class GreedyAnt(Ant):
    def __init__(self, currentNode: int, capacity: int, graph: nx.Graph):
        super().__init__(currentNode, capacity, graph)

    def chooseNextNode(self, graph: nx.Graph, alpha: float, beta: float):
        # Get unvisited nodes
        unvisitedNodes = [nodeId for nodeId in graph.nodes() if nodeId not in self.visited]
        reachableNodes = []

        for node_id in unvisitedNodes:
            if graph.nodes[node_id]['demand'] <= self.capacityLeft:
                reachableNodes.append((node_id, graph[self.currentNode][node_id]['weight']))

        if len(reachableNodes) == 0:
            nextNode = 1
            self.capacityLeft = self.capacity
        else:
            reachableNodes = sorted(reachableNodes, key=lambda x: x[1])
            smallest_nodes = [node[0] for node in reachableNodes[:3]]
            nextNode = random.choice(smallest_nodes)

        self.goToNextNode(nextNode, graph)

    def updatePheromones(self):
        pass

    def evaporatePheromones(evaporFactor: float):
        pass