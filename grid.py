import numpy as np
import random
# from scipy.sparse import random
from creature import Creature, Food

class Grid:

    #Ghost zone should be bigger than Creature.perceptionFieldSize
    ghostZone = 10

    def __init__(self, N, creatureDensity, foodDensity):
        self.creatureList = []
        self.__rg =  np.random.default_rng()
        self.creatureGrid = np.zeros((N+Grid.ghostZone*2,N+Grid.ghostZone*2), dtype=object)
        self.foodGrid = np.zeros((N+Grid.ghostZone*2,N+Grid.ghostZone*2), dtype=object)
        self.topography = np.full((N+Grid.ghostZone*2,N+Grid.ghostZone*2), 10000)
        self.topography[Grid.ghostZone:N+Grid.ghostZone, Grid.ghostZone:N+Grid.ghostZone] = 1

        self.N = N

        for i in range(Grid.ghostZone, N+Grid.ghostZone):
            for j in range(Grid.ghostZone, N+Grid.ghostZone):

                if (self.__rg.random() < creatureDensity):
                    self.creatureGrid[i,j] = Creature(self, [i, j], self.__rg.random())

                if (self.__rg.random() < foodDensity):
                    self.foodGrid[i,j] = Food([i,j])

    def updateAll(self):
        # Cannot be parallelized due to race condition issues
        random.shuffle(self.creatureList)
        for creature in self.creatureList:
            creature.update()

    def plotAll(self, ax):
        # Could be parallelized
        # mayube using numpy vectorize?
        for creature in self.creatureList:
            ax.scatter(creature.y, creature.x)
            ax.annotate(creature.id, (creature.y, creature.x), c="white")

        # Plot food
        ax.imshow(self.foodGrid != 0, origin='upper')

    
