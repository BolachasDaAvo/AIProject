import math
import pickle
import time
import copy
import matplotlib.pyplot as plt

class Node:

    def __init__(self, number, parent, g, h, tickets):
        self.number = number
        self.parent = parent
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
        self.agents = [[] for i in range(len(goal))]

    def calcHeuristic(self, n, goal, tickets):
        # Discovers what type of station it is
        station = 0
        for route in self.model[n]:
            if route[0] > station and tickets[route[0]] > 1:
                station = route[0]

        return math.floor(distance(self.auxheur[n - 1], self.auxheur[goal - 1]) / averageCost[station])

    def expandNode(self, node, agent):
        for route in self.model[node.number]:

            transp = route[0]
            n = route[1]

            #Node is parent node
            if n == node.parent.number:
                continue

            #We dont have enough tickets to travel
            if node.tickets[transp] < 1:
                continue

            tickets = [*(node.tickets)]
            tickets[transp] -= 1

            g = node.g + 1

            h = self.calcHeuristic(n, self.goal[agent], tickets)

            self.agents[agent].append(Node(n, node, g, h, tickets))

    def search(self, init, limitexp=2000, limitdepth=10, tickets=[math.inf, math.inf, math.inf]):

        solution = {}
        selection = []
        baseNode = Node(0, 0, 0, 0, [])

        #Initializes agents and selection list
        for agent in range(len(init)):
            h = self.calcHeuristic(init[agent], self.goal[agent], tickets)
            newNode = Node(init[agent], baseNode, 0, h, tickets)
            self.agents[agent].append(newNode)
            selection.append(newNode)

        finished = [False for i in range(len(self.agents))]

        while False in finished:

            for agent in range(len(self.agents)):
                #Gets node with least f
                node = self.agents[agent][0]
                for x in self.agents[agent]:
                    if x.f < node.f:
                        node = x
                self.agents[agent].remove(node)

                #We reached the goal
                if node.number == self.goal[agent]:
                    solution[agent] = []

                    #Trace path
                    while node.parent.number != 0:
                        # Find Used ticket
                        usedTicket = 0
                        ticketsp = node.parent.tickets
                        for i in range(3):
                            if (ticketsp[i] > node.tickets[i]):
                                usedTicket = i
                                break
                        solution[agent] += [[[i], [node.number]]]
                        node = node.parent
                    solution[agent] += [[[], [node.number]]]
                    solution[agent].reverse()
                    ##print("foram gerados %d nos" % len(openNodes))
                    finished[agent] = True

                limitexp -= 1
                if limitexp < 0:
                    print("limite de expansoes atingido")
                    return []

                if node.g == limitdepth:
                    print("Limte de profundidade atingido")
                    return []

                self.expandNode(node, agent)

        return solution









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

def plotpath(P,coords):
        img = plt.imread('maps.png')
        plt.imshow(img)
        colors = ['r.-','g+-','b^-']
        I = P[0][1]
        for agind in range(len(P[0][1])):
                st = I[agind]-1
                for tt in P:
                        nst = tt[1][agind]-1
                        plt.plot([coords[st][0],coords[nst][0]],[coords[st][1],coords[nst][1]],colors[agind])
                        st = nst
        plt.axis('off')
        fig = plt.gcf()
        fig.set_size_inches(1.*18.5, 1.*10.5)
        fig.savefig('test2png.png', dpi=100)
        plt.show()

def validatepath(oP,oI,U,tickets=[25,25,25]):
        print(oP)
        if not oP:
                return False
        P = copy.deepcopy(oP)
        I = copy.copy(oI)
        mtickets = copy.copy(tickets)

        print(I)
        print(P[0][1])
        if I!=P[0][1]:
                print('path does not start in the initial state')
                return False
        del P[0]

        for tt in P:
                for agind,ag in enumerate(tt[1]):
                        #print(ag)
                        st = I[agind]
                        if mtickets[tt[0][agind]]==0:
                                print(tt)
                                print('no more tickets')
                                return False
                        else:
                                mtickets[tt[0][agind]] -= 1

                                if [tt[0][agind],ag] in U[st]:
                                        I[agind] = ag
                                        #pass
                                else:
                                        print(tt,agind)
                                        print('invalid action')
                                        return False
                if(len(set(I))<3) and len(I)==3:
                        print(tt)
                        print('there is more than one police in the same location')
                        return False
        print(oP)
        return True

distance = lambda t1, t2 : math.sqrt((t2[0] - t1[0])**2 + (t2[1] - t1[1])**2)

with open("coords.pickle", "rb") as fp:   # Unpickling
    coords = pickle.load(fp)

with open("mapasgraph2.pickle", "rb") as fp:  # Unpickling
    AA = pickle.load(fp)
M = AA[1]

tinit = time.process_time()

averageCost = calcAverageCostTransp(coords, M)
print(averageCost)

I = [28, 13]

#Taxi = linhas brancas; Autocarro = linhas azuis; Metro = linhas vermelhas
SP = SearchProblem([85, 50], M, coords)
SOL = SP.search(I, tickets = [5, 5, 2])
print(SOL)

tend = time.process_time()

if validatepath(SOL, I, M):
    print("path")
    print(SOL)
    plotpath(SOL, coords)
else:
    print("invalid path")

print(tend - tinit)
