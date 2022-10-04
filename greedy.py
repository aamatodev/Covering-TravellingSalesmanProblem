import numpy as np
from random import randint

INT_MAX = -2147483647


def calculateRefund(startPoint, hubPoint, population, coveredNodeList, coveredNodes, adjMatrix, delta, refund):
    i = 0
    partialIncome = 0
    for i in range(len(adjMatrix[0])):
        if startPoint != i and coveredNodeList[i] == 0:
            if adjMatrix[hubPoint][i] < delta:
                coveredNodeList[i] = 1
                partialIncome += (population[i] * (1 - adjMatrix[hubPoint][i] / delta)) * refund

    partialIncome -= adjMatrix[startPoint][hubPoint]

    return coveredNodeList, coveredNodes, partialIncome


def greedy(adjMatrix, delta, population, refund, startNode=0):
    path = []
    totalIncome = 0
    coveredNodeList = [0] * len(adjMatrix[0])
    BKcoveredNodeList = [0] * len(adjMatrix[0])
    PossibleCoveredNodeList = [0] * len(adjMatrix[0])

    i = startNode
    j = 0
    nodeToAppend = -1
    canImprove = True

    coveredNodeList[startNode] = 1
    path.append(startNode)

    coveredNodes = 1
    # cover node around 0
    for i in range(len(adjMatrix[0])):
        if startNode != i:
            if adjMatrix[startNode][i] < delta:
                coveredNodeList[i] = 1
                totalIncome += (float(population[i]) * (1 - adjMatrix[startNode][i] / delta)) * refund
                coveredNodes += 1

    BKcoveredNodeList = coveredNodeList.copy()
    i=startNode

    while coveredNodes < (len(adjMatrix[0])):
        maxRefund = -100000
        for j in range(len(adjMatrix[0])):
            coveredNodeList = BKcoveredNodeList.copy()
            if i != j and coveredNodeList[j] == 0 :
                partialIncome = 0
                coveredNodeList, coveredNodes, partialIncome = calculateRefund(i, j, population, coveredNodeList,
                                                                               coveredNodes, adjMatrix, delta, refund)
                if maxRefund < partialIncome:
                    maxRefund = partialIncome
                    nodeToAppend = j
                    PossibleCoveredNodeList = coveredNodeList

        BKcoveredNodeList = PossibleCoveredNodeList
        BKcoveredNodeList[nodeToAppend] = 1
        coveredNodes = BKcoveredNodeList.count(1)
        path.append(nodeToAppend)
        i = nodeToAppend
        totalIncome += partialIncome

    print(totalIncome)
    print(BKcoveredNodeList)
    path.append(startNode)
    print(path)
    return path


#tsp = [[0, 10, 15, 20], [10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]]
#greedy(tsp, 20, [10, 20, 10, 20], 5)
