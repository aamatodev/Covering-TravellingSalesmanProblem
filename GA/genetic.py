import csv

import numpy as np
import operator
import pandas as pd
import random
from city import City
from fitness import Fitness
from opencity import openCity


def createRoute(cityList, population):
    route = []
    totalPopulation = np.sum(population)
    MinCover = random.randint(30, 99) / 100
    print(MinCover)
    coverage = 0
    coveredCities = [0] * len(cityList)
    alreadyVisited = []

    while coverage < MinCover and coveredCities.count(1) < len(cityList) - 1:

        selectedNode = random.randint(0, len(cityList) - 1)
        while (cityList[selectedNode] in alreadyVisited) or (coveredCities[selectedNode] == 1):
            selectedNode = random.randint(0, len(cityList) - 1)

        alreadyVisited.append(cityList[selectedNode])
        revenue, newCoveredCities, vaccinatedPopulation = cityList[selectedNode].CityRevenue(cityList, 300, coveredCities, 0, 5)
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
        fitnessResults[i] = Fitness(population[i], cityList, 300, citiesPopulation, 5).routeFitness()
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

    for i in range(0, generations):
        pop = nextGeneration(pop, eliteSize, mutationRate, cities, population)

    print("Final gain: " + str(rankRoutes(pop, cities, population)[0][1]))
    bestRouteIndex = rankRoutes(pop, cities, population)[0][0]
    bestRoute = pop[bestRouteIndex]
    print(bestRoute)
    return bestRoute


# path = [13, 25, 46, 51, 28, 36, 32, 42, 11, 6, 30, 40, 10, 50, 13]
# route = []
# for i in path:
#     route.append(City(id=i, x=fullData[i][0], y=fullData[i][1], population=population[i]))

# fitness = Fitness(route=route, cities=cityList, delta=300, populations=population, refund=5)

# print(fitness.fullRouteRevenue())

# print(createRoute(cityList, population))


cityList, population = openCity('Berlin52.txt', 'population.txt')

geneticAlgorithm(cities=cityList, population=population, popSize=30, eliteSize=20, mutationRate=0.01, generations=200)
