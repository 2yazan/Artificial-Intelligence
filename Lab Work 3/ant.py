from PyQt5.QtCore import qDebug
import random

class AntAlgorithm:
    def __init__(self, n, iterations, antsCount, eliteAntsCount, alpha, beta, rho):
        # Number of algorithm iterations
        self.iterations = iterations
        # Number of ants
        self.antsCount = antsCount
        # Number of roads
        self.roads = []
        # sum of pheromones for each ant
        self.sums = []
        # Number of elite ants
        self.eliteAntsCount = eliteAntsCount
        # Number of vertices
        self.n = n
        # weight for the influence of pheromones
        self.alpha = alpha
        # Heuristic coefficient
        self.beta = beta
        # Pheromone evaporation rate
        self.rho = rho

        self.eliteAnts = []
        for i in range(eliteAntsCount):
            r = random.randint(0, antsCount)
            while r in self.eliteAnts:
                r = random.randint(0, antsCount)
            self.eliteAnts.append(r)
        # Index is the serial number of the ant, value is the vertex in which it is located
        self.antsPositon = []
        # place each ant at the next vertex
        for i in range(0, self.antsCount):
            self.antsPositon.append(i % self.n)

        # Already visited vertices by ants
        self.tabuList = [[] for j in range(self.antsCount)]
        # Starting vertices are also marked as visited
        for i in range(0, len(self.antsPositon)):
            self.tabuList[i].append(self.antsPositon[i])
            self.roads.append([i])
            self.sums.append(0)
        # Assume the graph is fully connected
        # Matrix of distances between graph vertices
        self.distances = [[0 for i in range(n)] for j in range(n)]
        # Amount of pheromones on an edge is represented as a triple:
        # starting vertex, ending vertex, and the amount of pheromone
        self.ph = []
        self.newPh = []
        # The graph is undirected, so d[i][j] = d[j][i]
        for i in range (0, n):
            for j in range (i + 1, n):
                # Set a random path length value
                r = random.randint(1, 10)
                self.distances[i][j], self.distances[j][i] = int(r), int(r)
                # Remember the vertex and assign a pheromone value to it
                self.ph.append([i, j, 1 / self.n])

    # return the current pheromone levels on edges
    def getPh(self):
        return self.ph

    # return the distances between cities
    def getDistances(self):
        return self.distances


    def perform(self):
        # Create a copy of the initial pheromones
        self.newPh = self.ph.copy()
        # Until ants visit all vertices
        for iter in range(self.iterations):
            while len(self.tabuList[0]) != self.n:
                # For each ant
                for ant in range(self.antsCount):
                    P = [0 for pos in range(self.n)]        # Transition probabilities
                    taus = []     # Amount of pheromones on the path to the vertex
                    mus = []      # Attractiveness of the vertex
                    for i in range(self.n):
                        # If the vertex is visited
                        if i in self.tabuList[ant]:
                            # Do not add anything
                            tau = 0
                            mu = 0
                        else:
                            # Otherwise, calculate tau and mu
                            tau = self.tau(i, self.antsPositon[ant])
                            mu = self.mu(i, self.antsPositon[ant])
                        # Save them
                        taus.append(tau)
                        mus.append(mu)
                    tmpsum = 0
                    for i in range(len(P)):
                        if taus[i] and mus[i] != 0:
                            tmpsum  += taus[i] ** self.alpha * mus[i] ** self.beta
                    for i in range(len(P)):
                        if taus[i] and mus[i] != 0:
                            P[i] = taus[i] ** self.alpha * mus[i] ** self.beta / tmpsum

                    # Ant chooses where to go and moves quickly
                    if (ant in self.eliteAnts):
                        newAntPosition = self.chooseBestVertex(P)
                    else:
                        newAntPosition = self.chooseNewVertex(P)
                    self.roads[ant].append(newAntPosition)
                    # In this case, delta is equal to mu
                    ph = (1 - self.rho) * self.tau(newAntPosition, self.antsPositon[ant]) + self.mu(newAntPosition, self.antsPositon[ant])
                    self.updatePh(self.antsPositon[ant], newAntPosition, ph)
                    # The ant will not return to the starting point
                    self.antsPositon[ant] = newAntPosition
                    self.tabuList[ant].append(newAntPosition)
                    self.sums[ant] += ph
                # Record the new pheromone values
                self.ph = self.newPh.copy()
            for currentPh in self.ph:
                currentPh[2] *= self.rho
            best = self.sums.index(min(self.sums))
            qDebug("Epoch {} best route {}, contains: {} with pheromone {} and length {}".format(iter, best, self.roads[best], self.sums[best], sum(self.distances[best])))
            self.restore()

    def restore(self):
        self.tabuList = [[] for j in range(self.antsCount)]
        self.sums.clear()
        self.roads.clear()
        for i in range(0, len(self.antsPositon)):
            self.tabuList[i].append(self.antsPositon[i])
            self.roads.append([i])
            self.sums.append(0)

    # Updates the amount of pheromone on the edge
    def updatePh(self, start, end, ph):
        if start > end:
            start, end = end, start
        # Write to the UPDATED PHEROMONES
        for currentPh in self.newPh:
            if currentPh[0] == start and currentPh[1] == end:
                currentPh[2] += ph
                return

    # Returns the amount of pheromones on the edge between vertices i and j
    def tau(self, start, end):
        if start > end:
            start, end = end, start
        for currentPh in self.ph:
            if currentPh[0] == start and currentPh[1] == end:
                return currentPh[2]

    # Returns the attractiveness of the edge
    def mu(self, start, end):
        if start > end:
            start, end = end, start
        # The attractiveness is taken as the reciprocal of the distance
        return 1 / self.distances[start][end]

    # Returns the index of the vertex to which the ELITE ant will transition with transition probabilities P
    def chooseBestVertex(self, P):
        return P.index(max(P))

    # Returns the index of the vertex to which the ant will transition with transition probabilities P
    def chooseNewVertex(self, P):
        r = random.random()
        tmp = 0
        for i in range(len(P)):
            tmp += P[i]
            if tmp > r:
                return i