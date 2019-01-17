import logging
import time
from pathos.multiprocessing import ProcessingPool as Pool

from src.evo.evaluation_functions import *
from constants import FIELD_CONSTANTS as FC
from config import EVO_CONFIG as EC
import random

from src.maps.map_context import MapContext


def initiate_population(size, n):
    logging.info("Condi_evo: initiating_population")
    signs = ["<", ">", "<=", ">="]
    return [[[random.choice(signs), random.random()] for _ in range(size+1)] for _ in range(n)]


def cut_condi_population(population, res):
    n_cutted_elems = (int(len(res) * EC['DROP_RATIO']))
    logging.info("Condi_evo: cutting_population by " + str(n_cutted_elems) + " elems")
    res.sort()
    cut_res = res[:n_cutted_elems]
    lucky_numbers = map(lambda x: x[1], cut_res)
    for l in lucky_numbers:
        logging.debug(l)
    survivors = [population[n] for n in lucky_numbers]
    return survivors


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
    probes = random.sample(population, no_of_mutations)
    for p in probes:
        mutate_single_condi(p)
    return population


def evolve_condi_population(population, res):
    logging.info("Condi_evo: evolving_population")
    # res.sort()
    # for entry in (map(lambda x: str((x[0], population[x[1]])), res)):
    #     logging.info(entry)
    drop_ratio = 0.6666666666666666666
    amount_of_offspring = int(len(population) * drop_ratio)
    logging.debug("amount_of_offspring: "+ str(amount_of_offspring))
    population = cut_condi_population(population, res)
    logging.debug("Cut population:")
    offspring = []
    for p in population:
        logging.debug(p)
    while amount_of_offspring>0:
        cohab1, cohab2 = random.sample(population, 2)
        pivot = random.randint(1, len(cohab1) - 2)
        offspring.append(cohab1[:pivot] + cohab2[pivot:])
        offspring.append(cohab2[:pivot] + cohab1[pivot:])
        logging.debug("from cohab1 " + str(cohab1))
        logging.debug("and cohab2 " + str(cohab2))
        logging.debug("pivoted at " + str(pivot))
        logging.debug("constructed " + str(cohab1[:pivot] + cohab2[pivot:]))
        logging.debug("and " + str(cohab2[:pivot] + cohab1[pivot:]))
        amount_of_offspring -= 2
    population += mutate_condi_population(offspring)


def prepare_conditions(condition_probe):
    return [sign + str(val) for sign, val in condition_probe]


def context_from_condi_probe(condition_probe):
    FC['CONDITION'] = prepare_conditions(condition_probe)
    return MapContext()


def display_n_best(population, n=1):
    logging.info("Condi_evo: displaying_" + str(n) + "_best")
    for condition_probe in population[:n]:
        ctx = context_from_condi_probe(condition_probe)
        ctx.start(EC['NO_OF_MAPS'])
        logging.info("Displaying: " + str(condition_probe))
        ctx.display()


def calculate(population, evaluation_functions, context_from_probe):
    logging.info("Condi_evo: calculating population:")
    logging.info(population)
    for it in range(EC['NO_OF_ITERATIONS']):
        logging.info("Condi_evo: calculating iteration " + str(it) +
              " with population containing " + str(len(set(tuple(tuple(el) for el in row) for row in population))) + " unique elements")
        iter_start = time.time()
        scores = [([], id) for id in range(0, EC['POPULATION_SIZE'])]
        for efun in evaluation_functions:
            pool = Pool(EC['POOL_SIZE'])
            res = pool.map(lambda probe: efun(probe, context_from_probe), population)
            scores = [(curr + [nscore], id) for nscore, (curr, id) in zip(res, scores)]
        evolve_condi_population(population, scores)

        if it % 4 == 0:
            display_n_best(population)
        logging.info(time.time() - iter_start)


def main(ns=2):
    gen_start = time.time()
    logging.basicConfig(filename="logs/" + str(int(gen_start)) + ".log", level=logging.DEBUG)                                                   #, format='%(relativeCreated)6d %(threadName)s %(message)s')
    logging.info("EVO_CONFIG:")
    logging.info(EC)
    FC['NEIGHBOURHOOD_SIZE'] = ns
    FC['WAGES'] = [[1] if (lvl == 0) else [1]*8*lvl for lvl in range(0, ns+1)]
    logging.info(FC['WAGES'])
    primary_metrics = [groupness_metric, balance_metric]
    population = initiate_population(ns, EC['POPULATION_SIZE'])
    calculate(population, primary_metrics, context_from_condi_probe)
    display_n_best(population, EC['POPULATION_SIZE'])
    logging.info("FINISHED EVOLUTION WITH PRIMARY METRICS")
    extra_evaluation = [complexity_metric]
    calculate(population, extra_evaluation, context_from_condi_probe)
    display_n_best(population, EC['POPULATION_SIZE'])
    logging.info(time.time() - gen_start)


if __name__ == '__main__':
    main(4)
