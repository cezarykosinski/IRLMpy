class ConstantsBaseClass:
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise NameError("Class is locked. Can't change attributes (%s)." % name)
        self.__dict__[name] = value


FIELD_CONSTANTS = {
    'DEFAULT_VALUE': 0,
    #'NaF_VALUE': 0 
    }
    
PROPERTIES_CONSTANTS = {
    'size': 25,
    'initialRatio': 0.525,
    'mooreNeighbourhoodSize': 1,
    'numberOfIterations': 4,
    'condition': 0.4,
    'wages': [1, 1, 1, 1, 1, 1, 1, 1, 1],
    'seed': 777,
    }
