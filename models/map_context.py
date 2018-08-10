from models import map as m


class MapContext:
    """
    todo
    """
    def __init__(self, id=0):
        """
        todo
        :param id:
        """
        self.id = id
        self.maps = {}
        self.current_map = None

    def start(self):
        """
        todo
        :return:
        """
        self.maps.update({(0, 0): m.Map((0, 0), self)})
        self.access_map((0, 0))

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

        if not mid_up_left in map_keys:
            self.maps.update({mid_up: m.Map((mid_up, self, self.current_map.get_south_east_bound))})
        if not mid_up in map_keys:
            self.maps.update({mid_up: m.Map((mid_up, self, self.current_map.get_south_bound))})
        if not mid_up_right in map_keys:
            self.maps.update({mid_up: m.Map((mid_up, self, self.current_map.get_south_west_bound))})
        if not mid_left in map_keys:
            self.maps.update({mid_left: m.Map((mid_left, self, self.current_map.get_east_bound))})
        if not mid_right in map_keys:
            self.maps.update({mid_right: m.Map((mid_right, self, self.current_map.get_west_bound))})
        if not mid_down_left in map_keys:
            self.maps.update({mid_up: m.Map((mid_up, self, self.current_map.get_north_east_bound))})
        if not mid_down in map_keys:
            self.maps.update({mid_up: m.Map((mid_up, self, self.current_map.get_north_bound))})
        if not mid_down_right in map_keys:
            self.maps.update({mid_down: m.Map((mid_down, self, self.current_map.get_north_west_bound))})

    def set_northeastbound(self, pos):
    def set_northbound(self, pos):
    def set_northwestbound(self, pos):

    def set_eastbound(self, pos):
    def set_westbound(self, pos):

    def set_southeastbound(self, pos):
    def set_southbound(self, pos):
    def set_southwestbound(self, pos):

