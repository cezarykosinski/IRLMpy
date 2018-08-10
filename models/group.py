from constants import MAP_CONSTANTS
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
        self.__starting_field_position = starting_field.position
        self.__boarders = []
        self.__fields = []
        Group.LASTEST_ID += 1
    
    def find_rest_of_the_fields(self, fields):
        """
        todo
        :param fields:
        :return:
        """
        queue = [self.__starting_field_position]
        self.__fields.append(GroupService.assign_group_to_fields(self.id, queue, fields))

    def update_the_boarders(self):
        """
        todo
        :return:
        """
        self.__boarders = [f.position for f in self.__fields if FC['ROCK'] in f.neighboursValues]

    def __has_wayout_already(self):
        """
        todo
        :return:
        """
        return len([pos for pos in self.__boarders if (MAP_CONSTANTS['SIZE'] - 1 in pos)]) > 0

    def wayout_providing(self, fields):
        """
        todo
        :param fields:
        :return:
        """
        self.update_the_boarders()
        if not self.__has_wayout_already():
            mindist = MAP_CONSTANTS['SIZE'] 
            mingroup_id = self.id
            minsource = self.__starting_field_position
            minendpoint = self.__starting_field_position
            for pos in self.__boarders:
                distance, group_id, endpoint = GroupService.closest_group_with_wayout(self.id, fields, pos)
                if distance < mindist:
                    mindist, mingroup_id, minsource, minendpoint = distance, group_id, f, endpoint
            GroupService.drill_wayout(fields, minsource, minendpoint)
