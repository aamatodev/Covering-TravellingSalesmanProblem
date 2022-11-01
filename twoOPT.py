import csv
import random

import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
from fitness import Fitness


def _improve(bestPath, bestGain, cityList, size, population, delta, refund):

    saved = None

    # Choose 2 unique edges defined by their first node
    for a in range(size - 3):
        for c in range(a + 2, size-1):
            path = exchange(bestPath, a, c)

            #change = calculatePathCost(path, adjMatrix)
            change, vaccinatedPopulation = Fitness(path, cityList, delta, refund).routeFitness()

            if change > bestGain:
                saved = a, c
                bestGain = change

    print(saved, bestGain)

    return saved, bestGain


def exchange(p, a, c):

    # without loss of generality, sort (???)
    # a, b = sorted([a, b])

    b, d = a + 1, c + 1

    sol = p[:a+1] + p[c:b - 1:-1] + p[d:]

    return sol


def TwoOPT(cityList, population, greedyPath, greedyGain, delta, refund):
    bestChange = 1000000000
    bestGain = greedyGain
    bestPath = greedyPath
    saved=0

    #To sort out this cycle. Everything else should work
    while bestChange >= bestGain and saved is not None:
        saved, bestChange = _improve(bestPath, bestGain, cityList, len(bestPath), population, delta, refund)

        if bestChange > bestGain:
            a, c = saved
            bestPath = exchange(bestPath, a, c)
            bestGain = bestChange

        print(bestPath, bestGain)
    return bestPath, bestGain
