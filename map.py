from random import seed, randint
from field import Field
from group import Group
from constants import fieldConstants as fc
from constants import groupConstants as gc
from constants import mapConstants as mc

class Map:
    def __genererateNoise(self):
        fieldsNo = mc['size']**2;
        ammountOfNoise = 0;

        seed(mc['seed'])

        while ((ammountOfNoise / fieldsNo) < mc['initialRatio']):
            x = randint(0, mc['size']-1)
            y = randint(0, mc['size']-1)
            if (self.__fields[x][y].value == fc['default_value']):
                self.__fields[x][y].value = 1
                ammountOfNoise += 1

    def __getFieldNeighbours(self, positionTuple):
        x, y = positionTuple
        mns = fc['mooreNeighbourhoodSize'];

        isInRange = lambda x, y: (x >= 0 and x < mc['size'] 
                           and y >= 0 and y < mc['size'])

        neighboursValues = [[self.__fields[i+x][j+y].value 
                            if isInRange(i+x, j+y) 
                            else None 
                            for j in range(-mns, mns+1)] 
                            for i in range(-mns, mns+1)]
        neighboursPositions = [self.__fields[i+x][j+y].position 
                                if isInRange(i+x, j+y) 
                                else None 
                                for j in range(-mns, mns+1)
                                for i in range(-mns, mns+1)]
        return neighboursValues, neighboursPositions
    
    def __setFieldsNeighbours(self):
        for row in self.__fields:
            for f in row: 
                f.neighboursValues, f.neighboursPositions = self.__getFieldNeighbours(f.position)

    def __init__(self, id):
        self.id = id;
        self.mapsNeighbours = []
        self.isAccessed = False
        self.__groups = []
        self.__fields = [[Field(fi, fj) for fj in range(mc['size'])] 
                                        for fi in range(mc['size'])]

        self.__genererateNoise();
        self.__setFieldsNeighbours();

    def calculate(self):
        for i in range(mc['numberOfIterations']):
            for row in self.__fields:
                for f in row:
                    f.calculate()
            self.__setFieldsNeighbours();

    def access(self):
        raise NotImplementedError()
        IsAccessed = true;

    def groupFields(self):
        for row in self.__fields:
            for f in row: 
                if (f.value == 0 and f.groupId == gc['noGroupId']):
                    newGroup = Group(f)
                    newGroup.findRestOfTheFields(self.__fields)
                    self.__groups.append(newGroup)

    def connectGroups(self):
        fun = lambda g1, g2: group.ConcatAndDrill(g1,g2, self.__fields)
        self.__groups = reduce(fun, self.__groups)

    def display(self):
        for row in self.__fields:
            row_display = ""
            for f in row: 
                row_display += f.display()
            print(row_display)

    def displayGroups(self):
        for row in self.__fields:
            row_display = ""
            for f in row: 
                row_display += f.displayGroup()
            print(row_display)

