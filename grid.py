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
        self.creatureGrid = np.zeros((N+Grid.ghostZone*2,N+Grid.ghostZone*2), dtype=object)

        self.foodGrid = (self.__rg.random(np.shape(self.creatureGrid)).astype(float) < initFoodDensity).astype(int) * Food()

        self.dtfoodDensity = dtfoodDenstiy

        self.topography = np.full_like(self.creatureGrid, 10)
        self.topography[Grid.ghostZone:N+Grid.ghostZone, Grid.ghostZone:N+Grid.ghostZone] = 0

        # Each creature leave behind a scent, avoids creature to make repetitive moves
        self.scent = np.zeros_like(self.creatureGrid)

        self.N = N

        for i, j in product(range(Grid.ghostZone, N+Grid.ghostZone), range(Grid.ghostZone, N+Grid.ghostZone)):
            if (self.__rg.random() < creatureDensity):
                self.creatureGrid[i,j] = Creature(self, [i, j])

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

    
