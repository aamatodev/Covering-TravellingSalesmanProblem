import numpy as np


class Fitness:
    def __init__(self, route, cities, delta, refund):
        self.delta = delta
        self.refund = refund
        self.cities = cities
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
