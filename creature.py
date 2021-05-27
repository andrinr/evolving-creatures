from operator import le
import numpy as np
from helpers import normalize, sRound, closestPoint
from scipy.ndimage import gaussian_filter
from itertools import product, combinations
from genome import Genome
from matplotlib.cm import RdYlBu_r as cMap

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
        self._energy = 1

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
    deathProb = 0.0

    log = []
    maxEnergy = 10
    uniqueId = 0
    rg = np.random.default_rng()

    def __init__(self, grid, pos, energy, genome):
        super().__init__()
        self._color = None
        self._costsPerUnitMove = 0.05
        self._energy = energy
        self._finalCosts = None
        self._genome = genome
        self._id = Creature.uniqueId
        self._isAlive = True
        self._pos = np.array(pos)
        self._pfSize = 5 #round(self._genome.get('pfSize'))
        self._pfShape = [self._pfSize, self._pfSize]
        self._age = 0
        self._currentIteration = -1

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

    def update(self, iteration):
        self._currentIteration = iteration

        self._checkSurvivalConditions()

        if not self._isAlive:
            return 

        self._age += 1

        self._spotEnvironment()
        self._getfinalCosts()
        self._spotNextLoc()
        self._moveToNextLoc()
        self._eatFood()

        # # TODO: interact with enemy when close
        # r = self._pfSize
        # adjEnemies = (self._enemies[r-1:r+1,r-1:r+1])[np.nonzero(self._enemies[r-1:r+1,r-1:r+1] != 0)]
        # if len(adjEnemies) > 0:
        #     self._attackEnemy(adjEnemies[self.rg.integers(0,high=len(adjEnemies))])

        # # TODO: interact with friend when close
        # adjFriends = (self._friends[r-1:r+1,r-1:r+1])[np.nonzero(self._friends[r-1:r+1,r-1:r+1] != 0)]
        # if len(adjFriends) > 0:
        #     self._tradeFriend(adjFriends[self.rg.integers(0,high=len(adjFriends))])

        self._breed()



# =============================================================================
# actions
# =============================================================================
    def _eatFood(self):
        if self._grid.foodGrid[self.gridIndex]:
            self._energy = min(self._grid.foodGrid[self.gridIndex].energy + self.energy, self.maxEnergy)
            self._grid.foodGrid[self.gridIndex] = 0

    def _attackEnemy(self, enemy):
        # Fight logic
        if (self.energy > enemy.energy):
            self._energy += enemy.energy
            enemy._die('fight')
        # Costs for attacking a creature
        self._energy -= 0.1
        pass

    def _checkSurvivalConditions(self):
        if self.rg.random() < self.deathProb:
            self._die('natural')
            return

        if self._energy <= 0:
            self._die('energy')
            return

    def _tradeFriend(self, friend):
        # Fight logic
        # Costs for attacking a creature
        mid = (friend.energy + self.energy)/2
        self.energy = mid
        friend.energy = mid

    def _die(self, cause):
        # Add to log
        self.log.append(self.genome.genLog() + [cause, self._currentIteration, self._age])

        self._isAlive = False
        self._grid.creatureList.remove(self)
        self._grid.creatureGrid[self.gridIndex] = 0

    def _moveToNextLoc(self):
        self._layScent()
        # if self.genome.get('speed') >3:
        #     print(self._movementCosts(self._target))
        self._energy -= self._movementCosts(self._target)
        self._grid.creatureGrid[self.gridIndex] = 0
        self._pos = self._pos + self._target
        self._grid.creatureGrid[self.gridIndex] = self

    def _breed(self):
        if self.energy > self._genome.get('energyChildrenThreshold') and self._grid.checkBounds(self.x, self.y):
            # Adjacency field are all the fields within a distance of 1
            adjacency = self._perceptualField(self._grid.creatureGrid, 1)
            # All instances where there is no other creature
            free = adjacency == 0
            # Set the aim of new children, limited by the avaiable space
            nChildrenAim = min(int(self._genome.get('nKids')), np.count_nonzero(free))
            nChildrenActual = 0

            self._die('breed')

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
        # Make sure self is not spotted
        # if np.shape(self._creatures)[0] == 0:
        #     print(self.x, self.y)
        # self._creatures[self._pfSize, self._pfSize] = 1

    def _spotEnemies(self):
        e = self._creatures.copy()
        n = e.shape[0]
        for i, j in product(range(n), range(n)):
            # Similar genome means the two creatures are friendly
            if e[i,j] and e[i,j].genome.difference(self.genome) < self.genome.get('genomeThreshold'):
                e[i,j] = 0
        self._enemies = e

    def _spotEnvironment(self):
        self._spotFood()
        self._spotCreatures()
        # self._spotEnemies()
        # self._spotFriends()

    def _spotFood(self):
        self._food = self._perceptualField(self._grid.foodGrid, self._pfSize)

    def _spotFriends(self):
        f = self._creatures.copy()
        n = f.shape[0]
        for i, j in product(range(n), range(n)):
            # Similar genome means the two creatures are friendly
            if f[i,j] and self._enemies[i,j]:
                f[i,j] = 0
        self._friends = f

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
    def _creatureCosts(self):
        return (self._creatures != 0).astype(int)

    def _getDistanceCosts(self):
        for i, j in product(range(2 * self._pfSize + 1), range(2 * self._pfSize + 1)):
                self._distanceCosts[i,j] = np.linalg.norm(np.array([i - self._pfSize, j - self._pfSize]))
        # Normalize
        self._distanceCosts /= np.linalg.norm(np.array(self._pfShape))

    def _enemiesCosts(self):
        costs = (self._enemies != 0).astype(int) * self._genome.get('toEnemies')
        blured = gaussian_filter(costs,sigma=1, mode="nearest")
        blured[self._pfSize, self._pfSize] = 0
        return blured

    def _getfinalCosts(self):
        # crucial costs
        self._finalCosts = self._creatureCosts() + self._randomCosts() + self._topoCosts() + self._distanceCosts + self._scentCosts()
        
        # features costs
        self._finalCosts += self._foodCosts()
        # self._finalCosts += self._enemiesCosts()
        # self._finalCosts += self._friendsCosts()
        
        # Avoid staying at the same place
        # sefl._finalCosts[self._pfSize, self._pfSize] = 1

    def _foodCosts(self):
        return -(self._food != 0).astype(int)

    def _friendsCosts(self):
        costs = (self._enemies != 0).astype(int) * self._genome.get('toFriends')
        blured = gaussian_filter(costs,sigma=1, mode="nearest")
        blured[self._pfSize, self._pfSize] = 0
        return blured

    def _movementCosts(self, path):
        speedCosts = round(self.genome.get('speed'))
        return np.linalg.norm(path) * self._costsPerUnitMove * speedCosts

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

        return cMap(round(scaledSpeed))

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