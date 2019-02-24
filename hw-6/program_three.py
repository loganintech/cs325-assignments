from pulp import *
import networkx as nx
import pprint

g = nx.DiGraph()
plants = ["P1", "P2", "P3", "P4"]

for p in plants:
    g.add_node(p)

warehouses = ["W1", "W2", "W3"]
for w in warehouses:
    g.add_node(w)

retailers = [
    "R1",
    "R2",
    "R3",
    "R4",
    "R5",
    "R6",
    "R7",
]

for r in retailers:
    g.add_node(r)


g.add_edge("P1", "W1", weight=10)
g.add_edge("P1", "W2", weight=15)
g.add_edge("P2", "W1", weight=11)
g.add_edge("P2", "W2", weight=8)
g.add_edge("P3", "W1", weight=13)
g.add_edge("P3", "W2", weight=8)
g.add_edge("P3", "W3", weight=9)
g.add_edge("P4", "W2", weight=14)
g.add_edge("P4", "W3", weight=8)

g.add_edge("W1", "R1", weight=5)
g.add_edge("W1", "R2", weight=6)
g.add_edge("W1", "R3", weight=7)
g.add_edge("W1", "R4", weight=10)
g.add_edge("W2", "R3", weight=12)
g.add_edge("W2", "R4", weight=8)
g.add_edge("W2", "R5", weight=10)
g.add_edge("W2", "R6", weight=14)
g.add_edge("W3", "R4", weight=14)
g.add_edge("W3", "R5", weight=12)
g.add_edge("W3", "R6", weight=12)
g.add_edge("W3", "R7", weight=6)

prob = LpProblem("Minimizing Cost Transhipment", LpMinimize)
cost = nx.get_edge_attributes(g, "weight")
intermediate_costs = {}
total_costs = {}
for (frm, to, weight) in g.edges.data():
    # print(frm, to, weight)
    if frm.startswith("P"):
        intermediate_costs[frm, to] = weight
    else:
        for (p, w) in intermediate_costs:
            if w == frm:
                total_costs[p, to] = intermediate_costs[p,
                                                        w]["weight"] + weight["weight"]


routes = [(p, r) for (p, r) in total_costs.keys()]
route_vars = LpVariable.dicts("Route", routes, 0, None, LpInteger)


supply = {
    "P1": 150,
    "P2": 450,
    "P3": 250,
    "P4": 150,
}

demand = {
    "R1": 100,
    "R2": 150,
    "R3": 100,
    "R4": 200,
    "R5": 200,
    "R6": 150,
    "R7": 100,
}

pprint.pprint(routes)
pprint.pprint(route_vars)
pprint.pprint(total_costs)

prob += lpSum([route_vars[i, j]*total_costs[i, j]
               for i, j in routes]), "Sum of Transporting Costs"

for plant in plants:
    collector = 0
    for retailer in retailers:
        if (plant, retailer) in route_vars:
            collector += route_vars[plant, retailer]

    prob += collector <= supply[plant]

for retailer in retailers:
    collector = 0
    for plant in plants:
        if (plant, retailer) in route_vars:
            collector += route_vars[plant, retailer]

    prob += collector >= demand[retailer]


prob.solve()
print(LpStatus[prob.status])
print(value(prob.objective))
for v in prob.variables():
    print(v.name, "=", v.varValue)
