from constants import GROUP_CONSTANTS, MAP_CONSTANTS


class Group:
    """
    todo
    """
    LASTEST_ID = 0
    
    def __init__(self, starting_field):
        """
        todo
        :param starting_field:
        """
        self.id = Group.LASTEST_ID
        self.__starting_field_position = starting_field.position
        self.__boarders = []
        self.__fields = []
        Group.LASTEST_ID += 1
    
    def find_rest_of_the_fields(self, fields):
        """
        todo
        :param fields:
        :return:
        """
        queue = [self.__starting_field_position]
        while queue:
            x, y = queue.pop()
            # todo: 2 times iteration through one list -> save it to var??
            self.__fields.append(fields[x][y])
            # todo: v
            fields[x][y].group_id = self.id
            for npos in fields[x][y].neighbours_positions:
                if npos:
                    nx, ny = npos
                    if fields[nx][ny].value == 0 and fields[nx][ny].group_id == GROUP_CONSTANTS['NO_GROUP_ID']: #fixed field value condition
                        queue.append((nx, ny))
    
    def update_the_boarders(self):
        """
        todo
        :return:
        """
        self.__boarders = [f.position for f in self.__fields if (1 in f.neighboursValues)]

    def __has_wayout_already(self):
        """
        todo
        :return:
        """
        return len([pos for pos in self.__boarders if (MAP_CONSTANTS['SIZE'] - 1 in pos)]) > 0
    
    def __get_path(self, p_a, p_b):
        """
        todo
        :param p_a:
        :param p_b:
        :return:
        """
        xv, yv = p_a[0] - p_b[0], p_a[1] - p_b[1]
        step = xv / yv
        pts = []
        i = 0
        for j in range(yv):
            pts += [(p_a[0] + int(i), p_a[1] + j), (p_a[0] + int(i) + 1, p_a[1] + j)]
            i += step
        return pts

    def __drill_wayout(self, fields, starting_position, destination_position):
        """
        todo
        :param fields:
        :param starting_position:
        :param destination_position:
        :return:
        """
        path_points = self.__get_path(starting_position, destination_position)
        for px, py in path_points:
            fields[px][py].value = 0
            
    def __closest_group_with_wayout(self, fields, position):
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
            for npos in fields[x][y].neighbours_positions:
                if npos:
                    nx, ny = npos
                    if not fields[nx][ny].groupId == self.id or (fields[nx][ny].value == 0
                                                                 and (not (MAP_CONSTANTS['SIZE'] - 1 in fields[nx][ny].position))):
                        return counter, fields[nx][ny].group_id, (nx, ny) # todo discuss if proper: legacy x, y -> tuple ??
                    # todo : hardcoded, fixed constant in condition #and wishful mechanism of "_" that matches with everything
                    elif fields[nx][ny].value == 0 and not (nx, ny, _) in queue: # todo :)
                        queue.append((nx, ny, counter + 1))

    def wayout_providing(self, fields):
        """
        todo
        :param fields:
        :return:
        """
        self.update_the_boarders()
        if not self.__has_wayout_already():
            # todo :o hmm?
            mindist = MAP_CONSTANTS['SIZE'], mingroup_id = self.id, minsource = self.__starting_field_position, minendpoint = self.__starting_field_position
            for pos in self.__boarders:
                distance, group_id, endpoint = self.__closest_group_with_wayout(fields, pos)
                if distance < mindist:
                    # todo :o hmm?
                    mindist = distance, mingroup_id = group_id, minsource = f, minendpoint = endpoint
            self.__drill_wayout(fields, minsource, minendpoint)
