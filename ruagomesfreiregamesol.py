import math
import pickle
import time
import copy
import matplotlib.pyplot as plt
from itertools import product

class Node:

    def __init__(self, positions, transports, parent, g, tickets):
        self.positions = positions
        self.transports = transports
        self.parent = parent
        self.h = 0
        self.g = g
        self.f = g
        self.tickets = tickets

    def updateF(self, h):
        self.f = self.g + h

class SearchProblem:

    def __init__(self, goal, model, auxheur=[]):
        self.goal = goal
        self.agents = len(goal)
        self.model = model
        self.auxheur = auxheur

    def calcHeuristic(self, node):

        heuristics = []

        for position in node.positions:

            # Discovers what type of station it is
            station = 0
            for route in self.model[position]:
                if route[0] > station and node.tickets[route[0]] > 0:
                    station = route[0]

            heurs = []

            for goal in self.goal:
                heurs += [min(distance(self.auxheur[position - 1], self.auxheur[goal - 1]) / averageCost[station], distance(self.auxheur[position - 1], self.auxheur[goal - 1]) / averageCostGlobal)]
            heuristics += [max(heurs)]

        return sum(heuristics)/self.agents

    def expandNode(self, node, openNodes):
        
        transitions = []

        # Expands nodes
        for position in node.positions:
            transitions += [self.model[position]]

        combinations = list(product(*transitions))

        # Parses list
        for route in combinations:

            hasCollision = False
            hasTickets = True
            didntMove = False
            positions = []
            transports = []

            # Check for collisions
            for i in range(self.agents - 1):
                for j in range(i + 1, self.agents):
                    if route[i][1] == route[j][1]:
                        hasCollision = True
            if hasCollision:
                continue

            # Check if there are enough tickets
            tickets = [*(node.tickets)]
            for transp in route:
                tickets[transp[0]] -= 1
                if tickets[transp[0]] < 0:
                    hasTickets = False
            if not hasTickets:
                continue
                    
            # Adds positions and transports to lists
            for agent in route:
                positions.append(agent[1])
                transports.append(agent[0])

            # Checks if it's parent node
            for i in range(self.agents):
                if positions[i] == node.positions[i]:
                    didntMove = True
            if didntMove:
                continue
            # Creates new node
            g = node.g + 1
            
            newNode = Node(positions, transports, node, g, tickets)

            h = self.calcHeuristic(newNode)

            newNode.updateF(h)

            openNodes.append(newNode)

    def isGoal(self, node):

        for i in range(self.agents):
            if node.positions[i] not in self.goal:
                return False

        return True

    def search(self, init, limitexp=2000, limitdepth=10, tickets=[math.inf, math.inf, math.inf]):

        baseNode = Node([], [], 0, 0, [])
        openNodes = []
        closedNodes = []

        #Initializes openNodes list
        startNode = Node(init, [], baseNode, 0, tickets)
        h = self.calcHeuristic(startNode)
        startNode.updateF(h)
        openNodes.append(startNode)

        while openNodes != []:
                
            # Gets node with least f
            node = openNodes[0]
            for x in openNodes:
                if x.f < node.f:
                    node = x
            openNodes.remove(node)
            closedNodes.append(node)

            # We reached the goal
            if self.isGoal(node):
                solution = []
                #Trace path
                while node.positions != init:
                    solution += [[node.transports, node.positions]]
                    node = node.parent
                solution += [[node.transports, node.positions]]
                solution.reverse()
                return solution

            limitexp -= 1
            if limitexp < 0:
                print("limite de expansoes atingido")
                return []

            if node.g == limitdepth:
                continue

            self.expandNode(node, openNodes)

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

    averageCostGlobal = sum(transpSum) / sum(transpNum)

    return [averageCost, averageCostGlobal]

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

averageCosts = calcAverageCostTransp(coords, M)
averageCost = averageCosts[0]
averageCostGlobal = averageCosts[1]
print(averageCosts)

I = [28]

#Taxi = linhas brancas; Autocarro = linhas azuis; Metro = linhas vermelhas
SP = SearchProblem([58], M, coords)
SOL = SP.search(I, tickets = [5, 5, 2])
print(SOL)

tend = time.process_time()

print("%.1fms"%((tend-tinit)*1000))
'''
if validatepath(SOL, I, M):
    print("path")
    print(SOL)
    plotpath(SOL, coords)
else:
    print("invalid path")

print(tend - tinit)
'''