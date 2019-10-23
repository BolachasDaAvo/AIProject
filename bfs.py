import math
import pickle
import time

with open("mapasgraph2.pickle", "rb") as fp:  # Unpickling
    AA = pickle.load(fp)

Graph = AA[1]

matrix = [[0 for x in range(len(Graph))] for y in range(len(Graph))]

def bfs(graph, start):

    visited = [False] * len(graph)
    depth = [0] * len(graph)
    queue = [start]
    node = 0
    visited[start] = True

    while queue:
        node = queue.pop(0)
        for vertex in graph[node]:
            if not visited[vertex[1]]:
                queue.append(vertex[1])
                visited[vertex[1]] = True
                depth[vertex[1]] = depth[node] + 1

    return depth


for i in range(1, len(Graph)):
    matrix[i] = bfs(Graph, i)

f = open("heuristic.txt", "w")
f.write(str(matrix))
f.close()
