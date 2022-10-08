import numpy as np
from random import randint

INT_MAX = -2147483647


def calculateRefund(startPoint, hubPoint, population, coveredNodeList, coveredNodes, adjMatrix, delta, refund):
    i = 0
    partialIncome = 0
    vaccinatedPopulation = 0
    for i in range(len(adjMatrix[0])):
        if startPoint != i and coveredNodeList[i] == 0:
            if adjMatrix[hubPoint][i] < delta:
                coveredNodeList[i] = 1
                partialIncome += (population[i] * (1 - adjMatrix[hubPoint][i] / delta)) * refund
                vaccinatedPopulation+=population[i]

    partialIncome -= adjMatrix[startPoint][hubPoint]

    return coveredNodeList, coveredNodes, partialIncome, vaccinatedPopulation


def greedy(adjMatrix, delta, population, refund, startNode=0):
    path = []
    totalIncome = 0
    coveredNodeList = [0] * len(adjMatrix[0])
    BKcoveredNodeList = [0] * len(adjMatrix[0])
    potentialCoveredNodeList = [0] * len(adjMatrix[0])

    startingHub = startNode
    potentialHub = 0
    nodeToAppend = -1
    canImprove = True

    vaccinatedPopulation=0
    potentialVaccinatedPopulation=0
    BKvaccinatedPopulation=0

    minimumPopulation = np.sum(population)*0.3


    coveredNodeList[startNode] = 1
    path.append(startNode)

    #Mancava da sommare nell'income totale il refund ottenuto dalla popolazione del nodo iniziale
    totalIncome+=population[startNode]*refund
    BKvaccinatedPopulation+=population[0]

    coveredNodes = 1

    # Try to cover nodes around 0
    for potentialNode in range(len(adjMatrix[0])):
        if startNode != potentialNode:
            if adjMatrix[startNode][potentialNode] < delta:
                coveredNodeList[potentialNode] = 1
                totalIncome += (float(population[potentialNode]) * (1 - adjMatrix[startNode][potentialNode] / delta)) * refund
                coveredNodes += 1
                BKvaccinatedPopulation+=population[potentialHub]

    BKcoveredNodeList = coveredNodeList.copy()
    startingHub = startNode

    maxRefund = -100000

    potentialCheckedNodes = 1

    while potentialCheckedNodes < (len(adjMatrix[0])):
        potentialVaccinatedPopulation=0
        for potentialHub in range(len(adjMatrix[0])):
            coveredNodeList = BKcoveredNodeList.copy()

            if startingHub != potentialHub and coveredNodeList[potentialHub] == 0 :
                partialIncome = 0
                coveredNodeList, coveredNodes, partialIncome, vaccinatedPopulation = calculateRefund(startingHub, potentialHub, population, coveredNodeList,
                                                                               coveredNodes, adjMatrix, delta, refund)

                if maxRefund < partialIncome:
                    maxRefund = partialIncome
                    nodeToAppend = potentialHub
                    potentialCoveredNodeList = coveredNodeList
                    potentialVaccinatedPopulation = vaccinatedPopulation
                elif maxRefund > partialIncome and BKvaccinatedPopulation+potentialVaccinatedPopulation < minimumPopulation:
                    nodeToAppend = potentialHub
                    potentialCoveredNodeList = coveredNodeList
                    potentialVaccinatedPopulation = vaccinatedPopulation

        BKcoveredNodeList = potentialCoveredNodeList
        BKcoveredNodeList[nodeToAppend] = 1
        coveredNodes = BKcoveredNodeList.count(1)
        if(startingHub!=nodeToAppend):
            path.append(nodeToAppend)
            startingHub = nodeToAppend
        totalIncome += maxRefund
        BKvaccinatedPopulation+=potentialVaccinatedPopulation
        potentialCheckedNodes+=1

    print(totalIncome)
    print(BKcoveredNodeList)
    path.append(startNode)
    print(path)
    print(BKvaccinatedPopulation)
    print(minimumPopulation)
    return path


#tsp = [[0, 20, 20, 20], [20, 0, 20, 20], [20, 20, 0, 20], [20, 20, 20, 0]]
#greedy(tsp, 19, [1, 13, 10, 20], 1)
