from constants import groupConstants as gc
from constants import fieldConstants as fc

class Field:
    def __init__(self, x, y):
        self.position = x, y
        self.value = 0
        self.groupId = gc['noGroupId']
        self.neighboursValues = []
        self.neighboursPositions = []

    def calculate(self):
        numOfConsideredNeighbours = sum([len(list(filter(lambda x: not(x is None), row))) for row in self.neighboursValues])
        
        wagedNeighboursValues = [sum([n*w if n else 0 for (n,w) in list(zip(nrow,wrow))]) for (nrow,wrow) in list(zip(self.neighboursValues, fc['wages']))]

       # print(self.position)
       # print("neighboursValues")
       # print(self.neighboursValues)
       # print("wagedNeighboursValues")
       # print(wagedNeighboursValues)
       # print()

        result = sum(wagedNeighboursValues) / numOfConsideredNeighbours 

        self.value = 1 if result > fc['condition'] else 0 #NOT GENERIC

    def display(self):
        return [".", "#"][self.value] + " "

    def displayGroup(self):
        return [str(self.groupId), "#"][self.value] + " "

