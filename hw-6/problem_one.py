import sys
from pulp import *
import networkx as nx

lp_problem = LpProblem("Shortest Path Problem", LpMinimize)

graph = nx.DiGraph()
graph.add_node("A")
graph.add_node("B")
graph.add_node("C")
graph.add_node("D")
graph.add_node("E")
graph.add_node("F")
graph.add_edge("A", "B", weight=8)
graph.add_edge("A", "F", weight=10)
graph.add_edge("B", "C", weight=4)
graph.add_edge("B", "E", weight=10)
graph.add_edge("C", "D", weight=3)
graph.add_edge("D", "E", weight=25)
graph.add_edge("D", "F", weight=18)
graph.add_edge("E", "D", weight=9)
graph.add_edge("E", "G", weight=7)
graph.add_edge("F", "A", weight=5)
graph.add_edge("F", "B", weight=7)
graph.add_edge("F", "C", weight=3)
graph.add_edge("F", "E", weight=2)
graph.add_edge("G", "D", weight=2)
graph.add_edge("G", "H", weight=3)
graph.add_edge("H", "A", weight=4)
graph.add_edge("H", "B", weight=9)

cost = nx.get_edge_attributes(graph, "weight")

chosen_link_dict = {}
for (i, j) in graph.edges:
    x = LpVariable("x_(%s_%s)" % (i, j), cat=LpBinary)
    chosen_link_dict[i, j] = x

lp_problem += lpSum([cost[i, j] * chosen_link_dict[i, j]
                     for i, j in graph.edges]), "Total Hop Count"

source = "G"
dest = sys.argv[1]

# constraints
for node in graph.nodes:
    rhs = 0
    if node == source:
        rhs = -1
    elif node == dest:
        rhs = 1
    lp_problem += lpSum([chosen_link_dict[i, k] for i, k in graph.edges if k == node]) - \
        lpSum([chosen_link_dict[k, j]
               for k, j in graph.edges if k == node]) == rhs


lp_problem.solve()

print(LpStatus[lp_problem.status])
print(value(lp_problem.objective))
print("The shortest path is ")
for link in graph.edges:
    if chosen_link_dict[link].value() == 1.0:
        print(link, end=" ")
print()
