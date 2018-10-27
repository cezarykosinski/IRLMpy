from models import map as m
from constants import MAP_CONTEXT_CONSTANTS as MCC, ROGUE_CONSTANTS as RC


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

       def get_field_surroundings_ranges(self, param, torch_size):

    def get_field_surroundings_values(self, map_field_ranges):
        for rng, id in map_field_ranges:
            #take rng from map of given id

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
               map_field_ranges = get_field_surroundings_ranges(map_response['position'], rogue.torch_size)
               for _, id in map_field_ranges:
                   self.access_map(id)
               map_response['visible_surroundings'] = self.get_field_surroundings_values(map_field_ranges)
               rogue_response = rogue.make_move(map_response)
               map_response = self.current_map.make_move(rogue_response)

               for m_id in affected_maps_ids:

    def access_map(self, map_id):
        """
        todo
        :param map_id:
        :return:
        """
        self.current_map = self.maps[map_id]
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
