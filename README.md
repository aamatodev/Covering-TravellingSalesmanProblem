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

The data used are from [berlin52](https://github.com/pdrozdowski/TSPLib.Net/blob/5cb1449963fa56176c062ff806eb831dcbc07c54/TSPLIB95/tsp/berlin52.tsp), adapted to CSP by generating a casual population tuple, saved on the `population.txt` file.

We assumed that:
* Villages connections are represented by a [complete graph](https://en.wikipedia.org/wiki/Complete_graph) G=(N,A);
* Distances between villages are [euclidean](https://en.wikipedia.org/wiki/Euclidean_distance);
* Every village can be covered just once by itself or another village. *NOTE*: this way the result strongly depends on the order in which villages are visited. This is a wrong interpretation of the problem, used to simplify it. Consider to correct this problem;

The default values are: c=1 unit/Km, r=5 unit/person, Delta=300 Km

## Usage

The whole program is written in Python, so make sure to have it installed on your system. Find more information [here](https://wiki.python.org/moin/BeginnersGuide/Download).

After Python is installed, you can clone the repository and move to its folder, by opening a Terminal and typing `cd path-to-repository`. Remember that `path-to-repository` must be your own path to the repository.

From there, type `python gui.py` and press Enter. After that, the Graphical Interface (GUI) will appear, like here:

<img width="382" alt="CSP_first" src="https://github.com/alesordo/Covering-Salesman-Problem/assets/85616887/3e345ef9-0351-4d78-aa39-0208e717feea">

If some libraries are missing install them using `pip install name-of-the-library`.

From the GUI, choose one of the possible solvers by pressing the top buttons and watch the results. On the GUI you'll see the path, while on the terminal total gain (profit) and other useful information. A detailed explanation of the solution is provided below.

## Solution explanation

Various Operations Research techniques can be used to solve the problem, here are the ones you can run on our program.

### Greedy

A [Greedy](https://en.wikipedia.org/wiki/Greedy_algorithm) solution is often a good starting point in optimization problems. The algorithm you run by pressing `Greedy` is very similar to a ["Nearest Neighbor"](https://en.wikipedia.org/wiki/Nearest_neighbor_search). In fact, starting from the initial node, it looks for every adjacent node (since the graph is complete all the nodes are adjacent) and chooses the one not yet covered that can give the maximum gain.

This solution is obviously not optimal and the last chosen nodes of the CSP are isolated and distant from the others. This is very common in Greedy Algorithms, as the initial choices are locally optimal, but the last ones are low quality.

### 2-opt

A more optimized solution than the Greedy one can be achieved by applying local search algorithms, such as 2-opt. 2-opt consists in removing two non-adjacent arcs from the Greedy CSP solution (which is a cycle) and reconnecting the nodes while maintaining the cycle, so with crossing arcs.

The application of Greedy + 2-opt can be tested by pressing `2-OPT` and gives a slightly better solution than just Greedy. The time complexity of the solution is $O(n*m^3)$, where $n$ is the total number of villages and $m$ the number of villages in the Greedy solution.

### 3-opt

As the name suggests, it's another local search algorithm. The principle is similar to the 2-opt, but in this case three non-adjacent arcs are removed. The possible combinations to reconnect the nodes while keeping the cycle are 7:

![image](https://github.com/alesordo/Covering-Salesman-Problem/assets/85616887/6f7c3385-40eb-434c-bd2e-d279c1711ce7)

To test the results just press `3-OPT` on the GUI. This and the next solution could take much more time. In fact, the time complexity of this solution is $O(m*n^4)$, where $n$ is the total number of villages and $m$ the number of villages in the initial CSP.

### Genetic algorithm


