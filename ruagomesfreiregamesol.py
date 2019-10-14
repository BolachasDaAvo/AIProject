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
        d = 0
        goal = self.goal[0]
        baseNode = Node(0, 0, 0, 0, [])

        for n in init:
            g = 0
            d = distance(self.auxheur[n - 1], self.auxheur[goal - 1])
            h = 1
            startNode = Node(n, baseNode, 0, h, tickets) 
            openNodes += [startNode]

        while openNodes != []:

            #Gets node with least f
            q = openNodes[0]
            for x in openNodes:
                if x.f < q.f:
                    q = x
            openNodes.remove(q)

            for x in self.model[q.n]:

                transp = x[0]                
                n = x[1]

                #Node is parent node
                if n == q.p.n:
                    continue

                if n == goal:

                    #Trace path
                    sol += [n]
                    node = q
                    while node.n != 0:
                        sol += [node.n]
                        node = node.p
                    sol.reverse()
                    return sol

                g = q.g + 1
                h = distance(self.auxheur[n - 1], self.auxheur[goal - 1]) / d
                newNode = Node(n, q, g, h, [*(q.tickets)])

                #We dont have enough tickets to travel
                if newNode.remTicket(transp) < 0:
                    continue

                #Check if node is already in openNodes list and has a lower f
                flag = 0
                for x in openNodes:
                    if x.n == newNode.n and x.tickets == newNode.tickets and x.f < newNode.f:
                        flag = 1
                        break
                if (flag):
                    continue

                #Check if node is in closed list and and has a lower f
                flag = 0
                for x in closedNodes:
                    if x.n == newNode.n and x.tickets == newNode.tickets and x.f < newNode.f:
                        flag = 1
                        break
                if (flag):
                    continue
                openNodes += [newNode]
                exp -= 1
                if exp < 0:
                    return []


            closedNodes += [q]

        return []

distance = lambda t1, t2 : math.sqrt((t2[0] - t1[0])**2 + (t2[1] - t1[1])**2)

with open("coords.pickle", "rb") as fp:   # Unpickling
    coords = pickle.load(fp)

with open("mapasgraph.pickle", "rb") as fp:  # Unpickling
    AA = pickle.load(fp)
M = AA[1]

tinit = time.process_time()

#Taxi = linhas brancas; Autocarro = linhas azuis; Metro = linhas vermelhas
SP = SearchProblem([113], M, coords)
SOL = SP.search([18], tickets = [5, 5, 2])
print(SOL)

tend = time.process_time()

print(tend - tinit)