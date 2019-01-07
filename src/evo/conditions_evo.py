import time

from src.maps.map_context import MapContext
from constants import FIELD_CONSTANTS as FC
from config import MAP_CONFIG as MConfig
from config import EVO_CONFIG as EC
from functools import reduce
import random


def initiate_population(size, n):
    print("Condi_evo: initiating_population")
    signs = ["<", "==", ">", "<=", ">="]
    return [[[random.choice(signs), random.random()] for _ in range(size+1)] for _ in range(n)] + [[[">", 1], [">=", 0.5], ["<", 0.125]]]


def prepare_conditions(condition_probe):
    return [sign + str(val) for sign, val in condition_probe]


def cut_condi_population(population, res):
    n_cutted_elems = (int(len(res) * EC['DROP_RATIO']))
    print("Condi_evo: cutting_population by " + str(n_cutted_elems) + " elems")
    print(list(map(lambda x: str((x[0], population[x[1]])), res)))
    cut_res = sorted(res)[:n_cutted_elems]
    lucky_numbers = map(lambda x: x[1], cut_res)
    survivors = [population[n] for n in lucky_numbers]
    return survivors


def evolve_condi_population(population):
    print("Condi_evo: evolving_population")
    offspring = []
    ammount_of_offspring = len(population) * int(1/EC['DROP_RATIO']) - len(population)
    for _ in range(ammount_of_offspring):
        cohab1, cohab2 = random.choices(population, k=2)
        pivot = random.randint(1, len(cohab1) - 1)
        offspring.append(cohab1[:pivot] + cohab2[pivot:])
    return offspring


def mutate_single_condi(condition_probe):
    print("Condi_evo: mutating " + str(condition_probe))
    size = len(condition_probe) - 1
    signs = ["<", "==", ">", "<=", ">="]

    feature_no = random.randint(0, size)
    magic_value = random.randint(0, 1)

    condition_probe[feature_no][magic_value] = random.random() if magic_value else random.choice(signs)
    return condition_probe


def mutate_condi_population(population):
    print("Condi_evo: mutating_population")
    probe_no = random.randint(0, len(population) - 1)
    population[probe_no] = mutate_single_condi(population[probe_no])
    return population


### METRICS ###
def balance_metric(condition_probe):
    """
    for a given condition_probe of conditions, calculates the ratio between floor and rock fields on an average map
    :param condition_probe: list of conditions (pairs containing comparison string and an int value)
    """
    print("Condi_evo: balance_metric " + str(condition_probe))
    FC['CONDITION'] = prepare_conditions(condition_probe)
    ctx = MapContext()
    n_maps = EC['NO_OF_MAPS']
    ctx.start(n_maps)
    func = lambda balance, map: balance + abs(map.get_no_of_floors() - MConfig['SIZE'] ** 2 // 2)
    res =  reduce(func, ctx.maps.values(), 0)
    print("Finished with score: " + str(res))
    return res


def groupness_metric(condition_probe):
    """
    for a given population of conditions, calculates the average number of individual groups per map
    :param condition_probe: list of conditions (pairs containing comparison string and an int value)
    """
    print("Condi_evo: groupness_metric " + str(condition_probe))
    FC['CONDITION'] = prepare_conditions(condition_probe)
    ctx = MapContext()
    n_maps = EC['NO_OF_MAPS']
    ctx.start(n_maps)
    n_groups = 0
    for m in ctx.maps.values():
        n_groups += len(m._groups)
    res = float(n_groups) / float(n_maps)
    print("Finished with score: " + str(res))
    return res
###

def display_n_best(population, n):
    print("Condi_evo: displaying_" + str(n) + "_best")
    for condition_probe in population[:n]:
        FC['CONDITION'] = prepare_conditions(condition_probe)
        ctx = MapContext()
        ctx.start(EC['NO_OF_MAPS'])
        ctx.display()


def calculate(ns=2):
    gen_start = time.time()
    print("Condi_evo: calculating")
    print("ns = " + str(ns))
    print("EVO_CONFIG:")
    print(EC)
    FC['NEIGHBOURHOOD_SIZE'] = ns
    FC['WAGES'] = [[0] if lvl else [1]*lvl for lvl in range(0,ns+1)]

    metrics = [balance_metric, groupness_metric]
    metrics_wages = [50, 50]

    pop_size = EC['POPULATION_SIZE']
    population = initiate_population(ns, pop_size)

    for it in range(EC['NO_OF_ITERATIONS']):
        print("\nCondi_evo: calculating iteration " + str(it) +
              " with population of size " + str(len(population)))
        iter_start = time.time()
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
        print(time.time() - iter_start)
    print(time.time() - gen_start)

calculate()
