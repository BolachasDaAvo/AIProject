import math
import pickle
import time

class Node:

    def __init__(self, n, p, g, h, tickets):
        self.n = n
        self.p = p
        self.h = h
        self.g = g
        self.f = g + h
        self.tickets = tickets

    def remTicket(self, ticket):
        self.tickets[ticket] -= 1
        return self.tickets[ticket]

class SearchProblem:

    def __init__(self, goal, model, auxheur=[]):
        self.goal = goal
        self.model = model
        self.auxheur = auxheur

    def search(self, init, limitexp=2000, limitdepth=10, tickets=[math.inf, math.inf, math.inf]):

        sol = []
        openNodes = []
        closedNodes = []
        exp = limitexp
        depth = limitdepth
        g = 0
        h = 0
        goal = self.goal[0]
        baseNode = Node(0, 0, 0, 0, [])
        lastExpanded = 0

        for n in init:
            g = 0
            h = 0 
            startNode = Node(n, baseNode, 0, h, tickets) 
            openNodes += [startNode]

        while openNodes != []:

            #Gets node with least f
            q = openNodes[0]
            for x in openNodes:
                if x.f < q.f:
                    q = x
            openNodes.remove(q)
            closedNodes += [q]

            #We reached the goal
            if q.n == goal:

                #Trace path
                node = q
                while node.n != 0:
                    sol += [node.n]
                    node = node.p
                sol.reverse()
                print("foram gerados %d nos" % len(openNodes))
                return sol

            exp -= 1
            if exp < 0:
                print("limite de expansoes atingido")
                return []

            for x in self.model[q.n]:

                transp = x[0]                
                n = x[1]

                #Node is parent node
                if n == q.p.n:
                   continue

                #We dont have enough tickets to travel
                if tickets[transp] < 1:
                    continue

                tickets = [*(q.tickets)]
                tickets[transp] -= 1

                g = q.g + 1

                #Discovers what type of station it is
                station = 0
                for x in self.model[n]:
                    if x[0] > station and tickets[x[0]] > 1:
                        station = x[0]

                h = distance(self.auxheur[n - 1], self.auxheur[goal - 1]) / averageCost[station]

                newNode = Node(n, q, g, h, tickets)

                #Check if node is already in openNodes list and has a lower f
                flag = 0
                for x in openNodes:
                    if x.n == newNode.n and x.f < newNode.f:
                        if x.tickets[0] <= newNode.tickets[0] and x.tickets[1] <= newNode.tickets[1] and x.tickets[2] <= newNode.tickets[2]:
                            flag = 1
                            break
                if (flag):
                    print("skipped node %d" % newNode.n)
                    continue

                #Check if node is in closed list and has a lower f
                flag = 0
                for x in closedNodes:
                    if x.n == newNode.n and x.f < newNode.f:
                        if x.tickets[0] <= newNode.tickets[0] and x.tickets[1] <= newNode.tickets[1] and x.tickets[2] <= newNode.tickets[2]:
                            flag = 1
                            break
                if (flag):
                    print("skipped node %d" % newNode.n)
                    continue
                openNodes += [newNode]

        return []

def calcAverageCost(coords, M):

    edges = 0
    totalSum = 0

    processedEdges = []

    vertices = len(M)

    for i in range(1, vertices):
        for x in M[i]:
            if ((i, x[1]) or (x[1], i)) in processedEdges:
                continue
            processedEdges += (i, x[1])
            processedEdges += (x[1], i)
            edges += 1
            totalSum += distance(coords[i - 1], coords[x[1] - 1])

    return totalSum/edges

def calcAverageCostTransp(coords, map):

    transpNum = [0, 0, 0]
    transpSum = [0, 0, 0]
    averageCost = [0, 0, 0]

    vertices = len(map)

    for i in range(1, vertices):

        for x in map[i]:
            
            transp = x[0]
            vertex = x[1]
            transpNum[transp] += 1
            transpSum[transp] += distance(coords[i - 1], coords[vertex -1])

    for i in range(3):
        averageCost[i] = transpSum[i]/transpNum[i]

    return averageCost

distance = lambda t1, t2 : math.sqrt((t2[0] - t1[0])**2 + (t2[1] - t1[1])**2)

with open("coords.pickle", "rb") as fp:   # Unpickling
    coords = pickle.load(fp)

with open("mapasgraph2.pickle", "rb") as fp:  # Unpickling
    AA = pickle.load(fp)
M = AA[1]

tinit = time.process_time()

averageCost = calcAverageCostTransp(coords, M)
print(averageCost)

#Taxi = linhas brancas; Autocarro = linhas azuis; Metro = linhas vermelhas
SP = SearchProblem([85], M, coords)
SOL = SP.search([28], tickets = [5, 5, 2])
print(SOL)

tend = time.process_time()

print(tend - tinit)