from service.field import FieldService
from constants import GROUP_CONSTANTS as GC
from constants import FIELD_CONSTANTS as FC


class Field:
    """
    todo
    """
    def __init__(self, x, y):
        self.position = x, y
        self.value = FC['DEFAULT_VALUE']
        self.groupId = GC['NO_GROUP_ID']
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
        fs = FieldService
        num_of_considered_neighbours = fs.count_considered_neighbours(self.neighbours_values)
        waged_neighbours_values = fs.get_values_of_waged_neighbours(self.neighbours_values)

        result = sum(waged_neighbours_values) / num_of_considered_neighbours

        self.value = FC['ROCK'] if result > FC['CONDITION'] else FC['FLOOR'] #NOT GENERIC

    def move(self, rogue_data):
        if self.value == FC['ROCK']:
            return None #lame... maybe something else?
        else:
            field_info = #to precise
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
        return [str(self.groupId), "#"][self.value] + " "
