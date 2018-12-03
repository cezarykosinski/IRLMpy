import functools

from constants import MAP_CONTEXT_CONSTANTS as MCC
from src.maps import map as m
from functools import cmp_to_key

class MapContext:
    """
    todo
    """

    def __init__(self, id=0, rogue=None):
        """
        todo
        :param id:
        """
        self.id = id
        self.maps = {}
        self.current_map = None
        self.rogue = rogue

    def start(self):
        """
        todo
        :return:
        """
        self.maps.update({(0, 0): m.Map((0, 0), self)})
        self.access_map((0, 0))

    @staticmethod
    def mid_comp(m1, m2):
        x1, y1 = m1
        x2, y2 = m2
        if x1 < x2 or y1 > y2:
            return 1
        return -1

    @staticmethod
    def get_ranges(start_position, direction, mid):
        start_x, start_y = start_position
        dir_x, dir_y = direction
        dest_x, dest_y = (start_x + dir_x, start_y + dir_y)
        size = MCC['SIZE']
        ranges_list = []

        if dest_x > size:
            dest_x = size - 1
            nid = mid[0], mid[1] - 1
            dir_x -= size - start_x - 1
            ranges_list += MapContext.get_ranges((0, start_y), (dir_x, dir_y), nid)
        elif dest_x < 0:
            dest_x = 0
            nid = mid[0], mid[1] + 1
            dir_x += start_x
            ranges_list += MapContext.get_ranges((size - 1, start_y), (dir_x, dir_y), nid)
        if dest_y > size:
            dest_y = size - 1
            nid = mid[0] + 1, mid[1]
            dir_y -= size - start_y - 1
            ranges_list += MapContext.get_ranges((start_x, 0), (dir_x, dir_y), nid)
        elif dest_y < 0:
            dest_y = 0
            nid = mid[0] - 1, mid[1]
            dir_y += start_y
            ranges_list += MapContext.get_ranges((start_x, size - 1), (dir_x, dir_y), nid)

        is_positive = lambda x: x > 0

        if is_positive(dir_x):
            if is_positive(dir_y):
                pass
            else:
                start_y, dest_y = dest_y, start_y
        else:
            if is_positive(dir_y):
                start_x, dest_x = dest_x, start_x
            else:
                start_x, dest_x = dest_x, start_x
                start_y, dest_y = dest_y, start_y

        return ranges_list + [{"start": (start_x, start_y), "destination": (dest_x, dest_y), "id": mid}]

    @staticmethod
    def get_field_surroundings_ranges(pos, torch_size, map_id):
        ranges = []
        for ts in [(torch_size, torch_size),
                   (torch_size, -torch_size),
                   (-torch_size, -torch_size),
                   (-torch_size, torch_size)]:
            ranges += MapContext.get_ranges(pos, ts, map_id)
        result = {}
        for rng in ranges:
            result[rng['id']] = {i: rng[i] for i in rng if i != 'id'}
        return result

    @staticmethod
    def get_field_surroundings_values(map_field_ranges):
        sorted_ids = sorted(map_field_ranges.keys(), key=cmp_to_key(MapContext.mid_comp))
        rows_values = {}
        for id in sorted_ids:
            start, dest = map_field_ranges[id].values()
            vals = self.maps[id].get_field_values_in_range(start, dest)
            if rows_values[id[1]]:
                rows_values[id[1]] = [row + vrow for row, vrow in zip(rows_values[id[1]], vals)]
            else:
                rows_values[id[1]] = vals
        return functools.reduce(lambda x, y: x+y, rows_values, [])

    def start_with_rogue(self, rogue):
        """
        todo
        :return:
        """
        self.maps.update({(0, 0): m.Map((0, 0), self)})
        self.access_map((0, 0))
        rogue_init_data = rogue.get_init_data()
        map_response = self.current_map.make_move((rogue_init_data, self.current_map.get_starting_field))
        while rogue.torch_size:
            map_field_ranges = MapContext.get_field_surroundings_ranges(map_response['position'], rogue.torch_size,
                                                                        self.current_map.id)
            for rng in map_field_ranges:
                self.access_map(rng['id'])
            map_response['visible_surroundings'] = self.get_field_surroundings_values(map_field_ranges)
            rogue_response = rogue.make_move(map_response)
            map_response = self.current_map.make_move(rogue_response)

    def access_map(self, map_id):
        """
        todo
        :param map_id:
        :return:
        """
        # self.current_map = self.maps[map_id]  # ?
        self.generate_neighbours(map_id)
        # bounds = {'northbound': self.get_north_bound(map_id)}
        # self.current_map.access(bounds)
        self.current_map.access()

    def generate_neighbours(self, mid):
        """
        todo
        :return:
        """

        map_keys = self.maps.keys()
        potential_keys = [(mid[0] + x, mid[1] + y) for x, y in
                          [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)]]
        for key in potential_keys:
            if key not in map_keys:
                self.maps.update({key: m.Map(key, self)})

    # tried to generalize following methods, however it was saving only 1 line
    def get_northeast_bound(self, p):
        new_pos = p[0] + 1, p[1] + 1
        bound = self.maps[new_pos].get_southwest_bound()
        return bound

    def get_north_bound(self, pos):
        new_pos = pos[0], pos[1] + 1
        bound = self.maps[new_pos].get_south_bound()
        return bound

    def get_northwest_bound(self, pos):
        new_pos = pos[0] - 1, pos[1] + 1
        bound = self.maps[new_pos].get_southeast_bound()
        return bound

    def get_east_bound(self, pos):
        new_pos = pos[0] + 1, pos[1]
        bound = self.maps[new_pos].get_west_bound()
        return bound

    def get_west_bound(self, pos):
        new_pos = pos[0] - 1, pos[1]
        bound = self.maps[new_pos].get_east_bound()
        return bound

    def get_southeast_bound(self, pos):
        new_pos = pos[0] + 1, pos[1] - 1
        bound = self.maps[new_pos].get_northeast_bound()
        return bound

    def get_south_bound(self, pos):
        new_pos = pos[0], pos[1] - 1
        bound = self.maps[new_pos].get_north_bound()
        return bound

    def get_southwest_bound(self, pos):
        new_pos = pos[0] - 1, pos[1] - 1
        bound = self.maps[new_pos].get_northeast_bound()
        return bound

    def display(self):
        pass
