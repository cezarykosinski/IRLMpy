from models import map as m
from constants import MAP_CONTEXT_CONSTANTS as MCC
from constants import ROGUE_CONSTANTS as RC

class MapContext:
    """
    todo
    """
    def __init__(self, id=0, rogue):
        """
        todo
        :param id:
        """
        self.id = id
        self.maps = {}
        self.current_map = None
        self.rogue = rogue

    def start(self, size):
        """
        todo
        :return:
        """
        self.maps.update({(0, 0): m.Map((0, 0), self)})
        map_response = self.access_map((0, 0))
        

    def start_with_rogue(self, rogue):
        """
        todo
        :return:
        """
        self.maps.update({(0, 0): m.Map((0, 0), self)})
        self.access_map((0, 0))
        map_response = self.current_map.place_rogue(rogue.torch_size)
        while rogue.torch_size:
            rogue_response = self.rogue.make_move(map_response)
            map_response = self.current_map.make_move(rogue_response)

    def access_map(self, map_id): #, position = None):
        """
        todo
        :param map_id:
        :return:
        """
        self.current_map = self.maps.get((0, 0))
        self.generate_neighbours()

    def generate_neighbours(self):
        """
        todo
        :return:
        """
        current_id = self.current_map.id
        map_keys = self.maps.keys()
        mid_up_left, mid_up, mid_up_right, mid_left, mid_right, mid_down_left, mid_down, mid_down_right = [(current_id[0] + x, current_id[1] + y) for x,y in [(-1, 1), (0, 1), (1,1), (-1, 0), (1, 0), (-1,-1), (0, -1), (1,-1)]]

        if mid_up_left not in map_keys:
            self.maps.update({mid_up: m.Map((mid_up_left, self))})
        if mid_up not in map_keys:
            self.maps.update({mid_up: m.Map((mid_up, self))})
        if mid_up_right not in map_keys:
            self.maps.update({mid_up: m.Map((mid_up_right, self))})
        if mid_left not in map_keys:
            self.maps.update({mid_left: m.Map((mid_left, self))})
        if mid_right not in map_keys:
            self.maps.update({mid_right: m.Map((mid_right, self))})
        if mid_down_left not in map_keys:
            self.maps.update({mid_up: m.Map((mid_down_left, self))})
        if mid_down not in map_keys:
            self.maps.update({mid_up: m.Map((mid_down, self))})
        if mid_down_right not in map_keys:
            self.maps.update({mid_down: m.Map((mid_down_right, self))})

#tried to generalize following methods, however it was saving only 1 line
    def get_northeast_bound(self, pos):
        new_pos = pos[0] + 1, pos[1] - 1
        if new_pos in self.maps.keys():
            bound = self.maps[new_pos].get_southwest_bound()
        else:
            bound = MCC['DEFAULT_CORNER_BOUND']
        return bound    

    def get_north_bound(self, pos):
        new_pos = pos[0] + 1, pos[1]
        if new_pos in self.maps.keys():
            bound = self.maps[new_pos].get_south_bound()
        else:
            bound = MCC['DEFAULT_HORIZONTAL_BOUND']
        return bound    

    def get_northwest_bound(self, pos):
        new_pos = pos[0] + 1, pos[1] + 1
        if new_pos in self.maps.keys():
            bound = self.maps[new_pos].get_southeast_bound()
        else:
            bound = MCC['DEFAULT_CORNER_BOUND']
        return bound    


    def get_east_bound(self, pos):
        new_pos = pos[0], pos[1] + 1
        if new_pos in self.maps.keys():
            bound = self.maps[new_pos].get_west_bound()
        else:
            bound = MCC['DEFAULT_VERTICAL_BOUND']
        return bound    
    def get_west_bound(self, pos):
        new_pos = pos[0], pos[1] - 1
        if new_pos in self.maps.keys():
            bound = self.maps[new_pos].get_east_bound()
        else:
            bound = MCC['DEFAULT_VERTICAL_BOUND']
        return bound    


    def get_southeast_bound(self, pos):
        new_pos = pos[0] - 1, pos[1] + 1
        if new_pos in self.maps.keys():
            bound = self.maps[new_pos].get_northeast_bound()
        else:
            bound = MCC['DEFAULT_CORNER_BOUND']
        return bound    

    def get_south_bound(self, pos):
            new_pos = pos[0] - 1, pos[1]
            if new_pos in self.maps.keys():
                bound = self.maps[new_pos].get_northeast_bound()
            else:
                bound = MCC['DEFAULT_CORNER_BOUND']
            return bound    

    def get_southwest_bound(self, pos):
            new_pos = pos[0] - 1, pos[1] - 1
            if new_pos in self.maps.keys():
                bound = self.maps[new_pos].get_northeast_bound()
            else:
                bound = MCC['DEFAULT_CORNER_BOUND']
            return bound    

    def display(self):
        pass
