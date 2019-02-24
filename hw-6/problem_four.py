from pulp import *

coins_a = [1, 5, 10, 25]
coins_b = [1, 3, 7, 12, 27]
a_goal = 202
b_goal = 293


proba = LpProblem("Minimizing Coin Usage", LpMinimize)
coins = [LpVariable("Value %s Coin" % val, lowBound=0,
                    cat=LpInteger) for val in coins_a]
proba += lpSum(coins), "Total Coin Use"
proba += lpSum([val * coins_a[idx]
                for idx, val in enumerate(coins)]) == a_goal

proba.solve()
print(LpStatus[proba.status])
print(value(proba.objective))
for v in proba.variables():
    print(v.name, "=", v.varValue)


proba = LpProblem("Minimizing Coin Usage", LpMinimize)
coins = [LpVariable("Value %s Coin" % val, lowBound=0,
                    cat=LpInteger) for val in coins_b]
proba += lpSum(coins), "Total Coin Use"
proba += lpSum([val * coins_b[idx]
                for idx, val in enumerate(coins)]) == b_goal
proba.solve()
print(LpStatus[proba.status])
print(value(proba.objective))
for v in proba.variables():
    print(v.name, "=", v.varValue)
