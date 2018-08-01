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
        mid_up, mid_down, mid_left, mid_right = [(current_id[0] + x, current_id[1] + y) for x, y in [(0, 1), (0, -1), (-1, 0), (1, 0)]]

        # todo .keys() .get() to vars ?
        # todo Map() not enough params
        if mid_up not in self.maps.keys():
            self.maps.update({mid_up: m.Map((mid_up, self, self.maps.get(current_id).get_south_bound))})
        if mid_down not in self.maps.keys():
            self.maps.update({mid_down: m.Map((mid_down, self, self.maps.get(current_id).get_north_bound))})
        if mid_left not in self.maps.keys():
            self.maps.update({mid_left: m.Map((mid_left, self, self.maps.get(current_id).get_east_bound))})
        if mid_right not in self.maps.keys():
            self.maps.update({mid_right: m.Map((mid_right, self, self.maps.get(current_id).get_west_bound))})
