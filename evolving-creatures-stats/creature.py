from operator import le
import numpy as np
from helpers import normalize, sRound, closestPoint
from scipy.ndimage import gaussian_filter
from itertools import product, combinations
from genome import Genome
from matplotlib.cm import RdYlBu_r as cMap1
from matplotlib.cm import PiYG as cMap2

class Figure(object):

    def __init__(self):
        self._color = 'red'
        self._energy = 0

    @ property
    def energy(self):
        return self._energy

    @energy.setter
    def energy(self, var):
        self._energy = var

    @ property
    def color(self):
        return self._color

    def update(self):
        return


class Food(Figure):
    def __init__(self):
        super().__init__()
        self._color = 'green'
        self._energy = 5

    def __mul__(self, a):
        return self if a else a

    def __rmul__(self, a):
        return self if a else a

    def __add__(self, a):
        return self 

    def __radd__(self, a):
        return self


class Creature(Figure):
    # put this inside genome
    deathProb = 0.01

    data = []
    maxEnergy = 100
    uniqueId = 0
    rg = np.random.default_rng()

    def __init__(self, grid, pos, energy, genome):
        super().__init__()
        self._color = None
        self._costsPerUnitMove = .01
        self._energy = energy
        self._finalCosts = None
        self._genome = genome
        self._id = Creature.uniqueId
        self._isAlive = True
        self._pos = np.array(pos)
        self._pfSize = round(self._genome.get('pfSize'))
        self._size = self._genome.get('size')
        self._pfShape = [self._pfSize, self._pfSize]

        # for random costs
        self._randFact = 0.2

        self._grid = grid
        self._grid.creatureList.append(self)
        self._grid.creatureGrid[self.gridIndex] = self

        self._creatures = None
        self._enemies = None
        self._food = None
        self._friends = None

        self._distanceCosts = np.zeros((self._pfSize*2+1, self._pfSize*2+1))
        self._getDistanceCosts()

        Creature.uniqueId += 1

    def __str__(self):
        return 'Creature ID. = {}\nEnergyLevel = {}\n'.format(self.id, self.energy)

    def update(self):
        self._checkSurvivalConditions()

        if not self._isAlive:
            return 

        self._spotEnvironment()
        self._getfinalCosts()
        self._spotNextLoc()
        self._moveToNextLoc()
        self._breed()



# =============================================================================
# actions
# =============================================================================
    def _eatFood(self):
        food = self._grid.foodGrid[self.gridIndex]
        if food and self._energy <= self.maxEnergy:
            self._energy = food.energy + self._energy
            self._checkMaxEnergy()
            self._grid.foodGrid[self.gridIndex] = 0

    def _eatPrey(self):
        creature = self._grid.creatureGrid[self.gridIndex]
        if creature and self._isPrey(creature):
            self._energy += creature.energy
            self._checkMaxEnergy()
            creature.kill()
            
            self._grid.eaten[self.gridIndex] = 1


    def _isEnemy(self, creature):
        return True if creature.size > self._size * 1.2 else False

    def _isPrey(self, creature):
        return True if creature.size < self._size / 1.2 else False

    def _checkMaxEnergy(self):
        if self._energy > self.maxEnergy:
            self._energy = self.maxEnergy

    def _checkSurvivalConditions(self):
        if self.rg.random() < self.deathProb or self._energy <= 0:
            self.kill()

    def kill(self):
        self._isAlive = False
        self._grid.creatureList.remove(self)
        self._grid.creatureGrid[self.gridIndex] = 0

        self.data.append(self.genome.genes)

    def _moveToNextLoc(self):
        self._layScent()
        self._energy -= self._energyCosts(self._target)
        self._grid.creatureGrid[self.gridIndex] = 0
        self._pos = self._pos + self._target
        self._eatPrey()
        self._eatFood()
        self._grid.creatureGrid[self.gridIndex] = self

    def _breed(self):
        if self.energy > self._genome.get('energyChildrenThreshold') and self._grid.checkBounds(self.x, self.y):
            # Adjacency field are all the fields within a distance of 1
            adjacency = self._perceptualField(self._grid.creatureGrid, 1)
            # All instances where there is no other creature
            free = adjacency == 0
            # Set the aim of new children, limited by the avaiable space
            nChildrenAim = min(round(self._genome.get('nKids')), np.count_nonzero(free))
            nChildrenActual = 0

            self.kill()

            for i, j in combinations(range(3), 2):
                # Spawn creature when cell is free
                if (free[i,j]):
                    if (nChildrenActual >= nChildrenAim):
                        break
                    nChildrenActual += 1
                    # Each child receives energy penalty
                    Creature(self._grid, self._pos + np.array([i-1,j-1]), self.energy/nChildrenAim-0.1, self._genome.replicate(0.15))

    def _layScent(self):
        self._grid.scent[self.gridIndex] += 0.6

# =============================================================================
# perception
# =============================================================================
    def _perceptualField(self, grid, size):
        r = size
        lx = self.x - r
        ly = self.y - r
        ux = self.x + r + 1
        uy = self.y + r + 1
        return grid[lx : ux, ly : uy]


    def _spotCreatures(self):
        self._creatures = self._perceptualField(self._grid.creatureGrid, self._pfSize)

    def _spotEnvironment(self):
        self._spotFood()
        self._spotCreatures()

    def _spotFood(self):
        self._food = self._perceptualField(self._grid.foodGrid, self._pfSize)

    def _spotNextLoc(self):
        # Target is postions of minimum of all costs
        self._target = np.unravel_index(self._finalCosts.argmin(), self._finalCosts.shape) 
        self._target -= np.array([self._pfSize, self._pfSize])
        self._targetDist = np.linalg.norm(self._target)
        self._target = sRound(normalize(self._target))
        self._target *= round(min(self.genome.get('speed'), self._targetDist))

# =============================================================================
# costs
# =============================================================================
    # def _creatureCosts(self):
    #     return (self._creatures != 0).astype(int)

    def _getDistanceCosts(self):
        for i, j in product(range(2 * self._pfSize + 1), range(2 * self._pfSize + 1)):
                self._distanceCosts[i,j] = np.linalg.norm(np.array([i - self._pfSize, j - self._pfSize]))
        # Normalize
        self._distanceCosts /= np.linalg.norm(np.array(self._pfShape))

    def _creatureCosts(self):
        creatures = self._creatures.copy()
        n = creatures.shape[0]
        for i, j in product(range(n), range(n)):
            creature = creatures[i,j]
            if creature:
                if self._isEnemy(creature):
                    creatures[i,j] = self.genome.get('toEnemies')
                elif self._isPrey(creature):
                    creatures[i,j] = self.genome.get('toPrey')

                        
        # bluredCreatures = gaussian_filter(creatures ,sigma=1, mode="nearest")
        # bluredCreatures[self._pfSize, self._pfSize] = 0
        return (creatures != 0).astype(float)

    def _getfinalCosts(self):
        # crucial costs
        self._finalCosts = self._creatureCosts() + self._randomCosts() + self._topoCosts() + self._distanceCosts + self._scentCosts()
        
        # features costs
        self._finalCosts += self._foodCosts()

    def _foodCosts(self):
        return -(self._food != 0).astype(float)

    # def _friendsCosts(self):
    #     costs = (self._enemies != 0).astype(int) * self._genome.get('toFriends')
    #     blured = gaussian_filter(costs,sigma=1, mode="nearest")
    #     blured[self._pfSize, self._pfSize] = 0
    #     return blured

    def _energyCosts(self, path):
        speedCosts = np.linalg.norm(path)
        sizeCosts = np.pi * (self.genome.get('size')/2)**2 * self.genome.get('size')
        pfSizeCosts = self.genome.get('pfSize')/4
        return (.5 * (sizeCosts * speedCosts**2)  + pfSizeCosts)  * self._costsPerUnitMove

    def _randomCosts(self):
        return self.rg.random(np.shape(self._distanceCosts)) * self._randFact

    def _scentCosts(self):
        return self._perceptualField(self._grid.scent, self._pfSize)

    def _topoCosts(self):
        # print(self._perceptualField(self._grid.topography, self._pfSize).shape)
        return self._perceptualField(self._grid.topography, self._pfSize)

# =============================================================================
# getters
# =============================================================================
    @ property
    def color(self):
        minSpeed, maxSpeed = self.genome.bounds['speed']
        speed = self.genome.get('speed')

        # scaling to get the right color
        scaledSpeed = (speed-minSpeed) * 254/maxSpeed

        return cMap1(round(scaledSpeed))

    @ property
    def edgeColor(self):
        minPF, maxPF = self.genome.bounds['pfSize']
        size = self.genome.get('pfSize')

        # scaling to get the right color
        scaledSize = (size-minPF) * 254/maxPF

        return cMap2(round(scaledSize))

    @ property
    def genome(self):
         return self._genome

    @ property
    def gridIndex(self):
        return (self.x, self.y)

    @ property
    def id(self):
        return self._id

    @ property
    def isAlive(self):
        return self._isAlive

    @ property
    def size(self):
        return self._size

    @ property
    def x(self):
        return self._pos[0]

    @ property
    def y(self):
        return self._pos[1]

# =============================================================================
# setters
# =============================================================================
    @ color.setter
    def color(self, col):
        self._color = col