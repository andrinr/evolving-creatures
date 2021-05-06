import numpy as np
from scipy.sparse import random
from creature import Creature, Food

class Grid:

    def __init__(self, N, creatureDensity, foodDensity):
        self.creatureList = []
        self.rg =  np.random.default_rng()
        self.creatureGrid = np.zeros((N,N), dtype=object)
        self.foodGrid = np.zeros((N,N), dtype=object)

        self.N = N

        for i in range(N):
            for j in range(N):
                if (self.rg.random() < creatureDensity):
                    self.creatureGrid[i,j] = Creature(self, np.array([i,j]), Creature.rg.random())

                if (self.rg.random() < foodDensity):
                    self.foodGrid[i,j] = Food(np.array([i,j]))


    def updateAll(self):
        n = len(self.creatureList)
        indices = np.linspace(0, n-1, num=n, dtype=int)
        self.rg.shuffle(indices)

        # Cannot be parallelized due to race condition issues
        for index in indices:
            self.creatureList[index].update()

        return

    def plotAll(self, ax):
        # Could be parallelized
        # mayube using numpy vectorize?
        for creature in self.creatureList:
            ax.scatter(creature.x, creature.y)

        # Plot food
        ax.imshow(self.foodGrid != 0)
     
