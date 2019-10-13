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
        gn = 0
        hn = 0

        goal = self.goal[0]

        for n in init:
            gn = 0
            hn = h(self.auxheur[n - 1], self.auxheur[goal - 1])
            startNode = Node(n, -1, gn, hn, tickets) 
            openNodes += [startNode]

        while openNodes != []:

            #Gets node with greater f
            q = openNodes[0]
            for x in openNodes:
                if x.f < q.f:
                    q = x
            openNodes.remove(q)

            for x in self.model[q.n]:

                transp = x[0]                
                n = x[1]

                gn = q.g + g(self.auxheur[q.n - 1], self.auxheur[n - 1])
                hn = h(self.auxheur[n - 1], self.auxheur[goal - 1])
                newNode = Node(n, q, gn, hn, q.tickets)

                if newNode.n == goal:

                    #Trace path
                    node = newNode
                    while node.p != -1:
                        sol += [node.n]
                        node = node.p
                    sol += [node.n]
                    sol.reverse()
                    return sol

                #We dont have enough tickets to travel
                if newNode.remTicket(transp) < 0:
                    continue

                #Check if node is already in openNodes list and has a greater f
                flag = 0
                for x in openNodes:
                    if x.n == newNode.n and x.f < newNode.f:
                        flag = 1
                        break
                if (flag):
                    continue

                #Check if node is in closed list and and has a greater h
                flag = 0
                for x in closedNodes:
                    if x.n == newNode.n and x.f < newNode.f:
                        flag = 1
                        break
                if (flag):
                    continue
                openNodes += [newNode]

            closedNodes += [q]

        return []

h = lambda t1, t2 : math.sqrt((t2[0] - t1[0])**2 + (t2[1] - t1[1])**2)
g = lambda t1, t2 : math.sqrt((t2[0] - t1[0])**2 + (t2[1] - t1[1])**2)

with open("coords.pickle", "rb") as fp:   # Unpickling
    coords = pickle.load(fp)

with open("mapasgraph.pickle", "rb") as fp:  # Unpickling
    AA = pickle.load(fp)
M = AA[1]

SP = SearchProblem([63], M, coords)
SOL = SP.search([30])
print(SOL)