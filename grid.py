import numpy as np
from scipy.sparse import random
from creature import Creature, Food

class Grid:

    def __init__(self, N, creatureDensity, foodDensity):
        self.creatureList = []
        self.__rg =  np.random.default_rng()
        self.creatureGrid = np.zeros((N,N), dtype=object)
        self.foodGrid = np.zeros((N,N), dtype=object)

        self.N = N

        for i in range(N):
            for j in range(N):
                if (self.__rg.random() < creatureDensity):
                    self.creatureGrid[i,j] = Creature(self, [i,j], self.__rg.random())

                if (self.__rg.random() < foodDensity):
                    self.foodGrid[i,j] = Food([i,j])

    def updateAll(self):
        n = len(self.creatureList)
        indices = np.linspace(0, n-1, num=n, dtype=int)
        self.__rg.shuffle(indices)

        # Cannot be parallelized due to race condition issues
        for index in indices:
            self.creatureList[index].update()

    def plotAll(self, ax):
        # Could be parallelized
        # mayube using numpy vectorize?
        for creature in self.creatureList:
            ax.scatter(creature.x, creature.y)
            ax.annotate(creature.id, (creature.x, creature.y), c="white")

        # Plot food
        ax.imshow(np.flip(self.foodGrid,0) != 0, origin='upper')
