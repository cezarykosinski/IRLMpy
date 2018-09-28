from random import seed, randint
from collections import defaultdict

from models.field import Field
from models.group import Group

from constants import FIELD_CONSTANTS as FC
from constants import GROUP_CONSTANTS as GC
from constants import MAP_CONSTANTS as MC


class Map:
    """
    todo
    """
    def __init__(self, id, ctx):
        self.id = id
        self._context = ctx

        self.is_accessed = False
        self._groups = []
        self._fields = [[Field(fi, fj, self.id) 
                        for fj in range(MC['SIZE'])]
                        for fi in range(MC['SIZE'])]
        self._generate_noise()

    # do service'u
    def _generate_noise(self):
        """
        todo
        :return:
        """
        fields_no = MC['SIZE'] ** 2
        amount_of_noise = 0

        seed(self._context.id)

        while (amount_of_noise / fields_no) < MC['INITIAL_RATIO']:
            x = randint(0, MC['SIZE'] - 1)
            y = randint(0, MC['SIZE'] - 1)
            if self._fields[x][y].value == FC['DEFAULT_VALUE']:
                self._fields[x][y].value = FC['ROCK']
                amount_of_noise += 1

    def _set_fields_neighbours(self):
        """
        todo
        :return:
        """
        left_fields = self._northwestbound + self._westbound + self._southwestbound
        mid_fields = self._northbound + self._fields + self._southbound
        right_fields = self._northeastbound + self._eastbound + self._southeastbound
        all_fields = [i+j+g for i, j, g in zip(left_fields, mid_fields, right_fields)]
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

    def get_northeast_bound(self):
        """
        todo
        :return:
        """
        return [row[MC['SIZE'] - FC['NEIGHBOURHOOD_SIZE']:] for row in self._fields[:FC['NEIGHBOURHOOD_SIZE']]]

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
        return [row[:FC['NEIGHBOURHOOD_SIZE']] for row in self._fields[MC['SIZE'] - FC['NEIGHBOURHOOD_SIZE']:]]

    def get_south_bound(self):
        """
        todo
        :return:
        """
        return self._fields[MC['SIZE'] - FC['NEIGHBOURHOOD_SIZE']:]

    def get_southeast_bound(self):
        """
        todo
        :return:
        """
        return [row[MC['SIZE'] - FC['NEIGHBOURHOOD_SIZE']:] for row in self._fields[MC['SIZE'] - FC['NEIGHBOURHOOD_SIZE']:]]

    def get_east_bound(self):
        """
        todo
        :return:
        """
        return [row[MC['SIZE'] - FC['NEIGHBOURHOOD_SIZE']:] for row in self._fields]

    def get_starting_field(self):
        return self._groups[0].starting_field_position

    def calculate(self):
        """
        todo
        :return:
        """
        for i in range(MC['NUMBER_OF_ITERATIONS']):
            self.display()
            print()
            self._set_fields_neighbours_values()
            for row in self._fields:
                for f in row:
                    f.calculate()


    def group_fields(self):
        """
        todo
        :return:
        """
        for row in self._fields:
            for f in row: 
                if f.value == FC['FLOOR'] and f.group_id == GC['NO_GROUP_ID']:
                    new_group = Group(f)
                    new_group.find_rest_of_the_fields(self._fields)
                    self._groups.append(new_group)

    def groups_connecting(self):
        """
        todo
        :return:
        """
        while(len(self._groups) > 1):
            groups= (e for e in sorted(self._groups, key=lambda x: -len(x._border)))
            for group in groups:
                id_a, id_b  = group.group_connecting(self._fields)
                if id_a != id_b:
                    el_b = next(filter(lambda g: g.id == id_b, self._groups))
                    group.assign_new_fields(el_b._fields, self._fields)
                    indx_b = self._groups.index(el_b)
                    del self._groups[indx_b]

    def access(self):
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
        # self.groups_connecting()

    def make_move(self, rogue_data):
        position = rogue_data['position']
        move = rogue_data['move']
        torch_size = rogue_data['torch_size']
        new_pos = (position[0] + move[0], position[1] + move[1])
        if MC['SIZE'] - torch_size not in new_pos and torch_size - 1 not in new_pos:
           # [f.values]
           field_info = self._fields[new_pos[0]][new_pos[1]].move(rogue_data)
           if field_info:
               return field_info
           else:
               return self._fields[position[0]][position[1]].move(rogue_data)
        else:
            pass
            # return that we crossed some border
            # shouldn't we react to field from the map's neighbour being included
            # in visible_surrounding ??

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
