import numpy as np
import matplotlib.cm as cm
import random
# from scipy.sparse import random
from creature import Creature, Food
from itertools import product

class Grid:

    #Ghost zone should be bigger than Creature.perceptionFieldSize
    ghostZone = 5

    def __init__(self, N, creatureDensity, initFoodDensity, dtfoodDenstiy):
        self.creatureList = []
        self.__rg =  np.random.default_rng()

        self.dtfoodDensity = dtfoodDenstiy
        self.foodGrid = (self.__rg.random((N+self.ghostZone*2, N+self.ghostZone*2)).astype(float) < initFoodDensity).astype(int) * Food()

        self.creatureGrid = np.zeros_like(self.foodGrid, dtype=object)

        self.topography = np.full_like(self.foodGrid, 10, dtype=float)
        self.topography[Grid.ghostZone-1:N+Grid.ghostZone+1, Grid.ghostZone:N-1+Grid.ghostZone+1] = 1
        self.topography[Grid.ghostZone:N+Grid.ghostZone, Grid.ghostZone:N+Grid.ghostZone] = 0

        # Each creature leave behind a scent, avoids creature to make repetitive moves
        self.scent = np.zeros_like(self.foodGrid, dtype=float)

        self.N = N

        for i, j in product(range(Grid.ghostZone, N+Grid.ghostZone), range(Grid.ghostZone, N+Grid.ghostZone)):
            if (self.__rg.random() < creatureDensity):
                Creature(self, [i, j], 1.0)

    def updateAll(self):
        self.scent *= 0.9

        self.foodGrid += (self.__rg.random((np.shape(self.foodGrid))).astype(float) < self.dtfoodDensity) * Food()

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
            axl.scatter(creature.y, creature.x, s=creature.energy*10, c="red")
            axl.annotate(creature.id, (creature.y, creature.x), c='black')

        # Plot food
        axl.imshow(self.foodGrid != 0, origin='upper', cmap="Greens")
        if len(self.creatureList):
        
            axr.imshow(self.creatureList[0].finalCosts.astype(float), vmin=0, vmax=1.2, cmap='magma')
            axr.set_title("Perception field ID: " + str(self.creatureList[0]._id))

    
