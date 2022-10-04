# The code for changing pages was derived from: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# License: http://creativecommons.org/licenses/by-sa/3.0/

import matplotlib
import networkx as nx
import numpy as np
from random import randint

from greedy import greedy

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
import matplotlib.pyplot as plt
import csv

LARGE_FONT = ("Verdana", 12)


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

        # Initialize GUI components
        self.grid(padx=20, pady=20)
        self.columnconfigure(1, weight=1)
        # Buttons
        self.DisplayButtons()
        # Slider
        self.DisplaySlider()

        # Graph

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

        G = nx.DiGraph()
        for i in range(len(fullData)):
            G.add_node(i, pos=(fullData[i][0], fullData[i][1]))

        fig, ax = plt.subplots()
        ax.set_axis_on()

        ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)

        greedyPath = greedy(adjMatrix,300,population,5)

        i = 0
        while i < (len(greedyPath) - 1):
            G.add_edge(greedyPath[i], greedyPath[i + 1])
            i += 1

        pos = nx.get_node_attributes(G, 'pos')
        nx.draw(G, pos, with_labels=True, cmap=plt.get_cmap('jet'))

        plt.show()

    #    f = plt.figure(figsize=(6, 6))

    #  self.drawGraph(fullData[:, :2], np.array(test))

    def DisplayButtons(self):
        greedy = tk.Button(self, text='Greedy')
        twoOpt = tk.Button(self, text='2-OPT')
        ThreeOpt = tk.Button(self, text='3-OPT')

        greedy.grid(row=0, column=0)
        twoOpt.grid(row=0, column=1)
        ThreeOpt.grid(row=0, column=2)

    def DisplaySlider(self):
        DeltaSlider = tk.Scale(self, from_=0, to=100, length=600, orient=tk.HORIZONTAL)
        DeltaSlider.grid(row=1, column=1)

    def drawGraph(self, nodes, path):

        fig, ax = plt.subplots(2, sharex=True, sharey=True)  # Prepare 2 plots
        ax[0].set_title('Raw nodes')
        ax[1].set_title('Optimized tour')
        ax[0].scatter(nodes[:, 0], nodes[:, 1])  # plot A
        ax[1].scatter(nodes[:, 0], nodes[:, 1])  # plot B
        start_node = 0
        distance = 0.
        for i in range(len(path)):
            start_pos = nodes[path[i]]
            if (i + 1) < path.size:
                end_pos = nodes[path[i + 1]]
            else:
                end_pos = nodes[path[0]]
            # print(start_pos, " - ", end_pos)
            ax[1].annotate("",
                           xy=start_pos, xycoords='data',
                           xytext=end_pos, textcoords='data',
                           arrowprops=dict(arrowstyle="->",
                                           connectionstyle="arc3"))
            distance += np.linalg.norm(end_pos - start_pos)

        textstr = "N nodes: %d\nTotal length: %.3f" % (path.size, distance)
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        ax[1].text(0.05, 0.95, textstr, transform=ax[1].transAxes, fontsize=14,  # Textbox
                   verticalalignment='top', bbox=props)

        plt.tight_layout()
        plt.show()

        # canvas = FigureCanvasTkAgg(fig, self)

        # canvas.draw()
        # canvas.get_tk_widget().grid(row=2, column=1)  # ERROR Tk.

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
