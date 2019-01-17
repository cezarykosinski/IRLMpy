from functools import reduce

from config import MAP_CONFIG as MC, EVO_CONFIG as EC

def balance_metric(probe, context_from_probe):
    """
    for a given context of population's probe of conditions, calculates the ratio between floor and rock fields on an average map
    :param probe: list of conditions (pairs containing comparison string and an int value)
    """
    ctx = context_from_probe(probe)
    ctx.start(EC['NO_OF_MAPS'])
    func = lambda balance, map: balance + abs(map.get_no_of_floors() - MC['SIZE'] ** 2 // 2)
    return reduce(func, ctx.maps.values(), 0)


def groupness_metric(probe, context_from_probe):
    """
    for a given context of population's probe of conditions, calculates the average number of individual groups per map
    :param probe: list of conditions (pairs containing comparison string and an int value)
    """
    ctx = context_from_probe(probe)
    ctx.start(EC['NO_OF_MAPS'])
    n_groups = 0
    for m in ctx.maps.values():
        map_n_groups = len(m._groups)
        if map_n_groups == 0:
            map_n_groups = 987654321
        n_groups += map_n_groups
    return n_groups


def complexity_metric(probe, context_from_probe):
    """
    for a given context of population's probe of conditions, calculates the length of a maximum straight line of floors
    :param probe: list of conditions (pairs containing comparison string and an int value)
    """
    ctx = context_from_probe(probe)
    ctx.start(EC['NO_OF_MAPS'])
    longest_line = 0
    for m in ctx.maps.values():
        longest_line = max(m.get_longest_horizontal_path(), m.get_longest_vertical_path(), longest_line)
    return longest_line

def reach_metaheuristic(probe, context_from_probe):
    ctx = context_from_probe(probe)
    ctx.start_with_rogue()

