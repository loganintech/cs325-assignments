import sys
import pprint


def load_file(name):
    graph = {}
    with open(name, "r") as f:
        lines = [x.strip() for x in f.readlines()]
        for line in range(1, int(lines[0]) + 1):
            graph[lines[line]] = {"team": "", "neighbors": []}
        for line in range(int(lines[0]) + 2, int(lines[0]) + 2 + int(lines[int(lines[0]) + 1])):
            line = lines[line].split(" ")
            graph[line[0]]["neighbors"].append(line[1])
            graph[line[1]]["neighbors"].append(line[0])

        graph[lines[1]]["team"] = TEAMS[0]
        return graph, lines[1]


TEAMS = ["Babyfaces", "Heels"]


def pick_unassigned(graph):
    for vertex in graph:
        if graph[vertex]["team"] == "":
            return vertex


def all_assigned(graph, neighbors):
    for neighbor in neighbors:
        if graph[neighbor]["team"] == "":
            return False
    return True


VALID_BFS = True


def attempt_one(graph, verticies):
    global VALID_BFS
    # For every location we want to check
    for key in verticies:
        # For every one of the neighbors
        for neighbor in graph[key]["neighbors"]:
            # Check to see if the neighbor has an assigned team. If it doesn't, assign it to the opposite of this key
            if graph[neighbor]["team"] == "":
                graph[neighbor]["team"] = TEAMS[TEAMS.index(
                    graph[key]["team"]) ^ 1]
            # If it does, check to make sure it's compatible with this key. If it isn't, exit with false
            elif graph[neighbor]["team"] == graph[key]["team"]:
                VALID_BFS = False

    for key in verticies:
        for neighbor in graph[key]["neighbors"]:
            if not all_assigned(graph, graph[neighbor]["neighbors"]):
                return attempt_one(graph, graph[key]["neighbors"])

    return graph, True


def breadth_first(graph, first_node):
    global VALID_BFS
    queue = []
    queue.append(first_node)
    graph[first_node]["team"] = TEAMS[0]

    while len(queue) > 0:
        node = queue.pop(0)
        for neighbor in graph[node]["neighbors"]:
            if graph[neighbor]["team"] == "":
                queue.append(neighbor)
                graph[neighbor]["team"] = TEAMS[TEAMS.index(
                    graph[node]["team"]) ^ 1]
            elif graph[neighbor]["team"] == graph[node]["team"]:
                VALID_BFS = False

    return graph


if __name__ == "__main__":
    args = sys.argv
    if len(args) < 2:
        print("You need to pass a filename to load!")
        exit(1)

    graph, first_key = load_file(args[1])
    result_graph = breadth_first(graph, first_key)

    while not all_assigned(result_graph, result_graph.keys()):
        starting_key = pick_unassigned(result_graph)
        result_graph = breadth_first(result_graph, starting_key)

    # pprint.pprint(result_graph)

    babyfaces = []
    heels = []

    for key in result_graph:
        if TEAMS.index(result_graph[key]["team"]) == 0:
            babyfaces.append(key)
        else:
            heels.append(key)
    if VALID_BFS:

        print("Yes it's possible!")
        print("Babyfaces: " + " ".join(babyfaces))
        print("Heels: " + " ".join(heels))
    else:
        print("No it's not possible.")
