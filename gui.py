import os

import matplotlib
import networkx as nx
import numpy as np
from random import randint

from city import City
from fitness import Fitness
from genetic import geneticAlgorithm
from greedy import greedy
from threeOPT import ThreeOPT
from twoOPT import TwoOPT

from tkinter import ttk

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
import matplotlib.pyplot as plt
import csv
from opencity import openCity

LARGE_FONT = ("Verdana", 12)

DELTA= 300
REFUND=5



class CoveringTravellingSalesmanProblem(tk.Tk):



    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default="")
        tk.Tk.wm_title(self, "Covering Travelling Salesman Problem")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in ([GraphPage]):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(GraphPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class GraphPage(tk.Frame):
    GAPath = []
    GARevenue = 0
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # To remove and replace with openCity class

        node_array = []

        with open('Berlin52.txt', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ')
            for row in reader:
                node_array.append([float(row[1]), float(row[2])])

        with open('population.txt', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                population = row

        population = np.array(population, dtype='float64')

        fullData = np.array(node_array)

        adjMatrix = self.calculateADJMatrix(fullData[:, :2])

        path = []

        cityList, population = openCity('Berlin52.txt', 'population.txt')

        # Initialize GUI components
        self.grid(padx=20, pady=20)
        self.columnconfigure(1, weight=1)
        # Buttons
        self.DisplayButtons(fullData, population, adjMatrix, cityList)
        # Slider
        self.DisplaySlider()

        self.drawGraph(fullData, path)

    def greedyButton(self, fullData, cityList, population):

        path, cost = greedy(cityList, DELTA, population, REFUND)
        self.drawGraph(fullData, [p.id for p in path])

        print("Done")

    # def twoOPT(self, fullData, adjMatrix, population):
    #     path = [13, 25, 46, 51, 28, 36, 32, 42, 11, 6, 30, 40, 10, 50, 13]
    #     ThreeOPTPath, ThreeOPTCost = ThreeOPT(fullData, adjMatrix, population, path, 120000)
    #     self.drawGraph(fullData, path)

    def twoOPTButton(self, fullData, population, cityList):
        greedyPath, greedyGain = greedy(cityList, DELTA, population, REFUND)

        TwoOPTPath, TwoOPTCost = TwoOPT(cityList,population,greedyPath,greedyGain,DELTA,REFUND)

        self.drawGraph(fullData, [p.id for p in TwoOPTPath])


    def threeOPTButton(self, fullData, cityList, population):
        greedyPath, greedyCost = greedy(cityList, DELTA, population, REFUND)

        ThreeOPTPath, ThreeOPTCost = ThreeOPT(cityList, greedyPath, greedyCost, DELTA, REFUND)

        self.drawGraph(fullData, [p.id for p in ThreeOPTPath])

    def GAButton(self, fullData, cityList, population):

        if not self.GAPath:
            self.GAPath, self.GARevenue = geneticAlgorithm(cities=cityList, population=population, popSize=30, eliteSize=20,
                                                 mutationRate=0.01,
                                                 generations=200)

        self.drawGraph(fullData, [p.id for p in self.GAPath])
    def GAtwoOPTButton(self, fullData, cityList, population):

        if not self.GAPath:
            self.GAPath, self.GARevenue = geneticAlgorithm(cities=cityList, population=population, popSize=30, eliteSize=20,
                                                 mutationRate=0.01,
                                                 generations=200)

        fitness = Fitness(route= self.GAPath, cities=cityList, delta=300, refund=5)

        self.GARevenue, vaccinatedPopulation = fitness.fullRouteRevenue()

        TwoOPTPath, TwoOPTCost = TwoOPT(cityList,population, self.GAPath,self.GARevenue,DELTA,REFUND)

        self.drawGraph(fullData, [p.id for p in TwoOPTPath])
    def GAthreeOPTButton(self, fullData, cityList, population):

        if not self.GAPath:
            self.GAPath, self.GARevenue = geneticAlgorithm(cities=cityList, population=population, popSize=30, eliteSize=20,
                                                 mutationRate=0.01,
                                                 generations=200)

        fitness = Fitness(route=self.GAPath, cities=cityList, delta=300, refund=5)

        self.GARevenue, vaccinatedPopulation = fitness.fullRouteRevenue()

        ThreeOPTPath, ThreeOPTCost = ThreeOPT(cityList, self.GAPath, self.GARevenue, DELTA, REFUND)

        self.drawGraph(fullData, [p.id for p in ThreeOPTPath])

    def DisplayButtons(self, fullData, population, adjMatrix, cityList):
        greedy = tk.Button(self, text='Greedy', command=lambda: self.greedyButton(fullData, cityList, population))
        twoOpt = tk.Button(self, text='2-OPT', command=lambda: self.twoOPTButton(fullData, population,cityList))
        threeOpt = tk.Button(self, text='3-OPT', command=lambda: self.threeOPTButton(fullData, cityList, population ))
        GA = tk.Button(self, text='GA', command=lambda: self.GAButton(fullData, cityList, population ))
        GA2OPT = tk.Button(self, text='GA + 2-OPT', command=lambda: self.GAtwoOPTButton(fullData, cityList, population ))
        GA3OPT = tk.Button(self, text='GA + 3-OPT', command=lambda: self.GAthreeOPTButton(fullData, cityList, population ))

        greedy.grid(row=0, column=0)
        twoOpt.grid(row=0, column=1)
        threeOpt.grid(row=0, column=2)

        separator = ttk.Separator(self, orient='horizontal')
        separator.grid(row=1, column=1, sticky="ew", ipadx=100)

        GA.grid(row=2, column=0)
        GA2OPT.grid(row=2, column=1)
        GA3OPT.grid(row=2, column=2)

        separator2 = ttk.Separator(self, orient='horizontal')
        separator2.grid(row=3, column=1, sticky="ew", ipadx=100)


    def DisplaySlider(self):
        DeltaSlider = tk.Scale(self, from_=0, to=100, length=600, orient=tk.HORIZONTAL)
        DeltaSlider.grid(row=4, column=1)

    def drawGraph(self, nodes, path):

        f = plt.figure(figsize=(5, 4))
        a = f.add_subplot(111)

        G = nx.DiGraph()
        for i in range(len(nodes)):
            G.add_node(i, pos=(nodes[i][0], nodes[i][1]))

        i = 0
        while i < (len(path) - 1):
            G.add_edge(path[i], path[i + 1])
            i += 1

        pos = nx.get_node_attributes(G, 'pos')
        nx.draw(G, pos, with_labels=True, cmap=plt.get_cmap('jet'))

        # create matplotlib canvas using figure `f` and assign to widget `window`
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        # get canvas as tkinter's widget and `gird` in widget `window`
        canvas.get_tk_widget().grid(row=5, column=1)

        # navigation toolbar
        toolbarFrame = tk.Frame(self)
        toolbarFrame.grid(row=6, column=1)
        toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)

    def calculateADJMatrix(self, nodes):
        adjMatrix = []
        for i in range(len(nodes)):
            row = []
            for j in range(len(nodes)):
                dist = np.linalg.norm(nodes[i] - nodes[j])
                row.append(dist)
            adjMatrix.append(row)
        return adjMatrix


app = CoveringTravellingSalesmanProblem()
app.mainloop()
