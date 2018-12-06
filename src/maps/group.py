import random
import math

from constants import MAP_CONSTANTS as MC, FIELD_CONSTANTS as FC, GROUP_CONSTANTS as GC
from src.service import GroupService


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
        self._border = []
        self._fields = []
        Group.LASTEST_ID += 1
    
    def find_rest_of_the_fields(self, fields):
        """
        todo
        :param fields:
        :return:
        """
        self._fields = Group.assign_group_to_fields(self.id, self.starting_field_position, fields)
        self.update_the_border(fields)

    def update_the_border(self, fields):
        """
        todo
        :return:
        """
        self._border = [(x,y) for x, y in self._fields if FC['ROCK'] in fields[x][y].neighbours_values or MC['SIZE']-1 in fields[x][y].position or 0 in fields[x][y].position]

    def has_wayout_already(self):
        """
        todo
        :return:
        """
        return len([pos for pos in self._border if MC['SIZE']-1 in pos]) > 0

    @staticmethod
    def assign_group_to_fields(group_id, start_pos, fields):
        queue = [start_pos]
        assigned_fields = []
        map_id = fields[start_pos[0]][start_pos[1]].map_id
        while queue:
            x, y = queue.pop()
            assigned_fields.append((x,y))
            fields[x][y].group_id = group_id
            for n in fields[x][y].neighbours:
                if n.value == FC['FLOOR'] and n.map_id == map_id and n.group_id == GROUP_CONSTANTS['NO_GROUP_ID'] and n.position not in assigned_fields:
                    queue.append(n.position)
        return assigned_fields