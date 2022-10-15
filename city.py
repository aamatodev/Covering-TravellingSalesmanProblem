import numpy as np

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