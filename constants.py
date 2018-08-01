class ConstantsBaseClass:
    """
    todo
    """
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise NameError("Class is locked. Can't change attributes (%s)." % name)
        self.__dict__[name] = value


GROUP_CONSTANTS = {
    'noGroupId': -1
    }

FIELD_CONSTANTS = {
    'default_value': 0,
    'wages': [[1, 1, 1], [1, 0, 1], [1, 1, 1]],
    'mooreNeighbourhoodSize': 1,
    'condition': 0.4, #NOT GENERIC
    'NaF': None
    }
    
MAP_CONSTANTS = {
    'size': 25,
    'initialRatio': 0.525,
    'numberOfIterations': 1,
    'seed': 777,
    }
    
#class FIELD_CONSTANTS(ConstantsBaseClass):
#    def __init__(self):
#        FIELD_CONSTANTS.default_value = 0
#        FIELD_CONSTANTS.wages = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
#        FIELD_CONSTANTS.mooreNeighbourhoodSize = 1
#        FIELD_CONSTANTS.condition = 0.4
#        FIELD_CONSTANTS.NaF = None
#
#
#class GROUP_CONSTANTS(ConstantsBaseClass):
#    def __init__(self):
#        GROUP_CONSTANTS.noGroupId = -1
#
#class MAP_CONSTANTS(ConstantsBaseClass):
#    def __init__(self):
#        MAP_CONSTANTS.size = 25
#        MAP_CONSTANTS.initialRatio = 0.525
#        MAP_CONSTANTS.numberOfIterations = 1
#        MAP_CONSTANTS.seed = 666
