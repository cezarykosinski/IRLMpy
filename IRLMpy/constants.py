class ConstantsBaseClass:
    """
    todo
    """
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise NameError("Class is locked. Can't change attributes (%s)." % name)
        self.__dict__[name] = value


GROUP_CONSTANTS = {
    'NO_GROUP_ID': -1
    }

FIELD_CONSTANTS = {
    'DEFAULT_VALUE': 0,
    'WAGES': [[1, 1, 1], [1, 0, 1], [1, 1, 1]],
    'MOORE_NEIGHBOURHOOD_SIZE': 1,
    'CONDITION': 0.4, #NOT GENERIC
    'NAF': None
    }
    
MAP_CONSTANTS = {
    'SIZE': 25,
    'INITIAL_RATIO': 0.525,
    'NUMBER_OF_ITERATIONS': 1,
    'SEED': 777,
    }
    
#class FIELD_CONSTANTS(ConstantsBaseClass):
#    def __init__(self):
#        FIELD_CONSTANTS.DEFAULT_VALUE = 0
#        FIELD_CONSTANTS.WAGES = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
#        FIELD_CONSTANTS.MOORE_NEIGHBOURHOOD_SIZE = 1
#        FIELD_CONSTANTS.CONDITION = 0.4
#        FIELD_CONSTANTS.NAF = None
#
#
#class GROUP_CONSTANTS(ConstantsBaseClass):
#    def __init__(self):
#        GROUP_CONSTANTS.NO_GROUP_ID = -1
#
#class MAP_CONSTANTS(ConstantsBaseClass):
#    def __init__(self):
#        MAP_CONSTANTS.size = 25
#        MAP_CONSTANTS.INITIAL_RATIO = 0.525
#        MAP_CONSTANTS.NUMBER_OF_ITERATIONS = 1
#        MAP_CONSTANTS.SEED = 666
