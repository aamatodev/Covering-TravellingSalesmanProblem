# Covering Salesman Problem (CSP) Solver

Python project to determine, with Operations Research techniques, the best solution of a Covering Salesman Problem (CSP). CSPs are a generalization of the Traveling Salesman Problem, known also as [set TSP](https://en.wikipedia.org/wiki/Set_TSP_problem). They consist in finding the shortest tour in a graph in order to visit all specific subsets of the graph.

## Initial problem

The specific problem targeted by this program is the following: an NGO has to plan vaccinations in a rural area :syringe:. People are willing to move to nearby villages within a certain number of kilometers (Delta) to get vaccines at specific hubs.

The **rules** are:
- Everybody must get vaccinated on site;
- Nobody can be vaccinated over the Delta distance;
- If there's distance (d) between village and hub, the vaccinated people are, in percentage, d/Delta;
- Villages population and villages distances are known;
- The NGO receives a refund (r) for each vaccination;
- The NGO pays a cost (c) for each kilometer;
- The NGO must vaccinate at least 30% of all the people.

**Objective**: find a path (closed loop) to get maximum profit. Refund and Cost must be set so that visiting all the villages is not the optimum.

## Data, assumptions and defaults

The data used are from [berlin52](https://github.com/pdrozdowski/TSPLib.Net/blob/5cb1449963fa56176c062ff806eb831dcbc07c54/TSPLIB95/tsp/berlin52.tsp), adapted to CSP by generating a casual population tuple, save on the `population.txt` file.

We assumed that:
* Villages connections are represented by a [complete graph](https://en.wikipedia.org/wiki/Complete_graph) G=(N,A);
* Distances between villages are [euclidean](https://en.wikipedia.org/wiki/Euclidean_distance);
* Every village can be covered just once by itself or another village. *NOTE*: this way the result strongly depends on the order in which villages are visited. This is a wrong interpretation of the problem, used to simplify it. Consider to correct this problem;

The default values are: c=1 unit/Km, r=5 unit/person, Delta=300 Km

## Usage

The whole program is written in Python, so make sure to have it installed on your system. Find more information [here](https://wiki.python.org/moin/BeginnersGuide/Download).

After Python is installed, you can clone the repository and move to its folder, by opening a Terminal and typing `cd path-to-repository`. Remember that `path-to-repository` must be your own path to the repository.

From there, type `python gui.py`. After that, the Graphical Interface will appear, like here:

