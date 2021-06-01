import numpy as np
# from scipy.sparse import random
from creature import Creature, Food
from itertools import product
from genome import Genome

class Grid:

    #Ghost zone should be bigger than Creature.perceptionFieldSize
    ghostZone = 20

    def __init__(self, N, creatureDensity, initFoodDensity, growFoodDenstiy):
        self.N = N
        self.__rg =  np.random.default_rng()
        self.creatureDensity = creatureDensity
        self.initFoodDensity = initFoodDensity

        self.outerGridShape = (N+self.ghostZone*2, N+self.ghostZone*2)
        self.innerGridShape = (N,N)
        self.innerGridSlice = (slice(self.ghostZone, N+self.ghostZone),slice(self.ghostZone, N+self.ghostZone))

        self.growFoodDensity = growFoodDenstiy
        self.foodGrid = np.zeros(self.outerGridShape, dtype=object)
        self.foodGrid[self.innerGridSlice] = (self.__rg.random(self.innerGridShape).astype(float) < initFoodDensity).astype(int) * Food()

        self.topography = np.full(self.outerGridShape, 1000, dtype=float)
        self.topography[self.innerGridSlice] = 0

        # Each creature leave behind a scent, avoids creature to make repetitive moves
        self.scent = np.zeros(self.outerGridShape, dtype=float)

        self.creatureList = []
        self.creatureGrid = np.zeros(self.outerGridShape, dtype=object)

        for i, j in product(range(Grid.ghostZone, N+Grid.ghostZone), repeat=2):
            if (self.__rg.random() < creatureDensity):
                Creature(self, [i, j], 10, Genome(names=['speed', 'pfSize', 'size']))

        self.histCreatures = []
        self.histFood = []

    def updateAll(self):
        self.scent *= 0.9
        self.foodGrid[self.innerGridSlice] += (self.__rg.random(self.innerGridShape).astype(float) < self.growFoodDensity).astype(int) * Food()
        self.eaten =  np.zeros(self.outerGridShape, dtype=int)
        
        self.histSpeeds = []

        self.histPFsize = []
        self.histColors = []
        self.histSizes = []
        self.edgeColors = []
        self.histEnergy = []
        # self.histNKids = []
        
        # Cannot be parallelized due to race condition issues
        # Made this to easily be able to track single instance for plotting
        shuffled = self.creatureList.copy()
        self.__rg.shuffle(shuffled)

        for creature in shuffled:
            if creature.isAlive:
                self.histSpeeds.append(creature.genome.get('speed'))
                self.histPFsize.append(creature.genome.get('pfSize'))
                self.histColors.append(creature.color)
                self.histSizes.append(creature.size)
                # self.histEnergy.append(creature.energy)
                # self.histNKids.appendcreature.genome.get('nKids')
                self.edgeColors.append(creature.edgeColor)
                creature.update()
        
        self.histCreatures.append(len(self.creatureList))
        self.histFood.append(np.count_nonzero(self.foodGrid))
        # print(min(self.histEnergy), max(self.histEnergy))
    
    def checkBounds(self, x, y):
        N = self.N
        gz = self.ghostZone
        if x < gz or x > N + gz:
            return False
        if y < gz or y > N + gz:
            return False

        return True