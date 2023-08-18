# Covering Salesman Problem (CSP) Solver

Python project to determine, with Operations Research techniques, the best solution for a Covering Salesman Problem (CSP), aka [set TSP](https://en.wikipedia.org/wiki/Set_TSP_problem). CSPs are a generalization of the Traveling Salesman Problem and consist in finding the shortest tour in a graph in order to visit all specific subsets of the graph.

## Initial problem

The specific problem targeted by this program is the following: an NGO has to plan vaccinations in a rural area 🏚️:syringe:. People are willing to move to nearby villages within a certain number of kilometers ($Delta$) to get vaccines at specific hubs.

The **rules** are:
- Everybody must get vaccinated on site;
- Nobody can be vaccinated over the $Delta$ distance;
- If there's distance ($d$) between village and hub, the vaccinated people are, in percentage, $d/Delta$;
- Villages population and villages distances are known;
- The NGO receives a refund ($r$) for each vaccination;
- The NGO pays a cost ($c$) for each kilometer;
- The NGO must vaccinate at least 30% of all the people.

**Objective**: find a path (closed loop) to get maximum profit. Refund and Cost must be set so that visiting all the villages is not the optimum.

## Dataset, assumptions and defaults

The data used are from [berlin52](https://github.com/pdrozdowski/TSPLib.Net/blob/5cb1449963fa56176c062ff806eb831dcbc07c54/TSPLIB95/tsp/berlin52.tsp), adapted to CSP by generating a casual population tuple, saved on the `population.txt` file.

We assumed that:
* Villages connections are represented by a [complete graph](https://en.wikipedia.org/wiki/Complete_graph) G=(N,A);
* Distances between villages are [euclidean](https://en.wikipedia.org/wiki/Euclidean_distance);
* Every village can be covered just once by itself or another village. *NOTE*: this way the result strongly depends on the order in which villages are visited. This is a wrong interpretation of the problem, used to simplify it. Consider to correct this issue.

The default values are: $c$=1 unit/Km, $r$=5 unit/person, $Delta$=300 Km

## Usage

The whole program is written in Python, so make sure to have it installed on your system. Find more information [here](https://wiki.python.org/moin/BeginnersGuide/Download).

After Python is installed, you can clone the repository and move to its folder, by opening a Terminal and typing `cd path-to-repository`. Remember that `path-to-repository` must be your own path to the repository.

From there, type `python gui.py` and press Enter. After that, the Graphical Interface (GUI) will appear, like here:

<img width="382" alt="CSP_first" src="https://github.com/alesordo/Covering-Salesman-Problem/assets/85616887/3e345ef9-0351-4d78-aa39-0208e717feea">

If some libraries are missing install them using `pip install name-of-the-library`.

From the GUI, choose one of the possible solvers by clicking the top buttons and watch the results. On the GUI you'll see the path, while on the terminal the total gain (profit) and other useful information. A detailed explanation of the solutions is provided below.

## Solutions explanation

Various Operations Research techniques can be used to solve the problem, here are the ones you can run on our program.

### Greedy

A [Greedy Algorithm](https://en.wikipedia.org/wiki/Greedy_algorithm) is often a good starting point in optimization problems. The algorithm you run by pressing `Greedy` is very similar to a ["Nearest Neighbor"](https://en.wikipedia.org/wiki/Nearest_neighbor_search). In fact, starting from the initial node, it looks for every adjacent node (since the graph is complete all the nodes are adjacent) and chooses the one not yet covered that can give the maximum gain.

The solution returned is obviously not optimal and the last chosen nodes of the CSP are isolated and distant from the others. This is very common in Greedy Algorithms, as the initial choices are locally optimal, but the last ones are low quality.

### 2-opt

A more optimized solution than the Greedy one can be achieved by applying local search algorithms, such as 2-opt. 2-opt consists in removing two non-adjacent arcs from the Greedy CSP solution (which is a cycle) and reconnecting the nodes while maintaining the cycle, so with crossing arcs.

The application of Greedy + 2-opt can be run by clicking `2-OPT` and gives a slightly better result than just Greedy. The time complexity of the solution is $O(n*m^3)$, where $n$ is the total number of villages and $m$ the number of villages in the initial CSP.

### 3-opt

As the name suggests, it's another local search algorithm. The principle is similar to the 2-opt, but in this case three non-adjacent arcs are removed. The possible combinations to reconnect the nodes while keeping the cycle are 7:

![3-opt explanation](https://github.com/alesordo/Covering-Salesman-Problem/assets/85616887/6f7c3385-40eb-434c-bd2e-d279c1711ce7)

To see this algorithm at work just click `3-OPT` on the GUI. This and the next solution could take much more time than Greedy or 2-opt. In fact, the time complexity of this solution is $O(m*n^4)$, where $n$ is the total number of villages and $m$ the number of villages in the initial CSP.

### Genetic algorithm (GA)

A different approach that starts from generating random solutions with some requirements and applies the principles of natural selection. It's a metaheuristic that belongs to the class of Evolutionary Algorithms. To test the algorithm click `GA` on the GUI. **Be careful**, it could take long and also freeze your machine.

#### Parameters

- Initial population (initial number of solutions) = 30;
- Elite size = 20;
- Mutation rate = 0.01;
- Number of generations = 200.

The default parameters can be changed by editing them in the `gui.py` file. Look for `geneticAlgorithm()`.

#### Steps

1. Initial population generation;
2. Population ranking;
3. Mating pool selection;
4. Crossover;
5. Mutations;
6. Local Search to remove unnecessary nodes and adding nodes if covered population is < 30%.

##### 1. Initial population generation

To create a population of solutions that follows the initial rules we choose a random percentage between 30% and 99%, in order to vaccinate at least 30% of all the people. The nodes that are part of the solution are also chosen randomly, until the random percentage of vaccinated people is met.

**Note**: every node is chosen just once and we excluded 100% of people, because in that case all the nodes would be included in the CSP.

##### 2. Population ranking

The fitness function simply determines the net gain after costs. Solutions are ranked in decreasing order, from best to worst fit.

##### 3. Mating pool selection

Mating pooling means choosing the parents to create next generations. To choose the parents we used **fitness proportionate selection** or "roulette wheel selection", which you can visualize below.

![roulette](https://github.com/alesordo/Covering-Salesman-Problem/assets/85616887/cf3a1e7b-4e02-4797-ab8a-30467b81631f)

Also, **elitism** was applied, meaning that the best elements from the previous generation are always kept to create the next one. The number of elements chosen depends on the Elite size, [20 in this case](#parameters).

##### 4. Crossover

Crossover is the actual creation of new solutions from the ones chosen in the previous step. A standard crossover can't be used, as in any CSP a node can appear just once. So we do the following **Ordered crossover**:

1. Select a random length sub-string from the first parent;
2. Add all the elements of the second parent that aren't present yet.

##### 5. Mutations

In our case mutations are random swappings between cities in the CSP solution. Since the visiting order is crucial for the fitness function, swapping nodes can randomly improve a CSP.

The swapping is triggered if a random number is less than what we've set as [mutation rate](#parameters).

##### 6. Local Search

After all the GA generations, a Local Search (LS) is performed on the best solution to **avoid**:

- A non-optimized visiting order of nodes in the resulting CSP;
- Nodes that cover only themselves;
- A CSP that doesn't cover at least 30% of population.

The LS has three steps:

1. 2-opt to optimize the visting order;
2. Removal of unnecessary nodes. It always leads to an improvement, due to the [Triangle inequality](https://en.wikipedia.org/wiki/Triangle_inequality). In fact, removing a node deletes two arcs and creates a new arc shorther than the sum of the two removed;
3. If the covered population is < 30%, greedy search of the best nodes until the 30% quota is met.

### GA with 2-opt or 3-opt

They can be called by clicking `GA + 2-OPT` or `GA + 3-OPT`. These two approaches have already been explained individually. Their merging could lead to further improvements on the results, but we didn't track their performances due to a lack of time.

## Results

The profit varies as follows with the different approaches:

![results](https://github.com/alesordo/Covering-Salesman-Problem/assets/85616887/c89f76fb-8f8f-4873-84c3-a7494c788f01)

The GA gave the best results. Note that the best result overall was achieved by applying LS and 2-opt after each step. While this is not on the code, you can test it with a simple edit.

## Improvements

Some of the improvements to develop are:
- Changing function to calculate the revenue. As for now, it has a $O(n)$ time complexity, that leads to a heavy resources usage;
- Finding a compromise between the total number of people and the number of generations for the GA;
- Test the results with different values of $Delta$, $c$ and $r$.

## Credits

This project was developed by Alessandro Amato (@aleama98) and Alessio Sordo (@alesordo), both students from the University of Ferrara (Italy) 💻
