from functools import reduce

from config import MAP_CONFIG as MC, EVO_CONFIG as EC


def balance_criterion(map):
    """
    for a given context of population's sample of conditions, calculates the ratio between floor and rock fields on an average map
    :param sample: list of conditions: id, val (pairs containing comparison string and an int value), score
    """
    if 0.2 < (map.get_no_of_floors() / MC['SIZE']**2) < 0.8:
        return 1000
    return -500


def groupness_criterion(map):
    """
    for a given context of population's sample of conditions, calculates the average number of individual groups per map
    :param sample: list of conditions: id, val (pairs containing comparison string and an int value), score
    """
    top_score = 10000
    if map.get_no_of_groups_with_less_than_two_exits() == 0 and map.get_no_of_groups_with_at_least_two_exits() > 0:
        return top_score
    elif map.get_no_of_groups_with_less_than_two_exits() > 0 and map.get_no_of_groups_with_at_least_two_exits() > 0:
        return top_score - 100 * map.get_no_of_groups_with_less_than_two_exits()
    return -top_score // 2


def qualify_map(map, eval_functions):
    return reduce(lambda x, fun: x + fun(map), eval_functions, 0)


def sample_acceptance_score(sample, maps_generator):
    score = reduce(lambda currval, m: currval + qualify_map(m, [balance_criterion, groupness_criterion]), maps_generator, 0)
    sample[2] = score
    return sample


def reach_simulation(sample, map_from_sample):
    ctx = map_from_sample(sample)

    ctx.start_with_rogue()
    pass
