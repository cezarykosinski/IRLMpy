class ConstantsBaseClass:
    """
    todo
    """
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise NameError("Class is locked. Can't change attributes (%s)." % name)
        self.__dict__[name] = value


groupConstants = {
    'noGroupId': -1
    }

fieldConstants = {
    'default_value': 0,
    'wages': [[1, 1, 1], [1, 0, 1], [1, 1, 1]],
    'mooreNeighbourhoodSize': 1,
    'condition': 0.4, #NOT GENERIC
    'NaF': None
    }
    
mapConstants = {
    'size': 25,
    'initialRatio': 0.525,
    'numberOfIterations': 1,
    'seed': 777,
    }
    
#class fieldConstants(ConstantsBaseClass):
#    def __init__(self):
#        fieldConstants.default_value = 0
#        fieldConstants.wages = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
#        fieldConstants.mooreNeighbourhoodSize = 1
#        fieldConstants.condition = 0.4
#        fieldConstants.NaF = None
#
#
#class groupConstants(ConstantsBaseClass):
#    def __init__(self):
#        groupConstants.noGroupId = -1
#
#class mapConstants(ConstantsBaseClass):
#    def __init__(self):
#        mapConstants.size = 25
#        mapConstants.initialRatio = 0.525
#        mapConstants.numberOfIterations = 1
#        mapConstants.seed = 666
