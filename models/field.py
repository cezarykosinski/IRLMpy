from constants import GROUP_CONSTANTS as gc
from constants import FIELD_CONSTANTS as fc


class Field:
    """
    todo
    """
    def __init__(self, x, y):
        self.position = x, y
        self.value = fc['default_value']
        self.groupId = gc['noGroupId']
        self.neighbours_values = []
        self.neighbours_positions = []

    def calculate(self):
        """
        todo
        :return:
        """
        num_of_considered_neighbours = sum([len(list(filter(lambda x: not(x is None), row))) for row in self.neighbours_values])
        
        waged_neighbours_values = [sum([n * w if n else 0 for (n, w) in list(zip(nrow, wrow))])
                                   for (nrow, wrow) in list(zip(self.neighbours_values, fc['wages']))]
        result = sum(waged_neighbours_values) / num_of_considered_neighbours

        self.value = 1 if result > fc['condition'] else 0 #NOT GENERIC

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

