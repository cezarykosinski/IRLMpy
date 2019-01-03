from src.maps.map_context import MapContext
from constants import FIELD_CONSTANTS as FC
from config import MAP_CONFIG as MConfig
from config import EVO_CONFIG as EC
from functools import reduce
import random


def initiate_population(size, n):
    signs = ["<", "==", ">", "<=", ">="]
    vals = range(1, (size * 2 + 1) ** 2)
    return [[(random.choice(signs), random.choice(vals)) for _ in range(size)] for _ in range(n)]


def prepare_conditions(condition_probe):
    return [sign + str(val) for sign, val in condition_probe]


def cut_condi_population(population, res):
    cut_res = res.sort()[:(int(len(res) * EC['DROP_RATIO']))]
    lucky_numbers = map(lambda x: x[1], cut_res)
    survivors = [population[n] for n in lucky_numbers]
    return survivors


def evolve_condi_population(population):
    new_population = []
    for elem in population:
        cohab = random.choice(population)
        pivot = random.randint(1, len(elem) - 1)
        new_population.append(elem[:pivot] + cohab[pivot:])
    return new_population


def mutate_single_condi(condition_probe):
    size = len(condition_probe) - 1
    signs = ["<", "==", ">", "<=", ">="]
    vals = range(1, (size * 2 + 1) ** 2)

    feature_no = random.randint(0, size)
    magic_value = random.randint(0, 1)

    condition_probe[feature_no][magic_value] = random.choice([signs, vals][magic_value])
    return condition_probe


def mutate_condi_population(population):
    probe_no = random.randint(0, len(population) - 1)
    population[probe_no] = mutate_single_condi(population[probe_no])
    return population


### METRICS ###
def balance_metric(condition_probe):
    """
    for a given condition_probe of conditions, calculates the ratio between floor and rock fields on an average map
    :param condition_probe: list of conditions (pairs containing comparison string and an int value)
    """
    FC['CONDITION'] = prepare_conditions(condition_probe)
    ctx = MapContext()
    n_maps = EC['NO_OF_MAPS']
    ctx.start(n_maps)
    func = lambda balance, map: balance + abs(map.get_no_of_floors() - MConfig['SIZE'] ** 2 // 2)
    return reduce(func, ctx.maps, 0)


def groupness_metric(condition_probe):
    """
    for a given population of conditions, calculates the average number of individual groups per map
    :param condition_probe: list of conditions (pairs containing comparison string and an int value)
    """
    FC['CONDITION'] = prepare_conditions(condition_probe)
    ctx = MapContext()
    n_maps = EC['NO_OF_MAPS']
    ctx.start(n_maps)
    n_groups = 0
    for m in ctx.maps:
        n_groups += len(m.groups)
    return float(n_groups) / float(n_maps)


###


def display_n_best(population, n):
    for condition_probe in population[:n]:
        FC['CONDITION'] = prepare_conditions(condition_probe)
        ctx = MapContext()
        ctx.start(EC['NO_OF_MAPS'])
        ctx.display()


def calculate(ns=3):
    FC['NEIGHBOURHOOD_SIZE'] = ns

    metrics = [balance_metric, groupness_metric]
    metrics_wages = [50, 50]

    pop_size = EC['POPULATION_SIZE']
    population = initiate_population(ns, pop_size)

    for it in range(EC['NO_OF_ITERATIONS']):
        res = [(0, id) for id in range(0, pop_size)]
        for mi in range(len(metrics)):
            fun = metrics[mi]
            wage = metrics_wages[mi]
            n_res = map(lambda p: fun(p) * wage, population)
            res = [(nscore + curr, id) for nscore, (curr, id) in zip(n_res, res)]

        population = cut_condi_population(population, res)
        population += evolve_condi_population(population)
        population = mutate_condi_population(population)

        display_n_best(population, 1)
