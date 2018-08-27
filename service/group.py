from constants import GROUP_CONSTANTS, MAP_CONSTANTS as MC, FIELD_CONSTANTS as FC
from math import floor
from collections import defaultdict

class GroupService:

    @staticmethod
    def assign_group_to_fields(group_id, start_pos, fields):
        #import pdb; pdb.set_trace()
        queue = [start_pos]
        assigned_fields = []
        map_id = fields[start_pos[0]][start_pos[1]].map_id
        print(map_id)
        while queue:
            x, y = queue.pop()
            assigned_fields.append((x,y))
            fields[x][y].group_id = group_id
            for n in fields[x][y].neighbours:
                if n.value == FC['FLOOR'] and n.map_id == map_id and n.group_id == GROUP_CONSTANTS['NO_GROUP_ID']:# and n.position not in assigned_fields:
                    queue.append(n.position)
        return assigned_fields

    @staticmethod
    def drill_path(path, fields):
        for pos in path:
            x, y = pos 
            fields[x][y].value = FC['FLOOR']

    @staticmethod
    def _find_path(start_point, end_point, fields, levels, lvl):
        if end_point == start_point:
            return [start_point]
        else:
            x, y = end_point
            for pos in levels[lvl]:
                if pos in [n.positions for n in fields[x][y].neighbours]:
                    res = _find_path(start_point, pos, fields, levels, lvl - 1)
                    if res:
                        res.insert(0, pos)
            return None


    @staticmethod
    def find_path_to_closest_group(starting_point, fields, min_path_len):
        queue = [(0, starting_point)]
        visited = set()
        levels = defaultdict(lambda: [])
        xs, ys = starting_point
        starting_group_id = fields[xs][ys].group_id
        while queue:
            path_len, (x, y) = queue[0]
            levels.update({path_len: (levels[path_len] + (x,y))})
            visited.add((x,y))
            if path_len > min_path_len:
                return None, min_path_len, None
            if fields[x][y].value == FC['FLOOR']:
                return (starting_point, (x, y)), path_len, GroupService._find_path(starting_point,(x,y), fields, levels, path_len, [])
            queue = queue[1:]
            neighbours = [(path_len + 1, n.positon) for n in fields[x][y].neighbours if n.group_id != starting_group_id
                          and MC['SIZE'] - 1 not in n.positon]
            queue.extend([(l, n) for l, n in neighbours if n not in visited])
        return None, min_path_len, None
