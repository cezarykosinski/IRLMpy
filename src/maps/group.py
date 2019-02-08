from config import GROUP_CONFIG as GC, FIELD_CONFIG as FC, MAP_CONFIG as MC
from itertools import chain

class Group:
    """
    todo
    """
    LATEST_ID = 0

    def __init__(self, starting_field):
        """
        todo
        :param starting_field:
        """
        self.id = Group.LATEST_ID
        self.starting_field_position = starting_field.position
        self.no_of_exits = 0
        self._border = []
        self._fields_positions = []
        Group.LATEST_ID += 1

    def update_the_border(self, fields):
        """
        todo
        :return:
        """
        self._border = [(x,y) for x, y in self._fields_positions
                        if FC['ROCK'] in fields[x][y].neighbours_values
                        or MC['SIZE'] - 1 in fields[x][y].position
                        or 0 in fields[x][y].position]

    def count_exits(self):
        is_left_exit = 0 in map(lambda f: f[1], self._border)
        is_right_exit = MC['SIZE'] in map(lambda f: f[1], self._border)
        is_top_exit = 0 in map(lambda f: f[0], self._border)
        is_bottom_exit = MC['SIZE'] in map(lambda f: f[0], self._border)
        return [is_left_exit, is_right_exit, is_top_exit, is_bottom_exit].count(True)

    def assign_group_to_fields(self, fields):
        start_pos_x, start_pos_y = self.starting_field_position
        queue = [(start_pos_x, start_pos_y)]
        assigned_fields = []
        map_id = fields[start_pos_x][start_pos_y].map_id
        while queue:
            x, y = queue.pop()
            assigned_fields.append((x,y))
            fields[x][y].group_id = self.id
            for n in list(chain(*fields[x][y].neighbours.values())):
                if n.value == FC['FLOOR'] and n.map_id == map_id and n.group_id == GC['NO_GROUP_ID']: #and n.position not in assigned_fields:
                    n.group_id = self.id
                    queue.append(n.position)
        return assigned_fields

    def find_rest_of_the_fields(self, fields):
        """
        todo
        :param fields:
        :return:
        """
        self._fields_positions = self.assign_group_to_fields(fields)
        self.update_the_border(fields)
