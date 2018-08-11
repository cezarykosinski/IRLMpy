import models.map_context as mc
from constants import ROGUE_CONSTANTS as RC

class Rogue:
    """
    todo
    """
    def __init__(self):
        self.torch_size = RC['MAX_TORCH_SIZE']
        self.torch_time_left = RC['TORCH_BURN_TIME']
        self.position = (0,0)
        self.visible_surroundings = []
    
    def get_data(self):
        return {'torch_size': self.torch_size,
                'position': self.position,
                ''}

    def make_move(self, map_response):
        #to precise
        
