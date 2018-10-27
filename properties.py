class ConstantsBaseClass:
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise NameError("Class is locked. Can't change attributes (%s)." % name)
        self.__dict__[name] = value


FIELD_CONSTANTS = {
    'DEFAULT_VALUE': 0,
    #'NAF_VALUE': 0
    }
    
PROPERTIES_CONSTANTS = {
    'SIZE': 25,
    'INITIAL_RATIO': 0.525,
    'NEIGHBOURHOOD_SIZE': 1,
    'NUMBER_OF_ITERATIONS': 4,
    'CONDITION': 0.4,
    'WAGES': [1, 1, 1, 1, 1, 1, 1, 1, 1],
    'SEED': 777,
    }
