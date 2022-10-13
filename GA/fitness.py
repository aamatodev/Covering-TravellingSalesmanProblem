import csv

import numpy as np, random, operator, pandas as pd, matplotlib.pyplot as plt

from greedy import greedy


class City:
    def __init__(self, id, x, y, population):
        self.id = id
        self.x = x
        self.y = y
        self.population = population

    def distance(self, city):
        xDis = abs(self.x - city.x)
        yDis = abs(self.y - city.y)
        # distance = np.sqrt((xDis ** 2) + (yDis ** 2))
        distance = np.linalg.norm(np.array([self.x, self.y]) - np.array([city.x, city.y]))
        return distance

    def CityRevenue(self, cities, delta, coveredCities, vaccinatedPopulation, refund):
        revenue = 0
        if coveredCities[self.id] == 0:
            revenue += self.population * refund
            coveredCities[self.id] = 1
        for consideredCity in cities:
            dis = self.distance(consideredCity)
            if self.distance(consideredCity) < delta and coveredCities[
                consideredCity.id] == 0 and consideredCity.id != self.id:
                coveredCities[consideredCity.id] = 1
                revenue += ((consideredCity.population * (1 - self.distance(consideredCity) / delta)) * refund)
                vaccinatedPopulation += consideredCity.population
        return revenue, coveredCities, vaccinatedPopulation

    def __repr__(self):
        return str(self.id)


class Fitness:
    def __init__(self, route, cities, delta, populations, refund):
        self.delta = delta
        self.refund = refund
        self.cities = cities
        self.populations = populations
        self.route = route
        self.revenue = 0
        self.cost = 0
        self.vaccinatedPopulation = 0
        self.coveredCities = [0] * len(cities)
        self.fitness = 0.0

    def fullRouteRevenue(self):
        totalRevenue = 0
        totalCost = 0
        distance = 0
        for idx, consideredCity in enumerate(self.route):
            revenue, newCoveredCities, vaccinatedPopulation = consideredCity.CityRevenue(self.cities,
                                                                                                      self.delta,
                                                                                                      self.coveredCities,
                                                                                                      self.vaccinatedPopulation,
                                                                                                      self.refund)
            self.coveredCities = newCoveredCities
            self.vaccinatedPopulation += vaccinatedPopulation
            if idx > 0:
                distance = consideredCity.distance(self.cities[self.route[idx - 1].id])
            totalRevenue += revenue - distance
        return totalRevenue

    def routeFitness(self):
        if self.fitness == 0:
            self.fitness = float(self.fullRouteRevenue())
        return self.fitness


def createRoute(cityList, population):
    route = []
    totalPopulation = np.sum(population)
    MinCover = random.randint(30,99) / 100
    print(MinCover)
    coverage = 0
    coveredCities = [0] * len(cityList)
    alreadyVisited = []

    while coverage < MinCover and coveredCities.count(1) < len(cityList)-1:

        selectedNode = random.randint(0, len(cityList)-1)
        while (cityList[selectedNode] in alreadyVisited) or (coveredCities[selectedNode]==1):
            selectedNode = random.randint(0, len(cityList)-1)

        alreadyVisited.append(cityList[selectedNode])
        revenue, newCoveredCities, vaccinatedPopulation = cityList[selectedNode].CityRevenue(cityList, 300, coveredCities,
                                                                                          0, 5)
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
        fitnessResults[i] = Fitness(population[i], cityList,300, citiesPopulation, 5).routeFitness()
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


def geneticAlgorithm(cities,population, popSize, eliteSize, mutationRate, generations):
    pop = initialPopulation(popSize, cities, population)
    print("Initial distance: " + str( rankRoutes(pop , cities, population  )[0][1]))

    for i in range(0, generations):
        pop = nextGeneration(pop, eliteSize, mutationRate, cities, population)

    print("Final distance: " + str( rankRoutes(pop , cities, population  )[0][1]))
    bestRouteIndex = rankRoutes(pop, cities, population )[0][0]
    bestRoute = pop[bestRouteIndex]
    print(bestRoute)
    return bestRoute


cityList = []



node_array = []
with open('Berlin52.txt', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=' ')
    for row in reader:
        node_array.append([float(row[1]), float(row[2])])

fullData = np.array(node_array)

#adjMatrix = calculateADJMatrix(fullData[:, :2])

with open('population.txt', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        population = row

population = np.array(population, dtype='float64')

for i in range(len(fullData)):
    cityList.append(City(id=i, x=fullData[i][0], y=fullData[i][1], population=population[i]))

path = [13, 25, 46, 51, 28, 36, 32, 42, 11, 6, 30, 40, 10, 50, 13]
route = []
for i in path:
    route.append(City(id=i, x=fullData[i][0], y=fullData[i][1], population=population[i]))

fitness = Fitness(route=route, cities=cityList, delta=300, populations=population, refund=5)

print(fitness.fullRouteRevenue())

#print(createRoute(cityList, population))

#geneticAlgorithm(cities=cityList,population = population, popSize=30, eliteSize=20, mutationRate=0.01, generations=200)
