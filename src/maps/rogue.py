import random

from constants import ROGUE_CONSTANTS as RC


class DefaultRogue:
    """
    todo
    """

    def __init__(self, position=(0, 0), map_id=(0, 0)):
        self.map_id = map_id
        self.torch_size = RC['MAX_TORCH_SIZE']
        self.torch_time_left = RC['TORCH_BURN_TIME']
        self.position = position
        self.visible_surroundings = []

    def get_init_data(self):
        return {'torch_size': self.torch_size,
                'position': self.position,
                'move': (0, 0)}

    def make_move(self, map_response):
        self.position = map_response['position']
        self.visible_surroundings = map_response['visible_surroundings']
        self.torch_time_left -= 1
        if self.torch_time_left <= 0:
            self.torch_time_left = RC['TORCH_BURN_TIME']
            self.torch_size -= 1

        return {'map_id': self.map_id,
                'position': self.position,
                'move': self.make_decision(),
                'torch_size': self.torch_size}

    def make_decision(self):
        for r in self.visible_surroundings:
            print(r)
        decision = input('make decision')
        while not (self._handle(decision)):
            decision = input('make decision')
        return self._handle(decision)

    def _handle(self, decision):
        if decision == 'up':
            return 1, 0
        if decision == 'down':
            return -1, 0
        if decision == 'right':
            return 0, 1
        if decision == 'left':
            return 0, -1
        return False


class RandomRogue(DefaultRogue):
    def make_decision(self):
        return random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])

class SmartRogue(DefaultRogue):
    def __init__(self, position=(0, 0), map_id=(0, 0)):
        self.map_id = map_id
        self.torch_size = RC['MAX_TORCH_SIZE']
        self.torch_time_left = RC['TORCH_BURN_TIME']
        self.position = position
        self.visible_surroundings = []
        self.direction = None

    def make_decision(self):
        if self.direction:
            pass
        else
            
