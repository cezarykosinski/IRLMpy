from constants import groupConstants

class Group:
    latestId = 0
    
    def __init__(self, starting_field):
        self.id = Group.latestId
        self.__startingFieldPosition = starting_field.position
        self.__boarders = []
        self.__fields = []
        Group.latestId += 1
    
    def findRestOfTheFields(self, fields):
        queue = [self.__startingFieldPosition]
        while(queue):
            x, y = queue.pop()
            self.__fields.append(fields[x][y])
            fields[x][y].groupId = self.id
            for npos in fields[x][y].neighboursPositions:
                if npos:
                    nx,ny = npos
                    if fields[nx][ny].value == 0 and fields[nx][ny].groupId == groupConstants['noGroupId']:
                        queue.append((nx,ny))
