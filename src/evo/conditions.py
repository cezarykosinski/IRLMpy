from src.maps.map_context import MapContext
from constants import FIELD_CONSTANTS as FC
from config import MAP_CONFIG as MConfig
from config import EVO_CONFIG as EC
from functools import reduce
import random


def prepare_conditions(population):
    return [sign + str(val) for sign, val in population]


def initiate_population(size, n):
    signs = ["<", "==", ">", "<=", ">="]
    vals = range(1, (size * 2 + 1) ** 2)
    return [[(random.choice(signs), random.choice(vals)) for _ in range(size)] for _ in range(n)]


def evolve_population(population):
    new_population = []
    for elem in population:
        cohab = random.choice(population)
        pivot = random.randint(1, len(population) - 1)
        new_population.append(elem[pivot:] + cohab[:pivot])
    return new_population


### METRICS ###


def balance_metric(population):
    """
    for a given population of conditions, counts the ratio between floor and rock fields on an average map
    :return: float [0,100]
    """
    FC['CONDITION'] = prepare_conditions(population)
    ctx = MapContext()
    n_maps = EC['NO_OF_MAPS']
    ctx.start(n_maps)
    fun = lambda balance, map: balance + (map.get_nu_of_floors() - MConfig['SIZE']**2//2)
    return abs(reduce(fun, 0, ctx.maps))
    # balance = 0
    # for m in ctx.maps:
    #     balance += m.get_nu_of_floors()
    # return abs(balance - (MConfig['SIZE']**2 * n_maps / 2.0))


def groupness_metric(population):
    """
    for a given population of conditions, counts the ratio between floor and rock fields on an average map
    :param population: list of conditions (pairs containing comparison string and an int value)
    :return:
    """
    FC['CONDITION'] = prepare_conditions(population)
    ctx = MapContext()
    n_maps = EC['NO_OF_MAPS']
    ctx.start()
    n_groups = 0
    for m in ctx.maps:
        n_groups += len(m.groups)
    return 100 * (float(n_groups) / float(n_maps))


###


def calculate(ns=2):
    FC['NEIGHBOURHOOD_SIZE'] = ns
    FC['']
    metrics = [balance_metric, groupness_metric]
    metrics_wages = [50]
    population = initiate_population(FC['NEIGHBOURHOOD_SIZE'], EC['POPULATION_SIZE'])
    res = [[0] * len(population)]
    for i in len(metrics):
        fun = metrics[i]
        wage = metrics_wages[i]
        n_res = map(lambda p: fun(p) * wage, population)
        res = [i + j for i, j in zip(res, n_res)]
    population.sort(reverse=True)  # ???
    population = population[:(int(len(population) * EC['DROP_RATIO']))]
    population += evolve_population(population)
