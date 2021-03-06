from functools import reduce, partial
from random import seed, randint

from constants import FIELD_CONSTANTS as FC
from config import GROUP_CONFIG as GC, MAP_CONFIG as MCONFIG, FIELD_CONFIG as FCONFIG
from constants import MAP_CONSTANTS as MCONSTANTS
from src.maps.field import Field
from src.maps.group import Group


class Map:
    """
    todo
    """

    def __init__(self, ctx, id =(0,0)):
        self.id = id
        self._context = ctx

        self.is_accessed = False
        self._groups = []
        self._fields = [[Field(fi, fj, self.id)
                         for fj in range(MCONFIG['SIZE'])]
                        for fi in range(MCONFIG['SIZE'])]
        self._generate_noise()

    # do service'u
    def _generate_noise(self):
        """
        todo
        :return:
        """
        fields_no = MCONFIG['SIZE'] ** 2
        amount_of_noise = 0
        seed(self._context.id * 100 + self.id[0] * 10 + self.id[1])

        while (amount_of_noise / fields_no) < MCONSTANTS['INITIAL_RATIO']:
            x = randint(0, MCONFIG['SIZE'] - 1)
            y = randint(0, MCONFIG['SIZE'] - 1)
            if self._fields[x][y].value == FCONFIG['DEFAULT_VALUE']:
                self._fields[x][y].value = FCONFIG['ROCK']
                amount_of_noise += 1

    def _set_fields_neighbours(self):
        """
        todo
        :return:
        """
        left_fields = self._northwestbound + self._westbound + self._southwestbound
        mid_fields = self._northbound + self._fields + self._southbound
        right_fields = self._northeastbound + self._eastbound + self._southeastbound
        all_fields = [i + j + g for i, j, g in zip(left_fields, mid_fields, right_fields)]
        for row in self._fields:
            for f in row:
                f.set_neighbours(all_fields)

    def _set_fields_neighbours_values(self):
        """
        todo
        :return:
        """
        for row in self._fields:
            for f in row:
                f.set_neighbours_values()

    def calculate(self):
        """
        todo
        :return:
        """
        self._set_fields_neighbours_values()
        for i in range(MCONSTANTS['NUMBER_OF_ITERATIONS']):
            for row in self._fields:
                for f in row:
                    f.calculate()
            self._set_fields_neighbours_values()

    # noinspection PyAttributeOutsideInit
    def commit(self):
        """
        todo
        :return:
        """
        self.is_accessed = True
        # bounds can be passed as a parameters of start function
        self._northeastbound = self._context.get_northeast_bound(self.id)
        self._northbound = self._context.get_north_bound(self.id)
        self._northwestbound = self._context.get_northwest_bound(self.id)
        self._westbound = self._context.get_west_bound(self.id)
        self._southwestbound = self._context.get_southwest_bound(self.id)
        self._southbound = self._context.get_south_bound(self.id)
        self._southeastbound = self._context.get_southeast_bound(self.id)
        self._eastbound = self._context.get_east_bound(self.id)

        self._set_fields_neighbours()
        self.calculate()

        # self.group_fields()

    def display(self):
        """
        todo
        :return:
        """
        for row in self._fields:
            row_display = ""
            for f in row:
                row_display += f.display()
            print(row_display)

    def display_groups(self):
        """
        todo
        :return:
        """
        for row in self._fields:
            row_display = ""
            for f in row:
                row_display += f.display_group()
            print(row_display)

    def to_string(self):
        """
        todo
        :return:
        """
        output = []
        for row in self._fields:
            row_display = ""
            for f in row:
                row_display += f.display()
            output += [row_display]
        return output

####################
# BOUNDS FUNCTIONS #
####################

    def get_northeast_bound(self):
        """
        todo
        :return:
        """
        return [row[MCONFIG['SIZE'] - FC['NEIGHBOURHOOD_SIZE']:] for row in self._fields[:FC['NEIGHBOURHOOD_SIZE']]]

    def get_north_bound(self):
        """
        todo
        :return:
        """
        return self._fields[:FC['NEIGHBOURHOOD_SIZE']]

    def get_northwest_bound(self):
        """
        todo
        :return:
        """
        return [row[:FC['NEIGHBOURHOOD_SIZE']] for row in self._fields[:FC['NEIGHBOURHOOD_SIZE']]]

    def get_west_bound(self):
        """
        todo
        :return:
        """
        return [row[:FC['NEIGHBOURHOOD_SIZE']] for row in self._fields]

    def get_southwest_bound(self):
        """
        todo
        :return:
        """
        return [row[:FC['NEIGHBOURHOOD_SIZE']] for row in self._fields[MCONFIG['SIZE'] - FC['NEIGHBOURHOOD_SIZE']:]]

    def get_south_bound(self):
        """
        todo
        :return:
        """
        return self._fields[MCONFIG['SIZE'] - FC['NEIGHBOURHOOD_SIZE']:]

    def get_southeast_bound(self):
        """
        todo
        :return:
        """
        return [row[MCONFIG['SIZE'] - FC['NEIGHBOURHOOD_SIZE']:] for row in
                self._fields[MCONFIG['SIZE'] - FC['NEIGHBOURHOOD_SIZE']:]]

    def get_east_bound(self):
        """
        todo
        :return:
        """
        return [row[MCONFIG['SIZE'] - FC['NEIGHBOURHOOD_SIZE']:] for row in self._fields]

#############################
# EVALUATION FUNCTIONS #
#############################

    def get_no_of_floors(self):
        func = partial(filter, (lambda f: f.value == FCONFIG['FLOOR']))
        return reduce(lambda x, y: x + y, map(lambda row: len(list(func(row))), self._fields), 0)

    def group_fields(self):
        """
        todo
        :return:
        """
        for row in self._fields:
            for f in row:
                if f.value == FCONFIG['FLOOR'] and f.group_id == GC['NO_GROUP_ID']:
                    new_group = Group(f)
                    new_group.find_rest_of_the_fields(self._fields)
                    new_group.count_exits()
                    self._groups.append(new_group)

    def get_no_of_groups_with_less_than_two_exits(self):
        return reduce(lambda curval, g: curval + [0, 1][g.no_of_exits < 2], self._groups, 0)

    def get_no_of_groups_with_at_least_two_exits(self):
        return reduce(lambda curval, g: curval + [0, 1][g.no_of_exits > 2], self._groups, 0)

    def get_horizontal_path_lengths_extrema(self):
        max_length = 0
        min_length = MCONFIG['SIZE']
        for row in self._fields:
            curr_len = 0
            for f in row:
                if f.value == FCONFIG['FLOOR']:
                    curr_len += 1
                else:
                    if curr_len > max_length:
                        max_length = curr_len
                    if curr_len < min_length:
                        min_length = curr_len
                    curr_len = 0
        return min_length, max_length

    def get_vertical_path_lengths_extrema(self):
        max_length = 0
        min_length = MCONFIG['SIZE']
        for i in range(MCONFIG['SIZE']):
            column = map(lambda r: r[i], self._fields)
            curr_len = 0
            for f in column:
                if f.value == FCONFIG['FLOOR']:
                    curr_len += 1
                else:
                    if curr_len > max_length:
                        max_length = curr_len
                    if curr_len < min_length:
                        min_length = curr_len
                    curr_len = 0
        return min_length, max_length

    def get_paths_lengths_extrema(self):
        horizontal = self.get_horizontal_path_lengths_extrema()
        vertical = self.get_vertical_path_lengths_extrema()
        return min(horizontal[0], vertical[0]), max(horizontal[1], vertical[1])

########################
# SIMULATION FUNCTIONS #
########################

    def get_field_values_in_range(self, start, dest):
        start_x, start_y = start
        dest_x, dest_y = dest
        output_fields = map(lambda row: list(map(lambda e: e.value, row[start_x:dest_x])), self._fields[start_y:dest_y])
        return list(output_fields)

    def get_starting_field(self):
        return self._groups[0].starting_field_position

    def apply_move(self, rogue_data):
        px, py = rogue_data['position']
        mx, my = rogue_data['move']
        size = MCONFIG['SIZE']

        np_x, np_y = ((px + mx) % size, (py + my) % size)
        if self._fields[np_x][np_y].is_rock():
            rogue_data['position'] = (np_x, np_y)
        return rogue_data
