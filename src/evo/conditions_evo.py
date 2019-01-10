import time, logging
from pathos.multiprocessing import ProcessingPool as Pool

from src.maps.map_context import MapContext
from constants import FIELD_CONSTANTS as FC
from config import MAP_CONFIG as MConfig
from config import EVO_CONFIG as EC
from functools import reduce
import random


def initiate_population(size, n):
    logging.info("Condi_evo: initiating_population")
    signs = ["<", "==", ">", "<=", ">="]
    return [[[random.choice(signs), random.random()] for _ in range(size+1)] for _ in range(n)] + [[[">", 1], [">=", 0.5], ["<", 0.125]]]


def prepare_conditions(condition_probe):
    return [sign + str(val) for sign, val in condition_probe]


def cut_condi_population(population, res):
    n_cutted_elems = (int(len(res) * EC['DROP_RATIO']))
    logging.info("Condi_evo: cutting_population by " + str(n_cutted_elems) + " elems")
    logging.info(list(map(lambda x: str((x[0], population[x[1]])), res)))
    cut_res = sorted(res)[:n_cutted_elems]
    lucky_numbers = map(lambda x: x[1], cut_res)
    survivors = [population[n] for n in lucky_numbers]
    return survivors


def evolve_condi_population(population, res):
    logging.info("Condi_evo: evolving_population")
    amount_of_offspring = int(len(population) * EC['DROP_RATIO'])
    population = cut_condi_population(population, res)
    for _ in range(amount_of_offspring):
        cohab1, cohab2 = random.choices(population, k=2)
        pivot = random.randint(1, len(cohab1) - 1)
        population.append(cohab1[:pivot] + cohab2[pivot:])
    return population


def mutate_single_condi(condition_probe):
    size = len(condition_probe) - 1
    signs = ["<", "==", ">", "<=", ">="]

    feature_no = random.randint(0, size)
    magic_value = random.randint(0, 1)
    new_val = random.random() if magic_value else random.choice(signs)
    logging.info("Condi_evo: mutating " + str(condition_probe[feature_no]) + "'s " + ["sign", "value"][magic_value] +" into " + str(new_val))
    condition_probe[feature_no][magic_value] = new_val
    return condition_probe


def mutate_condi_population(population):
    logging.info("Condi_evo: mutating_population")
    no_of_mutations = int(len(population)*EC['MUTATION_RATE'])
    probes = random.choices(population, k=no_of_mutations)
    for p in probes:
        mutate_single_condi(p)
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
    res = reduce(func, ctx.maps.values(), 0)
    logging.info("Condi_evo: balance_metric " + str(condition_probe) + ". Finished with score: " + str(res))
    return res


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
    for m in ctx.maps.values():
        n_groups += len(m._groups)
    res = float(n_groups) / float(n_maps)
    logging.info("Condi_evo: groupness_metric " + str(condition_probe) + "Finished with score: " + str(res))
    return res
###

def display_n_best(population, n):
    logging.info("Condi_evo: displaying_" + str(n) + "_best")
    for condition_probe in population[:n]:
        FC['CONDITION'] = prepare_conditions(condition_probe)
        ctx = MapContext()
        ctx.start(EC['NO_OF_MAPS'])
        ctx.display()


def calculate(ns=2):
    logging.basicConfig(filename='example.log', level=logging.DEBUG, format='%(relativeCreated)6d %(threadName)s %(message)s')

    gen_start = time.time()
    logging.info("Condi_evo: calculating")
    logging.info("ns = " + str(ns))
    logging.info("EVO_CONFIG:")
    logging.info(EC)
    FC['NEIGHBOURHOOD_SIZE'] = ns
    FC['WAGES'] = [[1] if (lvl == 0) else [1]*(2**lvl*4) for lvl in range(0,ns+1)]
    logging.info(FC['WAGES'])
    metrics = [balance_metric, groupness_metric]
    metrics_wages = [50, 1000]

    pop_size = EC['POPULATION_SIZE']
    population = initiate_population(ns, pop_size)

    for it in range(EC['NO_OF_ITERATIONS']):
        logging.info("\nCondi_evo: calculating iteration " + str(it) +
              " with population of size " + str(len(population)))
        iter_start = time.time()
        res = [(0, id) for id in range(0, pop_size)]
        for mi in range(len(metrics)):
            pool = Pool()
            fun = metrics[mi]
            wage = metrics_wages[mi]
            n_res = pool.map(lambda p: fun(p) * wage, population)
            res = [(nscore + curr, id) for nscore, (curr, id) in zip(n_res, res)]
        population = evolve_condi_population(population, res)
        population = mutate_condi_population(population)

        if it % 10 == 0:
            display_n_best(population, 1)
        logging.info(time.time() - iter_start)
    logging.info(time.time() - gen_start)

if __name__ == '__main__':
    calculate()
