import json
import logging
import operator
import random
import time
import uuid
from pathos.multiprocessing import ProcessingPool as Pool

from src.evo.evaluation_functions import *
from constants import FIELD_CONSTANTS as FC
from config import EVO_CONFIG as EC
from src.maps.map_context import MapContext

NOW = "-".join(map(str, time.localtime()[:3])) + "_" + "".join(map(str, time.localtime()[3:6]))
STORAGE_PREFIX = "logs/v2.0/" + NOW


def prepare_conditions(condition_sample):
    return [sign + str(val) for sign, val in condition_sample]


def map_from_condi_sample(id):
    ctx = MapContext(id)
    ctx.start(0)
    return ctx.maps[(0, 0)]


def maps_generator_from_condi_sample(condi_sample):
    ns = len(condi_sample[1]) - 1
    FC['NEIGHBOURHOOD_SIZE'] = ns
    FC['WAGES'] = [[1] if (lvl == 0) else [1]*8*lvl for lvl in range(0, ns+1)]
    FC['CONDITION'] = prepare_conditions(condi_sample[1])
    return (map_from_condi_sample(i) for i in range(EC['NO_OF_MAPS']))


def display_n(population, n=1):
    logging.info("Condi_evo: displaying_" + str(n) + "_best")
    for condition_sample in population[:n]:
        map = next(maps_generator_from_condi_sample(condition_sample))
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
    return [[uuid.uuid4().hex, [[random.choice(signs), random.random()] for _ in range(size+1)], 0.0] for _ in range(n)]


def cut_condi_population(population):
    basic_cut_place = int(len(population) * EC['DROP_RATIO'])
    score_based_cut = len(list(filter(lambda elem: elem[2] > EC['MIN_SCORE'], population)))
    cut_in = basic_cut_place if basic_cut_place < score_based_cut else score_based_cut
    logging.info("Condi_evo: cutting_population by " + str(cut_in) + " elems")
    return population[:cut_in]


def mutate_condi_genome(genome):
    sign = random.choice(["<", ">", "<=", ">="])
    new_val = random.random()
    if random.random() >= 0.5:
        logging.debug("Condi_evo: mutating genome " + str(genome) + " into " + str([sign, new_val]))
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

    population.sort(key=operator.itemgetter(2), reverse=True)  # SORT

    logging.debug("Population sorted")

    for entry in population:
        logging.debug(str(entry[0]) + ": " + str(entry[2]))
    population = cut_condi_population(population)  # CUT
    amount_of_offspring = EC['POPULATION_SIZE'] - len(population)

    logging.debug("Population after the cut:")
    for p in population:
        logging.debug(p)
    logging.debug("amount_of_offspring: " + str(amount_of_offspring))

    offspring = []
    while amount_of_offspring > 0:                # EVOLVE
        cohab1, cohab2 = random.sample(population, 2)
        pivot = random.randint(1, len(cohab1) - 2)
        offspring1 = [uuid.uuid4().hex, mutate_condi_sample(cohab1[1][:pivot] + cohab2[1][pivot:]), 0.0]  # MUTATE OVER CROSSOVER
        offspring2 = [uuid.uuid4().hex, mutate_condi_sample(cohab2[1][:pivot] + cohab1[1][pivot:]), 0.0]  # MUTATE OVER CROSSOVER

        logging.debug("from cohab1 " + str(cohab1))
        logging.debug("and cohab2 " + str(cohab2))
        logging.debug("pivoted at " + str(pivot))
        logging.debug("constructed " + str(offspring1[1]))
        logging.debug("and " + str(offspring2[1]))

        offspring += [offspring1, offspring2]
        amount_of_offspring -= 2
    population += offspring


def calculate(population, maps_generator_from_sample):
    logging.info("Condi_evo: calculating population:")
    logging.info(population)
    pool = Pool(EC['POOL_SIZE'])
    for it in range(EC['NO_OF_ITERATIONS']):
        logging.info("Condi_evo: calculating iteration " + str(it))
        iter_start = time.time()

        population = pool.map(lambda s: sample_acceptance_score(s, maps_generator_from_sample(s)), population)  # EVALUATING POPULATION

        eval_fin = time.time()
        logging.info("TIME: Evaluating population finished in " + str(eval_fin - iter_start))

        evolve_condi_population(population)  # EVOLVING POPULATION

        evol_fin = time.time()
        logging.info("TIME: Evolving population finished in " + str(evol_fin-eval_fin))
        logging.info("TIME: Iteration finished in " + str(evol_fin - iter_start))

        with open(STORAGE_PREFIX + ".population", 'w') as f:
            f.write(json.dumps(population))

        if it % 10 == 9:
            display_n(population, 3)
    return population


def main(ns=2, filename=None):
    gen_start = time.time()
    logging.basicConfig(filename=STORAGE_PREFIX + ".log", level=logging.DEBUG)
    logging.info("STORAGE_PATH_PREFIX:" + STORAGE_PREFIX)
    logging.info("EVO_CONFIG:")
    logging.info(EC)

    FC['NEIGHBOURHOOD_SIZE'] = ns
    FC['WAGES'] = [[1] if (lvl == 0) else [1]*8*lvl for lvl in range(0, ns+1)]

    logging.info(FC['WAGES'])
    population = []
    if filename:
        with open(filename, 'r') as f:
            population = json.loads(f.read())

    population += initiate_population(ns, EC['POPULATION_SIZE'] - len(population))
    calculated_population = calculate(population, maps_generator_from_condi_sample)
    display_n(calculated_population, EC['POPULATION_SIZE'])
    logging.info("TIME: " + str(time.time() - gen_start))


if __name__ == '__main__':
    main(3, "logs/v2.0/2019-2-24_211220.population")
