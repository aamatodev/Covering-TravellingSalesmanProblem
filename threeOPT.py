import csv
import random

import networkx as nx
import numpy as np
from matplotlib import pyplot as plt

from fitness import Fitness


def _improve(bestPath, bestCurrentRevenue, cities, size, delta, refund):
    """
    Breakable improvement loop, find an improving move and return to the
    main loop to execute it, selects whether we look for the first
    improving move or the best.
    """
    saved = None
    bestChange = bestCurrentRevenue

    # Choose 3 unique edges defined by their first node
    for a in range(size - 5):
        for c in range(a + 2, size - 3):
            for e in range(c + 2, size - 1):
                change = 0
                # Now we have seven (sic) permutations to check
                for i in range(7):
                    # TODO improve this...
                    path = exchange(bestPath, i, a, c, e)

                    fitness = Fitness(path, cities, delta, refund)

                    change, vaccinatedPopulation = fitness.fullRouteRevenue()

                    if change > bestChange:
                        saved = a, c, e, i
                        bestChange = change

    print(saved, 'Improved total gain: ', bestChange)

    return saved, bestChange - bestCurrentRevenue


def calculatePathCost(path, adjMatrix):
    cost = 0
    for i in range(len(path) - 1):
        cost += adjMatrix[path[i]][path[i + 1]]
    return cost


def exchange(p, i, a, c, e, broad=False):
    """In the broad sense, 3-opt means choosing any three edges ab, cd
    and ef and chopping them, and then reconnecting (such that the
    result is still a complete tour). There are eight ways of doing
    it. One is the identity, 3 are 2-opt moves (because either ab, cd,
    or ef is reconnected), and 4 are 3-opt moves (in the narrower
    sense)."""
    n = len(p)

    # without loss of generality, sort
    a, c, e = sorted([a, c, e])
    b, d, f = a + 1, c + 1, e + 1

    which = i

    # in the following slices, the nodes abcdef are referred to by
    # name. x:y:-1 means step backwards. anything like c+1 or d-1
    # refers to c or d, but to include the item itself, we use the +1
    # or -1 in the slice
    if which == 0:
        sol = p[:a + 1] + p[b:c + 1] + p[d:e + 1] + p[f:]  # identity
    elif which == 1:
        sol = p[:a + 1] + p[b:c + 1] + p[e:d - 1:-1] + p[f:]  # 2-opt
    elif which == 2:
        sol = p[:a + 1] + p[c:b - 1:-1] + p[d:e + 1] + p[f:]  # 2-opt
    elif which == 3:
        sol = p[:a + 1] + p[c:b - 1:-1] + p[e:d - 1:-1] + p[f:]  # 3-opt
    elif which == 4:
        sol = p[:a + 1] + p[d:e + 1] + p[b:c + 1] + p[f:]  # 3-opt
    elif which == 5:
        sol = p[:a + 1] + p[d:e + 1] + p[c:b - 1:-1] + p[f:]  # 3-opt
    elif which == 6:
        sol = p[:a + 1] + p[e:d - 1:-1] + p[b:c + 1] + p[f:]  # 3-opt
    elif which == 7:
        sol = p[:a + 1] + p[e:d - 1:-1] + p[c:b - 1:-1] + p[f:]  # 3-opt

    return sol


def ThreeOPT(cities, CurrentBestPath, CurrentBestRevenue, delta, refund):
    bestChange = 1
    bestPath = CurrentBestPath
    bestRevenue = CurrentBestRevenue

    while bestChange > 0:
        saved, bestChange = _improve( bestPath, bestRevenue, cities, len(bestPath), delta, refund)

        if bestChange > 0:
            a, c, e, which = saved
            bestPath = exchange(bestPath, which, a, c, e)
            bestRevenue += bestChange

    print('Best Path: ', bestPath)
    print('Best Total Gain: ', bestRevenue)
    return bestPath, bestRevenue
