def bellman_ford(graph, source):

    distance, predecessor = dict(), dict()
    for node in graph:
        distance[node], predecessor[node] = float('inf'), None
    distance[source] = 0


    for _ in range(len(graph) - 1):
        for node in graph:
            for neighbour in graph[node]:

                if distance[neighbour] > distance[node] + graph[node][neighbour]:
                    distance[neighbour]= distance[node] + graph[node][neighbour]
                    predecessor[neighbour] = node


    for node in graph:
        for neighbour in graph[node]:
            assert distance[neighbour] <= distance[node] + graph[node][neighbour], "Negative weight cycle."

    return distance, predecessor



graph = {
    'B': {'A': 5, 'D': 1, 'G': 2},
    'A': {'B': 5, 'D': 3, 'E': 12, 'F' :5},
    'D': {'B': 1, 'G': 1, 'E': 1, 'A': 3},
    'G': {'B': 2, 'D': 1, 'C': 2},
    'C': {'G': 2, 'E': 1, 'F': 16},
    'E': {'A': 12, 'D': 1, 'C': 1, 'F': 2},
    'F': {'A': 5, 'E': 2, 'C': 16}}

for i in graph:
    print(i, graph[i])

startowy = input("podaj od ktorego wezla zaczynamy ")
distance, predecessor = bellman_ford(graph, startowy)

print(distance)