import os

import matplotlib
import networkx as nx
import numpy as np
from random import randint

from greedy import greedy
from threeOPT import ThreeOPT

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
        self.drawGraph(fullData, path)

        print("Done")

    def twoOPT(self, fullData, adjMatrix, population):
        path = [13, 25, 46, 51, 28, 36, 32, 42, 11, 6, 30, 40, 10, 50, 13]
        ThreeOPTPath, ThreeOPTCost = ThreeOPT(fullData, adjMatrix, population, path, 120000)
        self.drawGraph(fullData, path)

    def twoOPTButton(self, fullData, population, cityList):
        greedyPath, greedyCost = greedy(cityList, DELTA, population, REFUND)


    def threeOPTButton(self, fullData, adjMatrix, population, cityList):
        greedyPath, greedyCost = greedy(cityList, DELTA, population, REFUND)

        ThreeOPTPath, ThreeOPTCost = ThreeOPT(fullData, adjMatrix, population, greedyPath, greedyCost)

        self.drawGraph(fullData, ThreeOPTPath)

    def DisplayButtons(self, fullData, population, adjMatrix, cityList):
        greedy = tk.Button(self, text='Greedy', command=lambda: self.greedyButton(fullData, cityList, population))
        twoOpt = tk.Button(self, text='2-OPT', command=lambda: self.twoOPT(fullData, cityList, population))
        threeOpt = tk.Button(self, text='3-OPT', command=lambda: self.threeOPTButton(fullData, adjMatrix, population, cityList))

        twoOpt.grid(row=0, column=1)
        greedy.grid(row=0, column=0)
        threeOpt.grid(row=0, column=2)

    def DisplaySlider(self):
        DeltaSlider = tk.Scale(self, from_=0, to=100, length=600, orient=tk.HORIZONTAL)
        DeltaSlider.grid(row=1, column=1)

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
        canvas.get_tk_widget().grid(row=2, column=1)

        # navigation toolbar
        toolbarFrame = tk.Frame(self)
        toolbarFrame.grid(row=3, column=1)
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
