# The code for changing pages was derived from: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# License: http://creativecommons.org/licenses/by-sa/3.0/

import matplotlib
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pylab

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

import tkinter as tk
from tkinter import ttk

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

        f = plt.figure(figsize=(6, 6))

        G = nx.DiGraph()

        G.add_edges_from([('A', 'B'), ('C', 'D'), ('G', 'D')], weight=1)
        G.add_edges_from([('D', 'A'), ('D', 'E'), ('B', 'D'), ('D', 'E')], weight=2)
        G.add_edges_from([('B', 'C'), ('E', 'F')], weight=3)
        G.add_edges_from([('C', 'F')], weight=4)

        val_map = {'A': 1.0,
                   'D': 0.5714285714285714,
                   'H': 0.0}

        values = [val_map.get(node, 0.45) for node in G.nodes()]
        edge_labels = dict([((u, v,), d['weight'])
                            for u, v, d in G.edges(data=True)])
        red_edges = [('C', 'D'), ('D', 'A')]
        edge_colors = ['black' if not edge in red_edges else 'red' for edge in G.edges()]

        pos = nx.spring_layout(G)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        nx.draw(G, pos, node_color=values, node_size=1500, edge_color=edge_colors, edge_cmap=plt.cm.Reds)

        nx.draw_networkx(G, pos=pos)
        canvas = FigureCanvasTkAgg(f, self)

        canvas.draw()
        canvas.get_tk_widget().grid(row=2, column=1)  # ERROR Tk.


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


app = CoveringTravellingSalesmanProblem()
app.mainloop()
