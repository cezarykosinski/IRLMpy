from constants import groupConstants, mapConstants


class Group:
    """
    todo
    """
    latestId = 0
    
    def __init__(self, starting_field):
        """
        todo
        :param starting_field:
        """
        self.id = Group.latestId
        self.__startingFieldPosition = starting_field.position
        self.__boarders = []
        self.__fields = []
        Group.latestId += 1
    
    def findRestOfTheFields(self, fields):
        """
        todo
        :param fields:
        :return:
        """
        queue = [self.__startingFieldPosition]
        while queue:
            x, y = queue.pop()
            # todo: 2 times iteration through one list -> save it to var??
            self.__fields.append(fields[x][y])
            # todo: v
            fields[x][y].groupId = self.id
            for npos in fields[x][y].neighboursPositions:
                if npos:
                    nx, ny = npos
                    if fields[nx][ny].value == 0 and fields[nx][ny].groupId == groupConstants['noGroupId']: #fixed field value condition
                        queue.append((nx, ny))
    
    def updateTheBoarders(self):
        """
        todo
        :return:
        """
        self.__boarders = [f.position for f in self.__fields if (1 in f.neighboursValues)]

    def __hasWayoutAlready(self):
        """
        todo
        :return:
        """
        return len([pos for pos in self.__boarders if (mapConstants['size']-1 in pos)]) > 0
    
    def __getPath(self, pA, pB):
        """
        todo
        :param pA:
        :param pB:
        :return:
        """
        xv, yv = pA[0] - pB[0], pA[1] - pB[1]
        step = xv / yv
        pts = []
        i = 0
        for j in range(yv):
            pts += [(pA[0] + int(i), pA[1] + j), (pA[0] + int(i) + 1, pA[1] + j)]
            i += step
        return pts

    def __drillWayout(self, fields, starting_position, destination_position):
        """
        todo
        :param fields:
        :param starting_position:
        :param destination_position:
        :return:
        """
        pathPoints = self.__getPath(starting_position, destination_position)
        for px, py in pathPoints:
            fields[px][py].value = 0
            
    def __closestGroupWithWayout(self, fields, position):
        """
        todo
        :param fields:
        :param position:
        :return:
        """
        queue = [(position, 0)] #chcialbym szybkie FIFO
        while queue:
            x, y, counter = queue[0]
            # todo : FIFO
            queue = queue[1:]
            for npos in fields[x][y].neighboursPositions:
                if npos:
                    nx, ny = npos
                    if not fields[nx][ny].groupId == self.id or (fields[nx][ny].value == 0
                                                                 and (not (mapConstants['size']-1 in fields[nx][ny].position))):
                        return counter, fields[nx][ny].groupId, (nx, ny) # todo discuss if proper: legacy x, y -> tuple ??
                    # todo : hardcoded, fixed constant in condition #and wishful mechanism of "_" that matches with everything
                    elif fields[nx][ny].value == 0 and not (nx, ny, _) in queue: # todo :)
                        queue.append((nx, ny, counter + 1))

    def wayoutProviding(self, fields):
        """
        todo
        :param fields:
        :return:
        """
        self.updateTheBoarders()
        if not self.__hasWayoutAlready():
            # todo :o hmm?
            mindist = mapConstants['size'], mingroupId = self.id, minsource = self.__startingFieldPosition,  minendpoint = self.__startingFieldPosition
            for pos in self.__boarders:
                distance, groupId, endpoint = self.__closestGroupWithWayout(fields, pos)
                if distance < mindist:
                    # todo :o hmm?
                    mindist = distance, mingroupId = groupId, minsource = f, minendpoint = endpoint
            self.__drillWayout(fields, minsource, minendpoint)
