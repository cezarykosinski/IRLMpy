from functools import reduce

from config import MAP_CONFIG as MC, EVO_CONFIG as EC


def balance_criterion(map):
    """
    for a given context of population's sample of conditions, calculates the ratio between floor and rock fields on an average map
    :param sample: list of conditions: id, val (pairs containing comparison string and an int value), score
    """
    return 0.2 < (map.get_no_of_floors() / MC['SIZE']**2) < 0.8


def groupness_criterion(map):
    """
    for a given context of population's sample of conditions, calculates the average number of individual groups per map
    :param sample: list of conditions: id, val (pairs containing comparison string and an int value), score
    """
    return map.get_no_of_groups_with_less_than_two_exits() == 0 and map.get_no_of_groups_at_least_two_exits() > 0


def qualify_map(map, eval_functions):
    return reduce(lambda x, fun: x and fun(map), eval_functions, True)


def sample_acceptance_score(sample, maps_generator_from_sample):
    return list(map(lambda m: qualify_map(m, [balance_criterion, groupness_criterion]), maps_generator_from_sample(sample))).count(True)


def reach_simulation(sample, map_from_sample):
    ctx = map_from_sample(sample)

    ctx.start_with_rogue()
    pass
