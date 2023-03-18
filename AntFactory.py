import Ant
import networkx as nx
from abc import ABC

class AntFactory(ABC):
    def createAnt(self, currentNode: int, capacity: int, graph: nx.Graph):
        raise NotImplementedError()
    
    def initPheromones(self, graph: nx.Graph):
        raise NotImplementedError()

    def updatePheromones(self, evaporFactor: float, bestAntDistance: float, bestAntPath: list):
        raise NotImplementedError()
    
class BasicAntFactory(AntFactory):
    def createAnt(self, currentNode: int, capacity: int, graph: nx.Graph):
        return Ant.BasicAnt(currentNode, capacity, graph)

    def initPheromones(self, graph: nx.Graph):
        Ant.BasicAnt.initPheromones(graph)

    def updatePheromones(self, evaporFactor: float, bestAntDistance: float, bestAntPath: list):
        Ant.BasicAnt.updatePheromones(evaporFactor, bestAntDistance, bestAntPath)

class GreedyAntFactory(AntFactory):
    def createAnt(self, currentNode: int, capacity: int, graph: nx.Graph):
        return Ant.GreedyAnt(currentNode, capacity, graph)

    def initPheromones(self, graph: nx.Graph):
        pass

    def updatePheromones(self, evaporFactor: float, bestAntDistance: float, bestAntPath: list):
        pass