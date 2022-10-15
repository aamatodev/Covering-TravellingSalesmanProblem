import csv

import numpy as np
from city import City


def openCity(cityfile, populationfile):
    cityList = []
    node_array = []
    with open(cityfile, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ')
        for row in reader:
            node_array.append([float(row[1]), float(row[2])])

    fullData = np.array(node_array)

    # adjMatrix = calculateADJMatrix(fullData[:, :2])

    with open(populationfile, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            population = row

    population = np.array(population, dtype='float64')

    for i in range(len(fullData)):
        cityList.append(City(id=i, x=fullData[i][0], y=fullData[i][1], population=population[i]))

    return cityList, population