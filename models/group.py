import random
import math

from constants import MAP_CONSTANTS as MC, FIELD_CONSTANTS as FC, GROUP_CONSTANTS as GC
from service.group import GroupService


class Group:
    """
    todo
    """
    LASTEST_ID = 0

    # todo : discuss if group obj should contains field's obj's
    def __init__(self, starting_field):
        """
        todo
        :param starting_field:
        """
        self.id = Group.LASTEST_ID
        self.starting_field_position = starting_field.position
        self._boarder = []
        self._fields = []
        Group.LASTEST_ID += 1
    
    def find_rest_of_the_fields(self, field):
        """
        todo
        :param fields:
        :return:
        """
        queue = [self.starting_field_position]
        self._fields.append(GroupService.assign_group_to_fields(self.id, queue, field))

    def update_the_boarders(self):
        """
        todo
        :return:
        """
        self._boarder = [f.position for f in self._fields if FC['ROCK'] in f.neighboursValues]

    def __has_wayout_already(self):
        """
        todo
        :return:
        """
        return len([pos for pos in self._boarder if (MC['SIZE'] - 1 in pos)]) > 0

    def assign_new_fields(self, positions, fields):
        self._fields.extend(positions)
        self._boarder.extend(positions)
        for position in positions:
            x, y = position
            fields[x][y].group_id = self.id

    def group_connecting(self, fields):
        """
        todo
        :param fields:
        :return:
        """
        min_path = MC['SIZE']**2
        min_points_pair = None
        borders_last_index = len(self._boarder) - 1
        n_samples = math.ceil(GC['EXITS_RATIO'] * borders_last_index)
        exits_indexes = random.sample(range(borders_last_index), n_samples)
        for exit_point in [self._boarder[index] for index in exits_indexes]:
            points_pair, min_path = GroupService.find_closest_group(exit_point, fields, min_path)
            min_points_pair = points_pair or min_points_pair
        if min_points_pair:
            path = GroupService.find_path(min_points_pair, fields)
            GroupService.drill_path(path, fields)
            self.assign_new_fields(path, fields)

            
            
            







        # self.update_the_boarders()
        # if not self.__has_wayout_already():
        #     mindist = MC['SIZE']
        #     mingroup_id = self.id
        #     minsource = self.starting_field_position
        #     minendpoint = self.starting_field_position
        #     for pos in self._boarder:
        #         distance, group_id, endpoint = GroupService.closest_group_with_wayout(self.id, fields, pos)
        #         if distance < mindist:
        #             mindist, mingroup_id, minsource, minendpoint = distance, group_id, f, endpoint
        #     GroupService.drill_wayout(fields, minsource, minendpoint)
