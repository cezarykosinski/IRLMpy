from constants import groupConstants as gc
from constants import fieldConstants as fc


class Field:
    """
    todo
    """
    def __init__(self, x, y):
        self.position = x, y
        self.value = fc['default_value']
        self.groupId = gc['noGroupId']
        self._neighboursValues = []
        self.neighboursPositions = []

    def calculate(self):
        """
        todo
        :return:
        """
        numOfConsideredNeighbours = sum([len(list(filter(lambda x: not(x is None), row))) for row in self._neighboursValues])
        
        wagedNeighboursValues = [sum([n * w if n else 0 for (n, w) in list(zip(nrow, wrow))])
                                 for (nrow, wrow) in list(zip(self._neighboursValues, fc['wages']))]
        result = sum(wagedNeighboursValues) / numOfConsideredNeighbours 

        self.value = 1 if result > fc['condition'] else 0 #NOT GENERIC

    def display(self):
        """
        todo
        :return:
        """
        return [".", "#"][self.value] + " "

    def displayGroup(self):
        """
        todo
        :return:
        """
        return [str(self.groupId), "#"][self.value] + " "

