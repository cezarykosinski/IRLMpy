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
    def __init__(self, id, ctx):
        self.id = id
        self.__context = ctx

        self.__northeastbound = ctx.set_northeast_bound(id)
        self.__northbound = ctx.setNorthbound(id)
        self.__northwestbound = ctx.setNorthwestBound(id)
        self.__westbound = ctx.setWestbound(id)
        self.__southwestbound = ctx.setSouthwestBound(id)
        self.__southbound = ctx.setSouthbound(id)
        self.__southeastbound = ctx.setSoutheastbound(id)
        self.__eastbound = ctx.setEastbound(id)


        self.is_accessed = False
        self.__groups = []
        self.__fields = [[Field(fi, fj) for fj in range(MC['SIZE'])]
                         for fi in range(MC['SIZE'])]

        self.__generate_noise()
        self.__set_fields_neighbours()
        self.calculate()
        self.group_fields()

    #do service'u 
    def __generate_noise(self):
        """
        todo
        :return:
        """
        fields_no = MC['SIZE'] ** 2
        amount_of_noise = 0

        seed(self.__context.id)

        while (amount_of_noise / fields_no) < MC['INITIAL_RATIO']:
            x = randint(0, MC['SIZE'] - 1)
            y = randint(0, MC['SIZE'] - 1)
            if self.__fields[x][y].value == FC['DEFAULT_VALUE']:
                self.__fields[x][y].value = 1
                amount_of_noise += 1

    def __set_fields_neighbours(self):
        """
        todo
        :return:
        """
        left_fields = self.__northeastbound + self.__eastbound + self.southeastbound
        mid_fields = self.__northbound + self.__fields + self.__southbound
        right_fields = self.__northwestbound + self.__westbound + self.southwestbound
        all_fields = [i+j+g for i,j,g in zip(left_fields, mid_fields, right_fields)]

        for row in self.__fields:
            for f in row:
                f.set_neighbours(all_fields)

    def __set_fields_neighbours_values(self):
        """
        todo
        :return:
        """
        for row in self.__fields:
            for f in row:
                f.set_neighbours_values()


    def get_northeast_bound(self):
        """
        todo
        :return:
        """
        return [row[(FC['MOORE_NEIGHBOURHOOD_SIZE'] + 1):] for row in self.__fields[:FC['MOORE_NEIGHBOURHOOD_SIZE']]]

    def get_north_bound(self):
        """
        todo
        :return:
        """
        return self.__fields[:FC['MOORE_NEIGHBOURHOOD_SIZE']]

    def get_northwest_bound(self):
        """
        todo
        :return:
        """
        return [row[:FC['MOORE_NEIGHBOURHOOD_SIZE']] for row in self.__fields[:FC['MOORE_NEIGHBOURHOOD_SIZE']]]

    def get_west_bound(self):
        """
        todo
        :return:
        """
        return [row[:FC['MOORE_NEIGHBOURHOOD_SIZE']] for row in self.__fields]
    
    def get_southwest_bound(self):
        """
        todo
        :return:
        """
        return [row[:FC['MOORE_NEIGHBOURHOOD_SIZE']] for row in self.__fields[(FC['MOORE_NEIGHBOURHOOD_SIZE'] + 1):]]

    def get_south_bound(self):
        """
        todo
        :return:
        """
        return self.__fields[(FC['MOORE_NEIGHBOURHOOD_SIZE']+1):]

    def get_southeast_bound(self):
        """
        todo
        :return:
        """
        return [row[FC['MOORE_NEIGHBOURHOOD_SIZE']:] for row in self.__fields[FC['MOORE_NEIGHBOURHOOD_SIZE']:]]

    def get_east_bound(self):
        """
        todo
        :return:
        """
        return [row[FC['MOORE_NEIGHBOURHOOD_SIZE']:] for row in self.__fields]

    def calculate(self):
        """
        todo
        :return:
        """
        for i in range(MC['NUMBER_OF_ITERATIONS']):
            for row in self.__fields:
                for f in row:
                    f.calculate()
            self.__set_fields_neighbours_values()

    def access(self): #direction?
        """
        todo
        :return:
        """
        raise NotImplementedError()
        self.is_accessed = True
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

