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
        self.__N = N
        self.dtfoodDensity = dtfoodDenstiy
        self.outerGridShape = (N+self.ghostZone*2, N+self.ghostZone*2)
        self.innerGridShape = (N,N)
        self.innerGridSlice = (slice(self.ghostZone, N+self.ghostZone),slice(self.ghostZone, N+self.ghostZone))

        self.foodGrid = np.zeros(self.outerGridShape, dtype=object)
        self.foodGrid[self.innerGridSlice] = (self.__rg.random(self.innerGridShape).astype(float) < initFoodDensity).astype(int) * Food()

        self.creatureGrid = np.zeros(self.outerGridShape, dtype=object)

        self.topography = np.full(self.outerGridShape, 10, dtype=float)
        self.topography[self.innerGridSlice] = 0

        # Each creature leave behind a scent, avoids creature to make repetitive moves
        self.scent = np.zeros(self.outerGridShape, dtype=float)

        self.N = N

        for i, j in product(range(Grid.ghostZone, N+Grid.ghostZone), range(Grid.ghostZone, N+Grid.ghostZone)):
            if (self.__rg.random() < creatureDensity):
                Creature(self, [i, j], 1.0)

        self.histCreatures = []
        self.histFood = []

    def updateAll(self):
        self.scent *= 0.9
        self.foodGrid[self.innerGridSlice] += (self.__rg.random(self.innerGridShape).astype(float) < self.dtfoodDensity).astype(int) * Food()

        # Cannot be parallelized due to race condition issues
        # Made this to easily be able to track single instance for plotting
        shuffled = self.creatureList.copy()
        self.__rg.shuffle(shuffled)
        for creature in shuffled:
            creature.update()

        self.histCreatures.append(len(self.creatureList))
        self.histFood.append(np.count_nonzero(self.foodGrid))

    def plotAll(self, axl, axPf, axFood):
        # Could be parallelized
        # mayube using numpy vectorize?
        for creature in self.creatureList:
            axl.scatter(creature.y, creature.x, s=creature.energy*10, c="red")
            axl.annotate(creature.id, (creature.y, creature.x), c='black')

        # Plot food
        axl.imshow(self.foodGrid != 0, origin='upper', cmap="Greens")
        if len(self.creatureList):
        
            axPf.imshow(self.creatureList[0].finalCosts.astype(float), vmin=0, vmax=1.2, cmap='magma')
            axPf.set_title("Perception field ID: " + str(self.creatureList[0]._id))

        axFood.plot(range(len(self.histFood)), self.histFood, c="green")
        axFood.plot(range(len(self.histCreatures)), self.histCreatures, c="red")

        

    
