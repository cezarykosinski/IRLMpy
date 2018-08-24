from constants import GROUP_CONSTANTS, MAP_CONSTANTS as MC, FIELD_CONSTANTS as FC
from math import floor
from collections import defaultdict

class GroupService:

    @staticmethod
    def find_path(start_point, end_point, fields, levels):
        path = [end_point]
        while start_point not in path:
            x, y = path[0]
            nghbrs = [neighbour.position for neighbour in fields[x][y].neighbours]
            for i in levels[lvl]:



    @staticmethod
    def find_closest_group(starting_point, fields, min_path):
        queue = [(0, starting_point)]
        visited = set()
        levels = defaultdict(lambda: [])
        xs, ys = starting_point
        starting_group_id = fields[xs][ys].group_id
        while queue:
            path_len, (x, y) = queue[0]
            levels.update({path_len: (levels[path_len] + (x,y))})
            visited.add((x,y))
            if path_len > min_path:
                return None, min_path
            if fields[x][y].value == FC['FLOOR']:
                return (starting_point, (x, y)), path_len, GroupService.find_path(starting_point,(x,y), fields, levels)
            queue = queue[1:]
            neighbours = [(path_len + 1, n.positon) for n in fields[x][y].neighbours if n.group_id != starting_group_id
                          and MC['SIZE'] - 1 not in n.positon]
            queue.extend([(l, n) for l, n in neighbours if n not in visited])
        return None, min_path

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
                    if fields[nx][ny].value == FC['FLOOR'] and fields[nx][ny].group_id == GROUP_CONSTANTS['NO_GROUP_ID']:
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
