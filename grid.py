import numpy as np
# from scipy.sparse import random
from creature import Creature, Food
from itertools import product
from genome import Genome

class Grid:

    #Ghost zone should be bigger than Creature.perceptionFieldSize
    PARAMETERS = {}

    def __init__(self, N):
        self.N = N
        self.__rg =  np.random.default_rng()

        gz = self.PARAMETERS['GHOST_ZONE']
        self.outerGridShape = (N+gz*2, N+gz*2)
        self.innerGridShape = (N,N)
        self.innerGridSlice = (slice(gz, N+gz),slice(gz, N+gz))

        self.dtfoodDensity = self.PARAMETERS['GROW_FOOD_RATE']
        self.foodGrid = np.zeros(self.outerGridShape, dtype=object)
        self.foodGrid[self.innerGridSlice] = (self.__rg.random(self.innerGridShape).astype(float) < self.PARAMETERS['INIT_FOOD_RATE']).astype(int) * Food()

        self.topography = np.full(self.outerGridShape, 1000, dtype=float)
        self.topography[self.innerGridSlice] = 0

        # Each creature leave behind a scent, avoids creature to make repetitive moves
        self.scent = np.zeros(self.outerGridShape, dtype=float)

        self.creatureList = []
        self.creatureGrid = np.zeros(self.outerGridShape, dtype=object)

        for i, j in product(range(gz, N+gz), repeat=2):
            if (self.__rg.random() < self.PARAMETERS['CREATURE_RATE']):
                Creature(self, [i, j], 2, Genome(names=['speed', 'pfSize']))

        self.histCreatures = []
        self.histFood = []

    def updateAll(self, iteration):
        self.scent *= 0.9
        self.foodGrid[self.innerGridSlice] += (self.__rg.random(self.innerGridShape).astype(float) < self.dtfoodDensity).astype(int) * Food()
        self.histSpeeds = []
        self.histPFsize = []
        self.histColors = []
        # Cannot be parallelized due to race condition issues
        # Made this to easily be able to track single instance for plotting
        shuffled = self.creatureList.copy()
        self.__rg.shuffle(shuffled)
        for creature in shuffled:
            self.histSpeeds.append(creature.genome.get('speed'))
            self.histPFsize.append(creature.genome.get('pfSize'))
            self.histColors.append(creature.color)
            creature.update(iteration)
        
        self.histCreatures.append(len(self.creatureList))
        self.histFood.append(np.count_nonzero(self.foodGrid))

    
    def checkBounds(self, x, y):
        N = self.N
        gz = self.PARAMETERS['GHOST_ZONE']
        if x < gz or x > N + gz:
            return False
        if y < gz or y > N + gz:
            return False

        return True
