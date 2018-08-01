from random import seed, randint
from models.field import Field
from models.group import Group
from constants import FIELD_CONSTANTS as FC
from constants import GROUP_CONSTANTS as GC
from constants import MAP_CONSTANTS as MC


class Map:
    """
    todo
    """

    def __init__(self, id, ctx,
                 northbound=[[FC['DEFAULT_VALUE']] * MC['SIZE']] * FC['MOORE_NEIGHBOURHOOD_SIZE'],
                 westbound=[[FC['DEFAULT_VALUE']] * FC['MOORE_NEIGHBOURHOOD_SIZE']] * MC['SIZE'],
                 southbound=[[FC['DEFAULT_VALUE']] * MC['SIZE']] * FC['MOORE_NEIGHBOURHOOD_SIZE'],
                 eastbound=[[FC['DEFAULT_VALUE']] * FC['MOORE_NEIGHBOURHOOD_SIZE']] * MC['SIZE']):
        self.id = id
        self.__context = ctx

        self.__northbound = northbound
        self.__westbound = westbound
        self.__southbound = southbound
        self.__eastbound = eastbound

        self.is_accessed = False
        self.__groups = []
        self.__fields = [[Field(fi, fj) for fj in range(MC['SIZE'])]
                         for fi in range(MC['SIZE'])]

        self.__genererate_noise()
        self.__set_fields_neighbours()
        self.calculate()
        self.group_fields()

    def __genererate_noise(self):
        """
        todo
        :return:
        """
        fields_no = MC['SIZE'] ** 2
        amount_of_noise = 0

        # legacy ctx -> self.__context (to discuss)
        seed(self.__context.id)

        while (amount_of_noise / fields_no) < MC['INITIAL_RATIO']:
            x = randint(0, MC['SIZE'] - 1)
            y = randint(0, MC['SIZE'] - 1)
            if self.__fields[x][y].value == FC['DEFAULT_VALUE']:
                self.__fields[x][y].value = 1
                amount_of_noise += 1

    def __get_field_neighbours(self, position_tuple):
        """
        todo
        :param position_tuple:
        :return:
        """
    #maybe better on the field side to store references to the neighbours instead of just the positions, then we could've just update them locally from the field itself (clearer the code would be)
        x, y = position_tuple
        mns = FC['MOORE_NEIGHBOURHOOD_SIZE']
        
        corner = [[FC['DEFAULT_VALUE']] * mns] * mns
        left_fields = corner + self.__eastbound + corner
        mid_fields = self.__northbound + [[f.value for f in frow] for frow in self.__fields] + self.__southbound
        right_fields = corner + self.__westbound + corner
        all_fields = [i+j+g for i, j, g in zip(left_fields, mid_fields, right_fields)]

        # todo lambda should be unnamed function
        is_in_range = lambda x, y: 0 <= x < MC['SIZE'] and 0 <= y < MC['SIZE']

        neighbours_values = [[all_fields[i+x][j+y]
                              for j in range(0, 2*mns+1)]
                             for i in range(0, 2*mns+1)]
        neighbours_positions = [self.__fields[i+x][j+y].position
                                if is_in_range(i+x, j+y)
                                else None 
                                for j in range(-mns, mns+1)
                                for i in range(-mns, mns+1)]
        return neighbours_values, neighbours_positions
    
    def __set_fields_neighbours(self):
        """
        todo
        :return:
        """
        for row in self.__fields:
            for f in row:
                f.neighbours_values, f.neighbours_positions = self.__get_field_neighbours(f.position)

    def get_north_bound(self):
        """
        todo
        :return:
        """
        
    def get_south_bound(self):
        """
        todo
        :return:
        """
    
    def get_east_bound(self):
        """
        todo
        :return:
        """
    
    def get_west_bound(self):
        """
        todo
        :return:
        """

    def calculate(self):
        """
        todo
        :return:
        """
        for i in range(MC['NUMBER_OF_ITERATIONS']):
            for row in self.__fields:
                for f in row:
                    f.calculate()
            self.__set_fields_neighbours()

    def access(self): #direction?
        """
        todo
        :return:
        """
        raise NotImplementedError()
        self.is_accessed = true
        self.groups_wayouts_providing()

    def group_fields(self):
        """
        todo
        :return:
        """
        for row in self.__fields:
            for f in row: 
                if f.value == 0 and f.groupId == GC['NO_GROUP_ID']:
                    new_group = Group(f)
                    new_group.find_rest_of_the_fields(self.__fields)
                    self.__groups.append(new_group)

    def groups_wayouts_providing(self):
        """
        todo
        :return:
        """
        for g in self.__groups:
            g.wayout_providing(self.__fields)

    def display(self):
        """
        todo
        :return:
        """
        for row in self.__fields:
            row_display = ""
            for f in row: 
                row_display += f.display()
            print(row_display)

    def display_groups(self):
        """
        todo
        :return:
        """
        for row in self.__fields:
            row_display = ""
            for f in row: 
                row_display += f.display_group()
            print(row_display)

