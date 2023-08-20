import csv

import numpy as np
import operator
import pandas as pd
import random

from matplotlib import pyplot as plt

from city import City
from fitness import Fitness
from greedy import greedy
from opencity import openCity
from twoOPT import TwoOPT


def createRoute(cityList, population):
    route = []
    totalPopulation = np.sum(population)
    MinCover = random.randint(30, 99) / 100
    print('Minimum people to be vaccinated: ', MinCover)
    coverage = 0
    coveredCities = [0] * len(cityList)
    alreadyVisited = []

    while coverage < MinCover and coveredCities.count(1) < len(cityList) - 1:

        selectedNode = random.randint(0, len(cityList) - 1)
        while (cityList[selectedNode] in alreadyVisited) or (coveredCities[selectedNode] == 1):
            selectedNode = random.randint(0, len(cityList) - 1)

        alreadyVisited.append(cityList[selectedNode])
        revenue, newCoveredCities, vaccinatedPopulation = cityList[selectedNode].CityRevenue(cityList, 300,
                                                                                             coveredCities, 0, 5)
        coveredCities = newCoveredCities
        coverage += vaccinatedPopulation / totalPopulation
        route.append(cityList[selectedNode])

    route.append(route[0])

    return route


def initialPopulation(popSize, cityList, citiesPopulation):
    population = []

    for i in range(0, popSize):
        population.append(createRoute(cityList, citiesPopulation))
    return population


def rankRoutes(population, cityList, citiesPopulation):
    fitnessResults = {}
    for i in range(0, len(population)):
        fitnessResults[i], vaccinatedPopulation = Fitness(population[i], cityList, 300, 5).routeFitness()
    list = sorted(fitnessResults.items(), key=operator.itemgetter(1), reverse=True)
    return list


def selection(popRanked, eliteSize):
    selectionResults = []
    df = pd.DataFrame(np.array(popRanked), columns=["Index", "Fitness"])
    df['cum_sum'] = df.Fitness.cumsum()
    df['cum_perc'] = 100 * df.cum_sum / df.Fitness.sum()

    for i in range(0, eliteSize):
        selectionResults.append(popRanked[i][0])
    for i in range(0, len(popRanked) - eliteSize):
        pick = 100 * random.random()
        for i in range(0, len(popRanked)):
            if pick <= df.iat[i, 3]:
                selectionResults.append(popRanked[i][0])
                break
    return selectionResults


def matingPool(population, selectionResults):
    matingpool = []
    for i in range(0, len(selectionResults)):
        index = selectionResults[i]
        matingpool.append(population[index])
    return matingpool


def breed(parent1, parent2):
    child = []
    childP1 = []
    childP2 = []

    geneA = int(random.random() * len(parent1))
    geneB = int(random.random() * len(parent1))

    startGene = min(geneA, geneB)
    endGene = max(geneA, geneB)

    for i in range(startGene, endGene):
        childP1.append(parent1[i])

    childP2 = [item for item in parent2 if item not in childP1]

    child = childP1 + childP2
    return child


def breedPopulation(matingpool, eliteSize):
    children = []
    length = len(matingpool) - eliteSize
    pool = random.sample(matingpool, len(matingpool))

    for i in range(0, eliteSize):
        children.append(matingpool[i])

    for i in range(0, length):
        child = breed(pool[i], pool[len(matingpool) - i - 1])
        children.append(child)
    return children


def mutate(individual, mutationRate):
    for swapped in range(len(individual)):
        if (random.random() < mutationRate):
            swapWith = int(random.random() * len(individual))

            city1 = individual[swapped]
            city2 = individual[swapWith]

            individual[swapped] = city2
            individual[swapWith] = city1
    return individual


def mutatePopulation(population, mutationRate):
    mutatedPop = []

    for ind in range(0, len(population)):
        mutatedInd = mutate(population[ind], mutationRate)
        mutatedPop.append(mutatedInd)
    return mutatedPop


def nextGeneration(currentGen, eliteSize, mutationRate, cityList, citiesPopulation):
    popRanked = rankRoutes(currentGen, cityList, citiesPopulation)
    selectionResults = selection(popRanked, eliteSize)
    matingpool = matingPool(currentGen, selectionResults)
    children = breedPopulation(matingpool, eliteSize)
    nextGeneration = mutatePopulation(children, mutationRate)
    return nextGeneration


def geneticAlgorithm(cities, population, popSize, eliteSize, mutationRate, generations):
    pop = initialPopulation(popSize, cities, population)
    print("Initial gain: " + str(rankRoutes(pop, cities, population)[0][1]))
    progress = []
    progress.append(rankRoutes(pop, cities, population)[0][1])

    for i in range(0, generations):
        pop = nextGeneration(pop, eliteSize, mutationRate, cities, population)
        progress.append(rankRoutes(pop, cities, population)[0][1])

    # plt.clf()
    # plt.plot(progress)
    # plt.ylabel('Distance')
    # plt.xlabel('Generation')
    # plt.show()
    # plt.clf()

    print("Final gain: " + str(rankRoutes(pop, cities, population)[0][1]))
    bestRouteIndex = rankRoutes(pop, cities, population)[0][0]
    bestRoute = pop[bestRouteIndex]

    TwoOPTPath, TwoOPTRevenue = TwoOPT(cities, population, bestRoute, rankRoutes(pop, cities, population)[0][1], 300, 5)

    print("Final gain after 2 OPT: " + str(TwoOPTRevenue))

    cleanedRoute, revenue = RemoveUneddedNodes(TwoOPTPath, cities, population)

    print("Final gain after LS: " + str(revenue))

    if cleanedRoute[0] != cleanedRoute[len(cleanedRoute) - 1]:
        cleanedRoute.append(cleanedRoute[0])
    return cleanedRoute, revenue


def populationCoveredByPath(path):
    pupulation = 0
    for city in path:
        pupulation = pupulation + city.population
    return pupulation


def RemoveUneddedNodes(bestRoute, cityList, population):
    minimumPopulation = np.sum(population) * 0.3
    fitness = Fitness(route=bestRoute, cities=cityList, delta=300, refund=5)
    bestRevenue, vaccinatedPopulation  = fitness.fullRouteRevenue()
    bestComputedRoute = bestRoute
    for idx, city in enumerate(bestRoute):
        if idx != 0 and idx != len(bestRoute):
            bkPath = bestComputedRoute.copy()
            bestComputedRoute.remove(city)
            newPath = bestComputedRoute
            fitness = Fitness(route=newPath, cities=cityList, delta=300, refund=5)
            newRevenue, vaccinatedPopulation = fitness.fullRouteRevenue()
            if newRevenue > bestRevenue:
                bestRevenue = newRevenue
                bestComputedRoute = newPath
            else:
                bestComputedRoute = bkPath

    fitness, vaccinatedPopulation = Fitness(route=bestComputedRoute, cities=cityList, delta=300, refund=5).fullRouteRevenue()

    while vaccinatedPopulation < minimumPopulation:
        citiesNotAlreadyInPath = list(set(cityList) - set(bestComputedRoute))
        path, cost = greedy(citiesNotAlreadyInPath, 300, population, 5, 1,
                            bestComputedRoute[len(bestComputedRoute) - 1].id)
        path = path[1:-1]
        bestComputedRoute = bestComputedRoute + path
        fitness, vaccinatedPopulation = Fitness(route=bestComputedRoute, cities=cityList, delta=300, refund=5).fullRouteRevenue()

    return bestComputedRoute, bestRevenue

# fitness = Fitness(route=route, cities=cityList, delta=300, populations=population, refund=5)

# print(fitness.fullRouteRevenue())

# print(createRoute(cityList, population))


# cityList, population = openCity('Berlin52.txt', 'population.txt')

# print( geneticAlgorithm(cities=cityList, population=population, popSize=30, eliteSize=20, mutationRate=0.01, generations=200))
