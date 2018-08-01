from random import seed, randint
from models.field import Field
from models.group import Group
from constants import FIELD_CONSTANTS as fc
from constants import GROUP_CONSTANTS as gc
from constants import MAP_CONSTANTS as mc


class Map:
    """
    todo
    """

    def __init__(self, id, ctx,
                 northbound=[[fc['default_value']] * mc['size']] * fc['mooreNeighbourhoodSize'],
                 westbound=[[fc['default_value']] * fc['mooreNeighbourhoodSize']] * mc['size'],
                 southbound=[[fc['default_value']] * mc['size']] * fc['mooreNeighbourhoodSize'],
                 eastbound=[[fc['default_value']] * fc['mooreNeighbourhoodSize']] * mc['size']):
        self.id = id
        self.__context = ctx

        self.__northbound = northbound
        self.__westbound = westbound
        self.__southbound = southbound
        self.__eastbound = eastbound

        self.is_accessed = False
        self.__groups = []
        self.__fields = [[Field(fi, fj) for fj in range(mc['size'])]
                         for fi in range(mc['size'])]

        self.__genererate_noise()
        self.__set_fields_neighbours()
        self.calculate()
        self.group_fields()

    def __genererate_noise(self):
        """
        todo
        :return:
        """
        fields_no = mc['size']**2
        amount_of_noise = 0

        # legacy ctx -> self.__context (to discuss)
        seed(self.__context.id)

        while (amount_of_noise / fields_no) < mc['initialRatio']:
            x = randint(0, mc['size']-1)
            y = randint(0, mc['size']-1)
            if self.__fields[x][y].value == fc['default_value']:
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
        mns = fc['mooreNeighbourhoodSize']
        
        corner = [[fc['default_value']]*mns]*mns
        left_fields = corner + self.__eastbound + corner
        mid_fields = self.__northbound + [[f.value for f in frow] for frow in self.__fields] + self.__southbound
        right_fields = corner + self.__westbound + corner
        all_fields = [i+j+g for i, j, g in zip(left_fields, mid_fields, right_fields)]

        # todo lambda should be unnamed function
        is_in_range = lambda x, y: 0 <= x < mc['size'] and 0 <= y < mc['size']

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
        for i in range(mc['numberOfIterations']):
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
                if f.value == 0 and f.groupId == gc['noGroupId']:
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

