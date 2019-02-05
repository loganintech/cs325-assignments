# costs = [0, 150, 200, 295, 375, 480, 620]
# costs = [1, 3, 10, 12, 8, 13, 6]
costs = [2, 2, 3, 4]

def lowest_cost(costs):


    if len(costs) == 1:
        return costs[0]


    modified_costs = costs[1:]

    min_val =  min([(cost + lowest_cost(modified_costs[idx:])) for idx, cost in enumerate(modified_costs)])

    return min_val


def lecture_lowest(costs):
    complexity = 0
    computed_costs = [0]
    for j in range(1, len(costs) - 1):
        computed_costs.append(1000000000)
        for i in range(0, j):
            complexity += 1
            computed_costs[j] = min(computed_costs[i] + (costs[j] - costs[i]), computed_costs[j])


    return computed_costs, complexity



comp, complexity = lecture_lowest(costs)
print("Lowest cost {}\nComplexity: {}".format(comp, complexity))
