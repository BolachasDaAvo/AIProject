import math
import pickle
import time
import copy
import matplotlib.pyplot as plt

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
                while node.p.n != 0:
                    # Find Used ticket
                    usedTicket = 0
                    ticketsp = node.p.tickets
                    for i in range(3):
                        if (ticketsp[i] > node.tickets[i]):
                            usedTicket = i
                            break
                    sol += [[[i], [node.n]]]
                    node = node.p
                sol += [[[], [node.n]]]
                sol.reverse()
                ##print("foram gerados %d nos" % len(openNodes))
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
                if q.tickets[transp] < 1:
                    continue

                tickets = [*(q.tickets)]
                tickets[transp] -= 1

                g = q.g + 1

                # Discovers what type of station it is
                station = 0
                for x in self.model[n]:
                    if x[0] > station and tickets[x[0]] > 1:
                        station = x[0]

                h = math.floor(distance(self.auxheur[n - 1], self.auxheur[goal - 1]) / averageCost[station])

                newNode = Node(n, q, g, h, tickets)
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

I = [28]

#Taxi = linhas brancas; Autocarro = linhas azuis; Metro = linhas vermelhas
SP = SearchProblem([85], M, coords)
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
