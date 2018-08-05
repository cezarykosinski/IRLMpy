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
        self.neighbours_positions = []

    def calculate(self):
        """
        todo
        :return:
        """
        fs = FieldService
        num_of_considered_neighbours = fs.count_considered_neighbours(self.neighbours_values)
        waged_neighbours_values = fs.get_values_of_waged_neighbours(self.neighbours_values)

        result = sum(waged_neighbours_values) / num_of_considered_neighbours

        self.value = 1 if result > FC['CONDITION'] else 0 #NOT GENERIC

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
