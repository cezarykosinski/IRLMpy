import models.map_context as mc
from constants import ROGUE_CONSTANTS as RC

class Rogue:
    """
    todo
    """
    def __init__(self, position=(0, 0), map_id=(0, 0)):
        self.map_id = map_id
        self.torch_size = RC['MAX_TORCH_SIZE']
        self.torch_time_left = RC['TORCH_BURN_TIME']
        self.position = position
        self.visible_surroundings = []
    
    def get_data(self):
        return {'torch_size': self.torch_size,
                'position': self.position
                'move': (0, 0)
                }

    def make_move(self, map_response):
        self.position = map_response['position']
        self.visible_surroundings = map_response['surroundings']
        self.torch_time_left -= 1
        if self.torch_time_left >= 0:
            self.torch_time_left = RC['TORCH_BURN_TIME']
            self.torch_size -= 1

        response = {'map_id': self.map_id,
                    'position': self.position,
                    'move': self.make_decision(),
                    'torch_size': self.torch_size}

        return response

    def make_decision(self):
        pass

