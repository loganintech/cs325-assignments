from pulp import *

prob = LpProblem("Maximizing Acme Profits", LpMaximize)

silk_yards = LpVariable("Silk Yards", lowBound=0, upBound=1_000)
polyester_yards = LpVariable("Polyester Yards", lowBound=0, upBound=2_000)
cotton_yards = LpVariable("Cotton Yards", lowBound=0, upBound=1_250)


units_of_silk = LpVariable("Units of Silk", lowBound=6_000, upBound=7_000)
units_of_poly = LpVariable("Units of Poly", lowBound=10_000, upBound=14_000)
units_of_bone = LpVariable("Units of Blend1", lowBound=13_000, upBound=16_000)
units_of_btwo = LpVariable("Units of Blend2", lowBound=6_000, upBound=8_500)


# (selling_price_of_tie*ties_sold - labor_for_tie*ties_sold - combined_material_cost)
prob += ((6.7 * units_of_silk) - (units_of_silk * .75) - (silk_yards * 20))\
    + ((3.55 * units_of_poly) - (units_of_poly * .75) - (polyester_yards * 6))\
    + ((4.31 * units_of_bone) - (units_of_bone * .75) - ((polyester_yards * 3) + (cotton_yards * 4.5)))\
    + ((4.81 * units_of_btwo) - (units_of_btwo * .75) -
       ((polyester_yards * (.3 * 6)) + (cotton_yards * (.7 * 9)))), "Total Profit"

# The units of silk * the yards used should equal the yards
prob += units_of_silk * .125 == silk_yards
# The units of poly * yards used in poly ties + units of b1 * yards of poly in b1 + units of b2 * yards of poly in p2 should equal poly yards
prob += ((units_of_poly * .08) + (units_of_bone * .05) +
         (units_of_btwo * .03)) == polyester_yards
# The units of b1 * yards cotton used in b1 + units of b2 * yards cotton used in b2 should equal cotton yards used
prob += (units_of_bone * .05) + (units_of_btwo * .07) == cotton_yards

prob.solve()
print(LpStatus[prob.status])
print(value(prob.objective))
for v in prob.variables():
    print(v.name, "=", v.varValue)
