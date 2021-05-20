import numpy as np
# from scipy.sparse import random
from creature import Creature, Food
from itertools import product
from genome import Genome

class Grid:

    #Ghost zone should be bigger than Creature.perceptionFieldSize
    ghostZone = 10

    def __init__(self, N, creatureDensity, initFoodDensity, dtfoodDenstiy):
        self.creatureList = []
        self.__rg =  np.random.default_rng()
        self.dtfoodDensity = dtfoodDenstiy
        self.outerGridShape = (N+self.ghostZone*2, N+self.ghostZone*2)
        self.innerGridShape = (N,N)
        self.innerGridSlice = (slice(self.ghostZone, N+self.ghostZone),slice(self.ghostZone, N+self.ghostZone))
        self.N = N
        self.foodGrid = np.zeros(self.outerGridShape, dtype=object)
        self.foodGrid[self.innerGridSlice] = (self.__rg.random(self.innerGridShape).astype(float) < initFoodDensity).astype(int) * Food()

        self.creatureGrid = np.zeros(self.outerGridShape, dtype=object)

        self.topography = np.full(self.outerGridShape, 1000, dtype=float)
        self.topography[self.innerGridSlice] = 0

        # Each creature leave behind a scent, avoids creature to make repetitive moves
        self.scent = np.zeros(self.outerGridShape, dtype=float)

        for i, j in product(range(Grid.ghostZone, N+Grid.ghostZone), range(Grid.ghostZone, N+Grid.ghostZone)):
            if (self.__rg.random() < creatureDensity):
                Creature(self, [i, j], 1.0, Genome())

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

    def plotAll(self, axl, axPf, axFood, axGen1, axGen2):
        # Could be parallelized
        # mayube using numpy vectorize?
        for creature in self.creatureList:

            axl.scatter(creature.y, creature.x, s=1, c="red", marker=',')

            axGen1.scatter(creature.genome.get('energyChildrenThreshold'), creature.genome.get('nChildren'),s=1, marker=',')

            #axGen2.scatter(creature.genome.get('size'), creature.genome.get('energyChildrenRatio'), marker=',')

            #axl.annotate(creature.id, (creature.y, creature.x), c='black')

        axGen1.set_title('energyChildrenThreshold (x) vs nChildren (y)')

        # Plot food
        axl.imshow(self.foodGrid != 0, origin='upper', cmap="Greens")
        if len(self.creatureList):
        
            axPf.imshow(self.creatureList[0].finalCosts.astype(float), vmin=0, vmax=1.2, cmap='magma')
            axPf.set_title("PF ID: " + str(self.creatureList[0]._id))

        axFood.plot(range(min(len(self.histFood),1000)), self.histFood[-1000:None], c="green")
        axFood.plot(range(min(len(self.histCreatures),1000)), self.histCreatures[-1000:None], c="red")
    
    def checkBounds(self, x, y):
        N = self.N
        gz = self.ghostZone
        if x < gz or x > N + gz:
            return False
        if y < gz or y > N + gz:
            return False

        return True
