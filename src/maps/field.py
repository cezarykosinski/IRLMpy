from config import GROUP_CONFIG as GC
from config import FIELD_CONFIG as FCONFIG
from constants import FIELD_CONSTANTS as FC


class Field:
    """
    Elementary object

    """

    def __init__(self, x, y, mid):
        self.position = x, y
        self.value = FCONFIG['DEFAULT_VALUE']
        self.map_id = mid
        self.group_id = GC['NO_GROUP_ID']
        self.neighbours_values = {}
        self.neighbours = {}

    def set_neighbours(self, fields):
        # neighbours grouped by level of neighbourhoodism instead of row by row.
        # This implementation can be moved to set_neighbours_values
        n_size = FC['NEIGHBOURHOOD_SIZE']
        x, y = [i + n_size for i in self.position]

        for s in range(1, n_size + 1):
            self.neighbours[s] = []
            rng = list(range(-s, s + 1))
            self.neighbours[s] += [fields[x - i][y - s] for i in rng if fields[x - i][y - s] not in self.neighbours[s]]
            self.neighbours[s] += [fields[x - s][y + i] for i in rng if fields[x - s][y + i] not in self.neighbours[s]]
            self.neighbours[s] += [fields[x + i][y + s] for i in rng if fields[x + i][y + s] not in self.neighbours[s]]
            self.neighbours[s] += [fields[x + s][y - i] for i in rng if fields[x + s][y - i] not in self.neighbours[s]]
        # for r in self.neighbours.values():
        #     print(len(r))

    def set_neighbours_values(self):
        # import pdb; pdb.set_trace()
        self.neighbours_values[0] = [self.value]
        for s in range(1, FC['NEIGHBOURHOOD_SIZE']+1):
            self.neighbours_values[s] = [n.value for n in self.neighbours[s]]

    def calculate(self):
        # import pdb; pdb.set_trace()
        """
        todo
        :return:
        """
        is_rock = False
        for lvl in range(FC['NEIGHBOURHOOD_SIZE']+1):
            num_of_considered_neighbours = lvl*8 if lvl else 1
            waged_neighbours_values = [nv * w for (nv, w) in list(zip(self.neighbours_values[lvl], FC['WAGES'][lvl]))]
            ratio = float(sum(waged_neighbours_values)) / float(num_of_considered_neighbours)
            is_rock = is_rock or eval(str(ratio) + FC['CONDITION'][lvl])
            self.value = FCONFIG['ROCK'] if is_rock else FCONFIG['FLOOR']

    def is_rock(self):
        return self.value == FCONFIG['ROCK']

    def display(self):
        """
        todo
        :return:
        """
        return [".", "#"][self.value]

    def display_group(self):
        """
        todo
        :return:
        """
        return [str(self.group_id), "#"][self.value]
