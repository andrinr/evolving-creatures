import numpy as np
# from scipy.sparse import random
from creature import Creature, Food
from itertools import product
from genome import Genome

class Grid:

    #Ghost zone should be bigger than Creature.perceptionFieldSize
    ghostZone = 10

    def __init__(self, N, creatureDensity, initFoodDensity, dtfoodDenstiy):
        self.N = N
        self.__rg =  np.random.default_rng()

        self.outerGridShape = (N+self.ghostZone*2, N+self.ghostZone*2)
        self.innerGridShape = (N,N)
        self.innerGridSlice = (slice(self.ghostZone, N+self.ghostZone),slice(self.ghostZone, N+self.ghostZone))

        self.dtfoodDensity = dtfoodDenstiy
        self.foodGrid = np.zeros(self.outerGridShape, dtype=object)
        self.foodGrid[self.innerGridSlice] = (self.__rg.random(self.innerGridShape).astype(float) < initFoodDensity).astype(int) * Food()

        self.topography = np.full(self.outerGridShape, 1000, dtype=float)
        self.topography[self.innerGridSlice] = 0

        # Each creature leave behind a scent, avoids creature to make repetitive moves
        self.scent = np.zeros(self.outerGridShape, dtype=float)

        self.creatureList = []
        self.creatureGrid = np.zeros(self.outerGridShape, dtype=object)

        for i, j in product(range(Grid.ghostZone, N+Grid.ghostZone), range(Grid.ghostZone, N+Grid.ghostZone)):
            if (self.__rg.random() < creatureDensity):
                Creature(self, [i, j], 1.0, Genome())

        self.histCreatures = []
        self.histFood = []

    def updateAll(self, iteration):
        self.scent *= 0.9
        self.foodGrid[self.innerGridSlice] += (self.__rg.random(self.innerGridShape).astype(float) < self.dtfoodDensity).astype(int) * Food()

        # Cannot be parallelized due to race condition issues
        # Made this to easily be able to track single instance for plotting
        shuffled = self.creatureList.copy()
        self.__rg.shuffle(shuffled)
        for creature in shuffled:
            creature.update(iteration)

        self.histCreatures.append(len(self.creatureList))
        self.histFood.append(np.count_nonzero(self.foodGrid))

    
    def checkBounds(self, x, y):
        N = self.N
        gz = self.ghostZone
        if x < gz or x > N + gz:
            return False
        if y < gz or y > N + gz:
            return False

        return True
