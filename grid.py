import numpy as np
import random
# from scipy.sparse import random
from creature import Creature, Food
from itertools import product

class Grid:

    #Ghost zone should be bigger than Creature.perceptionFieldSize
    ghostZone = 5

    def __init__(self, N, creatureDensity, foodDensity):
        self.creatureList = []
        self.__rg =  np.random.default_rng()
        self.creatureGrid = np.zeros((N+Grid.ghostZone*2,N+Grid.ghostZone*2), dtype=object)

        self.foodGrid = (self.__rg.random((N+Grid.ghostZone*2,N+Grid.ghostZone*2)).astype(float) < foodDensity) * Food()

        self.topography = np.full((N+Grid.ghostZone*2,N+Grid.ghostZone*2), 10)
        self.topography[Grid.ghostZone-1:N+Grid.ghostZone+1, Grid.ghostZone:N-1+Grid.ghostZone+1] = 1
        self.topography[Grid.ghostZone:N+Grid.ghostZone, Grid.ghostZone:N+Grid.ghostZone] = 0

        # Each creature leave behind a scent, avoids creature to make repetitive moves
        self.scent = np.zeros((N+Grid.ghostZone*2,N+Grid.ghostZone*2))

        self.N = N

        for i, j in product(range(Grid.ghostZone, N+Grid.ghostZone), range(Grid.ghostZone, N+Grid.ghostZone)):
            if (self.__rg.random() < creatureDensity):
                self.creatureGrid[i,j] = Creature(self, [i, j], self.__rg.random())

    def updateAll(self):
        self.scent *= 0.9
        # Cannot be parallelized due to race condition issues
        # Made this to easily be able to track single instance for plotting
        shuffled = self.creatureList.copy()
        self.__rg.shuffle(shuffled)
        for creature in shuffled:
            creature.update()

    def plotAll(self, axl, axr):
        # Could be parallelized
        # mayube using numpy vectorize?
        for creature in self.creatureList:
            axl.scatter(creature.y, creature.x, c="red")
            axl.annotate(creature.id, (creature.y, creature.x), c="white")

        # Plot food
        axl.imshow(self.foodGrid != 0, origin='upper')

        axr.imshow(self.creatureList[0].finalCosts, vmin=0, vmax=2)
        axr.set_title("Perception field ID: " + str(self.creatureList[0]._id))

    
