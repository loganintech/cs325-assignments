import heapq


def calculate_distances(graph, starting_vertex):
    distances = {vertex: float('infinity') for vertex in graph}
    distances[starting_vertex] = 0

    entry_lookup = {}
    pq = []

    for vertex, distance in distances.items():
        entry = [distance, vertex]
        entry_lookup[vertex] = entry
        heapq.heappush(pq, entry)

    while len(pq) > 0:
        current_distance, current_vertex = heapq.heappop(pq)

        for neighbor, neighbor_distance in graph[current_vertex].items():
            distance = distances[current_vertex] + neighbor_distance
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                entry_lookup[neighbor][0] = distance

    return distances


roads = {
    "A": {"C": 4, "F": 7},
    "C": {"A": 4, "F": 2, "G": 9, "D": 3},
    "F": {"A": 7, "G": 8, "C": 2},
    "D": {"C": 3, "G": 7, "E": 3},
    "G": {"F": 8, "H": 3, "D": 7, "C": 9, "E": 2},
    "E": {"B": 9, "D": 3, "G": 3, "H": 7},
    "H": {"E": 7, "G": 3, "B": 3},
    "B": {"E": 9, "H": 3}
}

for road in roads:
    distance = calculate_distances(roads, road)
    total = sum(distance.values())
    print("[{}] {}".format(road, total))
