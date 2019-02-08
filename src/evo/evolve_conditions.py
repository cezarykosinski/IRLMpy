import logging
import operator
import random
import time
from pathos.multiprocessing import ProcessingPool as Pool

from src.evo.evaluation_functions import *
from constants import FIELD_CONSTANTS as FC
from config import EVO_CONFIG as EC
from src.maps.map_context import MapContext


def prepare_conditions(condition_sample):
    return [sign + str(val) for sign, val in condition_sample]


def map_from_condi_sample(id):
    ctx = MapContext(id)
    ctx.start(0)
    return ctx.maps[(0, 0)]


def maps_generator_from_condi_sample(condi_sample):
    FC['CONDITION'] = prepare_conditions(condi_sample[1])
    return [map_from_condi_sample(i) for i in range(EC['NO_OF_MAPS'])]


def display_n(population, n=1):
    logging.info("Condi_evo: displaying_" + str(n) + "_best")
    for condition_sample in population[:n]:
        map = maps_generator_from_condi_sample(condition_sample)[0]
        logging.info("Displaying: " + str(condition_sample))
        for row in map.print():
            logging.info(row)


def display_nth(population, n):
    logging.info("Condi_evo: displaying " + str(n) + "th of population")
    map = maps_generator_from_condi_sample(population[n])[0]
    map.display()


def initiate_population(size, n):
    logging.info("Condi_evo: initiating_population")
    signs = ["<", ">", "<=", ">="]
    return [[id, [[random.choice(signs), random.random()] for _ in range(size+1)], 0.0] for id in range(n)]


def cut_condi_population(population):
    n_elems_to_cut = (int(len(population) * EC['DROP_RATIO']))
    logging.info("Condi_evo: cutting_population by " + str(n_elems_to_cut) + " elems")
    return population[:n_elems_to_cut]


def mutate_condi_genome(genome):
    sign = random.choice(["<", ">", "<=", ">="])
    new_val = random.random()
    if random.random() >= 0.5:
        logging.debug("Condi_evo: mutating genome " + str(genome) +" into " + str([sign, new_val]))
        return [sign, new_val]
    return genome


def mutate_condi_sample(sample):
    logging.debug("Condi_evo: mutating sample " + str(sample))
    return list(map(mutate_condi_genome, sample))


def reindex(population):
    for i in range(len(population)):
        population[i][0] = i


def evolve_condi_population(population):
    logging.info("Condi_evo: evolving_population")
    population.sort(key=operator.itemgetter(2)) #SORT
    logging.debug("Population've been sorted")
    for entry in population:
        logging.debug(str(entry[0]) + ": " + str(entry[2]))
    drop_ratio = EC['DROP_RATIO']
    amount_of_offspring = int(len(population) * drop_ratio)
    logging.debug("amount_of_offspring: " + str(amount_of_offspring))
    population = cut_condi_population(population) #CUT
    logging.debug("Population after the cut:")
    offspring = []
    for p in population:
        logging.debug(p)
    while amount_of_offspring > 0:                #EVOLVE
        cohab1, cohab2 = random.sample(population, 2)
        pivot = random.randint(1, len(cohab1) - 2)
        offspring1 = [42, mutate_condi_sample(cohab1[1][:pivot] + cohab2[1][pivot:]), 0.0] #MUTATE OVER CROSSOVER
        offspring2 = [43, mutate_condi_sample(cohab2[1][:pivot] + cohab1[1][pivot:]), 0.0] #MUTATE OVER CROSSOVER
        logging.debug("from cohab1 " + str(cohab1))
        logging.debug("and cohab2 " + str(cohab2))
        logging.debug("pivoted at " + str(pivot))
        logging.debug("constructed " + str(offspring1[1]))
        logging.debug("and " + str(offspring2[1]))
        offspring += [offspring1, offspring2]
        amount_of_offspring -= 2
    population += offspring
    reindex(population)                         #REINDEX


def calculate(population, maps_generator_from_sample):
    logging.info("Condi_evo: calculating population:")
    logging.info(population)
    for it in range(EC['NO_OF_ITERATIONS']):
        logging.info("Condi_evo: calculating iteration " + str(it))
        iter_start = time.time()
        pool = Pool(EC['POOL_SIZE'])
        pool.map(lambda s: sample_acceptance_score(s, maps_generator_from_sample), population)
        evolve_condi_population(population)

        if it % 5 == 0:
            display_n(population, 1)
        logging.info(time.time() - iter_start)


def main(ns=2):
    gen_start = time.time()
    now = "-".join(map (str, time.localtime()[:3])) + "_" + "".join(map(str, time.localtime()[3:6]))
    logging.basicConfig(filename="logs/v2.0/" + now + ".log", level=logging.DEBUG)                                                   #, format='%(relativeCreated)6d %(threadName)s %(message)s')
    logging.info("EVO_CONFIG:")
    logging.info(EC)

    FC['NEIGHBOURHOOD_SIZE'] = ns
    FC['WAGES'] = [[1] if (lvl == 0) else [1]*8*lvl for lvl in range(0, ns+1)]

    logging.info(FC['WAGES'])
    population = initiate_population(ns, EC['POPULATION_SIZE'])
    calculate(population, maps_generator_from_condi_sample)
    display_n(population, EC['POPULATION_SIZE'])
    logging.info(time.time() - gen_start)


if __name__ == '__main__':
    main(3)
