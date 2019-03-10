from pulp import *

six_items = [4, 4, 4, 6, 6, 6]
s_bin_cap = 10

five_items = [20, 10, 15, 10, 5]
f_bin_cap = 20

items = ["item_{}".format(i) for i in range(len(five_items))]
sizes = dict(zip(items, five_items))
bin_cap = f_bin_cap

# # Uncomment to run the test on six items
# items = ["item_{}".format(i) for i in range(len(six_items))]
# sizes = dict(zip(items, six_items))
# bin_cap = s_bin_cap

bins = ["bin_{}".format(i) for i in range(len(items))]
x = LpVariable.dicts("x", [(i, b)
                           for i in items for b in bins], 0, 1, LpBinary)
y = LpVariable.dicts("bin", bins, 0, bin_cap, LpBinary)

prob = LpProblem("bin_packing", LpMinimize)
cost = lpSum([y[b] for b in bins])

prob += cost

for i in items:
    prob += lpSum([x[i, b] for b in bins]) == 1


for b in bins:
    prob += lpSum([sizes[i] * x[i, b] for i in items]) <= bin_cap * y[b]

prob.solve()
print(LpStatus[prob.status])
print(value(prob.objective))
