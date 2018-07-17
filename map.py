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

        seed(ctx.id)

        while ((ammountOfNoise / fieldsNo) < mc['initialRatio']):
            x = randint(0, mc['size']-1)
            y = randint(0, mc['size']-1)
            if (self.__fields[x][y].value == fc['default_value']):
                self.__fields[x][y].value = 1
                ammountOfNoise += 1

    def __getFieldNeighbours(self, positionTuple): 
    #maybe better on the field side to store references to the neighbours instead of just the positions, then we could've just update them locally from the field itself (clearer the code would be)
        x, y = positionTuple
        mns = fc['mooreNeighbourhoodSize'];
        
        corner = [[fc['default_value']]*mns]*mns
        leftFields = corner + self.__eastbound + corner
        midFields = self.__northbound + [[f.value for f in frow] for frow in self.__fields] + self.__southbound
        rightFields = corner + self.__westbound + corner
        allFields = [i+j+g for i,j,g in zip(leftFields, midFields, rightFields)]

        isInRange = lambda x, y: (x >= 0 and x < mc['size'] 
                              and y >= 0 and y < mc['size'])

        neighboursValues = [[allFields[i+x][j+y] 
                            for j in range(0, 2*mns+1)] 
                            for i in range(0, 2*mns+1)]
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

    def __init__(self, id, ctx,
                        northbound=[[fc['default_value']]*mc['size']]*fc['mooreNeighbourhoodSize'],
                        westbound=[[fc['default_value']]*fc['mooreNeighbourhoodSize']]*mc['size'],
                        southbound=[[fc['default_value']]*mc['size']]*fc['mooreNeighbourhoodSize'],
                        eastbound=[[fc['default_value']]*fc['mooreNeighbourhoodSize']]*mc['size']):
        self.id = id;
        self.__context = ctx

        self.__northbound = northbound
        self.__westbound = westbound
        self.__southbound = southbound
        self.__eastbound = eastbound
        
        self.isAccessed = False
        self.__groups = []
        self.__fields = [[Field(fi, fj) for fj in range(mc['size'])] 
                                        for fi in range(mc['size'])]

        self.__genererateNoise();
        self.__setFieldsNeighbours();
        self.calculate()
        self.groupFields()

    def getNorthBound(self):
        
    def getSouthBound(self):
    
    def getEastBound(self):
    
    def getWestBound(self):

    def calculate(self):
        for i in range(mc['numberOfIterations']):
            for row in self.__fields:
                for f in row:
                    f.calculate()
            self.__setFieldsNeighbours();

    def access(self): #direction?
        raise NotImplementedError()
        IsAccessed = true;
        self.groupsWayoutsProviding()



    def groupFields(self):
        for row in self.__fields:
            for f in row: 
                if (f.value == 0 and f.groupId == gc['noGroupId']):
                    newGroup = Group(f)
                    newGroup.findRestOfTheFields(self.__fields)
                    self.__groups.append(newGroup)

    def groupsWayoutsProviding(self):
        for g in self.__groups:
            g.wayoutProviding(self.__fields)

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

