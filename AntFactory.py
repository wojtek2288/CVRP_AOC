import Ant
import networkx as nx
from abc import ABC

class AntFactory(ABC):
    def createAnt(self, currentNode: int, capacity: int, graph: nx.Graph):
        raise NotImplementedError()
    
    def initPheromones(self, graph: nx.Graph):
        raise NotImplementedError()

    def updatePheromones(self, bestSolution: list, bestDistance: float):
        raise NotImplementedError()

    def evaporatePheromones(self, evaporFactor: float):
        raise NotImplementedError()
    
class BasicAntFactory(AntFactory):
    def createAnt(self, currentNode: int, capacity: int, graph: nx.Graph):
        return Ant.BasicAnt(currentNode, capacity, graph)

    def initPheromones(self, graph: nx.Graph):
        Ant.BasicAnt.initPheromones(graph)

    def updatePheromones(self, bestSolution: list, bestDistance: float):
        pass

    def evaporatePheromones(self, evaporFactor: float):
        Ant.BasicAnt.evaporatePheromones(evaporFactor)

class ClosestOnlyAntFactory(AntFactory):
    def createAnt(self, currentNode: int, capacity: int, graph: nx.Graph):
        return Ant.ClosestOnlyAnt(currentNode, capacity, graph)

    def initPheromones(self, graph: nx.Graph):
        Ant.ClosestOnlyAnt.initPheromones(graph)

    def updatePheromones(self, bestSolution: list, bestDistance: float):
        pass

    def evaporatePheromones(self, evaporFactor: float):
        Ant.ClosestOnlyAnt.evaporatePheromones(evaporFactor)

class EliteAntFactory(AntFactory):
    def createAnt(self, currentNode: int, capacity: int, graph: nx.Graph):
        return Ant.EliteAnt(currentNode, capacity, graph)

    def initPheromones(self, graph: nx.Graph):
        Ant.EliteAnt.initPheromones(graph)

    def updatePheromones(self, bestSolution: list, bestDistance: float):
        Ant.EliteAnt.updateBestPheromones(bestSolution, bestDistance)

    def evaporatePheromones(self, evaporFactor: float):
        Ant.EliteAnt.evaporatePheromones(evaporFactor)

class GreedyAntFactory(AntFactory):
    def createAnt(self, currentNode: int, capacity: int, graph: nx.Graph):
        return Ant.GreedyAnt(currentNode, capacity, graph)

    def initPheromones(self, graph: nx.Graph):
        pass

    def updatePheromones(self, bestSolution: list, bestDistance: float):
        pass

    def evaporatePheromones(self, evaporFactor: float):
        pass