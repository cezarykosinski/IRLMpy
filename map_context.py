import map as m

class MapContext:
    
    def __init__(self, id = 0):
        self.id = id
        self.maps = {}
        self.current_map = None

    def start(self):
        self.maps.update({(0,0): m.Map((0,0), self)})
        self.accessMap((0,0))

    def accessMap(self, map_id): #, position = None):
        self.current_map = self.maps.get((0,0))
        self.generateNeighbours()

    def generateNeighbours(self)
        current_id = self.current_map.id
        mid_up, mid_down, mid_left, mid_right = [(current_id[0] + x, current_id[1] + y) for x,y in [(0, 1), (0, -1), (-1, 0), (1, 0)]]

        if not mid_up in self.maps.keys:
            self.maps.update({mid_up: m.Map((mid_up, self, self.maps.get(current_id).getSouthBound))})
        if not mid_down in self.maps.keys:
            self.maps.update({mid_down: m.Map((mid_down, self, self.maps.get(current_id).getNorthBound))})
        if not mid_left in self.maps.keys:
            self.maps.update({mid_left: m.Map((mid_left, self, self.maps.get(current_id).getEastBound))})
        if not mid_right in self.maps.keys:
            self.maps.update({mid_right: m.Map((mid_right, self, self.maps.get(current_id).getWestBound))})

