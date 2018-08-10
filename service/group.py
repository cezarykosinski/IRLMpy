from constants import GROUP_CONSTANTS, MAP_CONSTANTS
from math import floor


class GroupService:

    @staticmethod
    def assign_group_to_fields(group_id, queue, fields):
        assigned_fields = []
        while queue:
            x, y = queue.pop()
            assigned_fields.append(fields[x][y])
            fields[x][y].group_id = group_id
            for npos in fields[x][y].neighbours_positions:
                if npos:
                    nx, ny = npos
                    if fields[nx][ny].value == FC['FLOOR'] and fields[nx][ny].group_id == GROUP_CONSTANTS['NO_GROUP_ID']: #fixed field value condition
                        queue.append((nx, ny))
        return assigned_fields

    @staticmethod
    def get_path(p_a, p_b):
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
            pts += [(p_a[0] + floor(i), p_a[1] + j), (p_a[0] + floor(i) + 1, p_a[1] + j)]
            i += step
        return pts

    @staticmethod
    def drill_wayout(fields, starting_position, destination_position):
        """
        todo
        :param fields:
        :param starting_position:
        :param destination_position:
        :return:
        """
        path_points = GroupService.get_path(starting_position, destination_position)
        for px, py in path_points:
            fields[px][py].value = FC['FLOOR']

    @staticmethod
    def closest_group_with_wayout(id, fields, position):
        """
        todo
        :param fields:
        :param position:
        :return:
        """
        queue = [(position, 0)] #chcialbym szybkie FIFO
        while queue:
            (x, y), counter = queue[0]
            # todo : FIFO
            queue = queue[1:]
            for npos in fields[x][y].neighbours_positions:
                if npos:
                    nx, ny = npos
                    if not fields[nx][ny].groupId == id or (fields[nx][ny].value == FC['FLOOR'] 
                                                                 and (MAP_CONSTANTS['SIZE'] - 1 not in fields[nx][ny].position)):
                        return counter, fields[nx][ny].group_id, (nx, ny) # todo discuss if proper: legacy x, y -> tuple ??
                    # todo : hardcoded, fixed constant in condition #and wishful mechanism of "_" that matches with everything
                    elif fields[nx][ny].value == FC['FLOOR'] and (nx, ny) not in [((x, y), tmp) in queue]: # todo :)
                        queue.append((nx, ny), counter + 1)
