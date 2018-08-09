from constants import GROUP_CONSTANTS as GC
from constants import FIELD_CONSTANTS as FC


class FieldService:

    @staticmethod
    def count_considered_neighbours(neighbours_values):
        """
        todo : docs and logic refactor
        :param neighbours_values:
        :return:
        """
        return sum([len(list(filter(lambda x: not(x is None), row))) for row in neighbours_values])

    @staticmethod
    def get_values_of_waged_neighbours(neighbours_values):
        """
        todo
        :param neighbours_values:
        :return:
        """
        return [sum([n * w if n else 0 for (n, w) in list(zip(nrow, wrow))])
                for (nrow, wrow) in list(zip(neighbours_values, FC['WAGES']))]
