from constants import FIELD_CONSTANTS as FC
from config import EVO_CONFIG as EC
import random


def initiate_population(size, n):
    signs = ["<", "==", ">", "<=", ">="]
    vals = range(1, (size * 2 + 1) ** 2)
    return [[(random.choice(signs), random.choice(vals)) for _ in range(size)] for _ in range(n)]


def evolve_population(population):
    pass


def balance_metric(population):
    """

    :return: float
    """
    pass

def groupness_metric(population):
    """

    :param population:
    :return:
    """
    pass

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
    population = population[:(int(len(population)*EC['DROP_RATIO']))]
    population += evolve_population(population)
