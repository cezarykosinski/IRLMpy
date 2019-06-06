from functools import reduce

from config import MAP_CONFIG as MC
from config import EVO_CONFIG as EC


def balance_criterion(map):
    """
    for a given context of population's sample of conditions, calculates the ratio between floor and rock fields on an average map
    :param map: generated map, ready to be scored
    """
    if 0.2 < (map.get_no_of_floors() / MC['SIZE']**2) < 0.8:
        return EC['MIN_SCORE']//10
    return -EC['MIN_SCORE']*0.3


def groupness_criterion(map):
    """
    for a given context of population's sample of conditions, calculates the average number of individual groups per map
    that meets the criterion of the number of exits
    :param map: generated map, ready to be scored
    """
    top_score = EC['MIN_SCORE']*0.25
    map.group_fields()
    if len(map._groups) >= 1:
        if map.get_no_of_groups_with_at_least_two_exits() == len(map._groups):
            return top_score
        elif 0 < map.get_no_of_groups_with_at_least_two_exits() < len(map._groups):
            return top_score - 100 * map.get_no_of_groups_with_less_than_two_exits()
    return -top_score


def cell_distance_criterion(map):
    map_size = MC['SIZE']
    if 2 < map.maximal_cell_max_distance or\
            map.minimal_cell_max_distance > map_size*0.8:
        return -EC['MIN_SCORE']*0.5
    return EC['MIN_SCORE']//10


def qualify_map(map, eval_functions):
    return reduce(lambda x, fun: x + fun(map), eval_functions, 0)


def sample_acceptance_score(sample, maps_generator):
    criterions = [balance_criterion, groupness_criterion, cell_distance_criterion]
    sample[2] = reduce(lambda curval, m: curval + qualify_map(m, criterions), maps_generator, 0)
    return sample
