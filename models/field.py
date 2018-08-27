from constants import GROUP_CONSTANTS as GC
from constants import FIELD_CONSTANTS as FC


class Field:
    """
    Elementary object

    """
    def __init__(self, x, y):
        self.position = x, y
        self.value = FC['DEFAULT_VALUE']
        self.group_id = GC['NO_GROUP_ID']
        self.neighbours_values = []
        self.neighbours = []

    def set_neighbours(self, fields):
        
        mns = FC['MOORE_NEIGHBOURHOOD_SIZE']
        x, y = [i + mns for i in self.position]

        self.neighbours = [fields[x+i][y+j]
                           for j in range(-mns, mns+1)
                           for i in range(-mns, mns+1)]

    def set_neighbours_values(self):
        self.neighbours_values = [n.value for n in self.neighbours]

    def calculate(self):
        """
        todo
        :return:
        """
        num_of_considered_neighbours = (FC['MOORE_NEIGHBOURHOOD_SIZE']*2 + 1)**2
        waged_neighbours_values = [sum([n * w if n else 0 for (n, w) in list(zip(self.neighbours_values, FC['WAGES']))])]

        result = sum(waged_neighbours_values) / num_of_considered_neighbours

        self.value = FC['ROCK'] if result > FC['CONDITION'] else FC['FLOOR'] #NOT GENERIC

    def move(self, rogue_data):
        if self.value == FC['ROCK']:
            return None 
            #lame... maybe something else to return?
        else:
            field_info = {'visible_surrounding': self.get_surrounding(rogue_data[''])}
            return field_info

    def display(self):
        """
        todo
        :return:
        """
        return [".", "#"][self.value] + " "

    def display_group(self):
        """
        todo
        :return:
        """
        return [str(self.group_id), "#"][self.value] + " "
