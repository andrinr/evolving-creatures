import numpy as np
from scipy.sparse import random
from creature import Creature, Food

class Grid:

    #Ghost zone should be bigger than Creature.perceptionFieldSize
    ghostZone = 10

    def __init__(self, N, creatureDensity, foodDensity):
        self.creatureList = []
        self.__rg =  np.random.default_rng()
        self.creatureGrid = np.zeros((N+Grid.ghostZone*2,N+Grid.ghostZone*2), dtype=object)
        self.foodGrid = np.zeros((N+Grid.ghostZone*2,N+Grid.ghostZone*2), dtype=object)

        self.N = N

        for i in range(Grid.ghostZone, N+Grid.ghostZone):
            for j in range(Grid.ghostZone, N+Grid.ghostZone):

                if (self.__rg.random() < creatureDensity):
                    self.creatureGrid[i,j] = Creature(self, [i, j], self.__rg.random())

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
            ax.scatter(creature.y, creature.x)
            ax.annotate(creature.id, (creature.y, creature.x), c="white")

        # Plot food
        ax.imshow(self.foodGrid != 0, origin='upper')
