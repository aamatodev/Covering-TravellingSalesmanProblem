import numpy as np
from random import randint
from city import City
from opencity import openCity

INT_MAX = -2147483647


def calculateRefund(startPoint, hubPoint, population, coveredNodeList, coveredNodes, cityList, delta, refund):
    i = 0
    partialIncome = 0
    vaccinatedPopulation = 0
    for i in range(len(cityList)):
        if startPoint != i and coveredNodeList[i] == 0:
            if cityList[hubPoint].distance(cityList[i]) < delta:
                coveredNodeList[i] = 1
                partialIncome += (population[i] * (1 - cityList[hubPoint].distance(cityList[i]) / delta)) * refund
                vaccinatedPopulation += population[i]

    cost = cityList[startPoint].distance(cityList[hubPoint])
    partialIncome -= cost

    return coveredNodeList, coveredNodes, partialIncome, vaccinatedPopulation, cost


def greedy(cityList, delta, population, refund, startNode=0):
    path = []
    totalIncome = 0
    coveredNodeList = [0] * len(cityList)
    BKcoveredNodeList = [0] * len(cityList)
    potentialCoveredNodeList = [0] * len(cityList)

    pathCost = 0
    partialCost = 0

    startingHub = startNode
    potentialHub = 0
    nodeToAppend = -1
    canImprove = True

    vaccinatedPopulation = 0
    potentialVaccinatedPopulation = 0
    BKvaccinatedPopulation = 0

    minimumPopulation = np.sum(population) * 0.3

    coveredNodeList[startNode] = 1
    #path.append(startNode)
    path.append(cityList[startNode])

    # Mancava da sommare nell'income totale il refund ottenuto dalla popolazione del nodo iniziale
    totalIncome += population[startNode] * refund
    BKvaccinatedPopulation += population[startNode]

    coveredNodes = 1

    # Try to cover nodes around 0
    for potentialNode in range(len(cityList)):
        if startNode != potentialNode:
            if cityList[startNode].distance(cityList[potentialNode]) < delta:
                coveredNodeList[potentialNode] = 1
                totalIncome += (float(population[potentialNode]) * (
                            1 - cityList[startNode].distance(cityList[potentialNode]) / delta)) * refund
                coveredNodes += 1
                BKvaccinatedPopulation += population[potentialHub]

    BKcoveredNodeList = coveredNodeList.copy()
    startingHub = startNode

    maxRefund = -100000

    potentialCheckedNodes = 1

    improvement = True

    while potentialCheckedNodes < (len(cityList)) and improvement:
        potentialVaccinatedPopulation = 0
        maxRefund = -100000
        for potentialHub in range(len(cityList)):
            coveredNodeList = BKcoveredNodeList.copy()

            if startingHub != potentialHub and coveredNodeList[potentialHub] == 0:
                partialIncome = 0

                # calculateRefund andrebbe sostituito con city.cityRevenue, dopo aver adattato la funzione
                coveredNodeList, coveredNodes, partialIncome, vaccinatedPopulation, cost = calculateRefund(startingHub,
                                                                                                           potentialHub,
                                                                                                           population,
                                                                                                           coveredNodeList,
                                                                                                           coveredNodes,
                                                                                                           cityList,
                                                                                                           delta,
                                                                                                           refund)

                if maxRefund < partialIncome:
                    maxRefund = partialIncome
                    nodeToAppend = potentialHub
                    potentialCoveredNodeList = coveredNodeList
                    potentialVaccinatedPopulation = vaccinatedPopulation
                    partialCost = cost

        if totalIncome + maxRefund < totalIncome and BKvaccinatedPopulation + potentialVaccinatedPopulation > minimumPopulation:
            improvement = False

        BKcoveredNodeList = potentialCoveredNodeList
        BKcoveredNodeList[nodeToAppend] = 1
        coveredNodes = BKcoveredNodeList.count(1)
        if startingHub != nodeToAppend:
            #path.append(nodeToAppend)
            path.append(cityList[nodeToAppend])
            startingHub = nodeToAppend
        totalIncome += maxRefund
        BKvaccinatedPopulation += potentialVaccinatedPopulation
        potentialCheckedNodes += 1
        pathCost += partialCost

    print(totalIncome)
    print(BKcoveredNodeList)
    #path.append(startNode)
    path.append(cityList[startNode])
    print(path)
    print(BKvaccinatedPopulation)
    print(minimumPopulation)
    print("path cost - ", pathCost)
    return path, pathCost
