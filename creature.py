from operator import le
import numpy as np
from helpers import normalize, sRound, closestPoint
from scipy.ndimage import gaussian_filter
from itertools import product, combinations
from genome import Genome

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
    # Static
    costsPerUnitMove = 0.05
    genomThreshold = 0.2
    deathProb = 0.02
    maxEnergy = 10
    pfSize = 5
    pfShape = [pfSize, pfSize]
    distanceCosts = np.zeros((pfSize*2+1, pfSize*2+1))
    rg = np.random.default_rng()
    
    uniqueId = 0

    data = []

    def __init__(self, grid, pos, energy, genome):
        super().__init__()
        self._pos = np.array(pos)
        self._genome = genome
        self._grid = grid
        self._color = 'red'
        self._isAlive = True

        self.food = None
        self.creatures = None
        self.enemies = None
        self.friends = None
        self.congener = None
        self.finalCosts = 0

        #self.pfSize = int(self._genome.get('size'))

        self._grid.creatureList.append(self)
        self._grid.creatureGrid[self.gridIndex] = self

        self._energy = energy

        # Assuming all creatures have the same perceptualFieldSize
        # We calculate this here to save computing costs
        #if not self.uniqueId:
        self.costsDistances()

        self._id = Creature.uniqueId
        Creature.uniqueId += 1

    def __str__(self):
        return 'Creature ID. = {}\nEnergyLevel = {}\n'.format(self.id, self.energy)

    def update(self):

        if not self._isAlive:
            return

        if self.rg.random() < self.deathProb or self._energy <= 0:
            self.kill()
            return

        self.spotFood()
        self.spotCreatures()
        self.spotEnemies()
        self.spotFriends()
        
        foodCosts = self.costsFood()
        creatureCosts = self.costsCreatures()
        enCosts = self.costsEnemies()
        frCosts = self.costsFriends()
        randomCosts = self.costsRandom(0.02)
        topoCosts = self.perceptualField(self._grid.topography)

        #scentCosts = self.perceptualField(self._grid.scent)

        finalCosts = foodCosts + creatureCosts + randomCosts + topoCosts + self.distanceCosts + enCosts + frCosts

        # Avoid staying at the same place
        finalCosts[self.pfSize, self.pfSize] = 1
        # Store final costs for plotting
        self.finalCosts = finalCosts

        # Target is postions of minimum of all costs
        target = np.unravel_index(finalCosts.argmin(), finalCosts.shape) - np.array([self.pfSize, self.pfSize])
        # only allow single grid cell movements
        move = sRound(normalize(target))
        # Apply move
        self.moveBy(move)

        # Make scent trail
        #self._grid.scent[self.gridIndex] += 0.3

        # Eat food when on top
        if self._grid.foodGrid[self.gridIndex]:
            self.eatFood()
        
        # TODO: interact with enemy when close
        r = self.pfSize
        adjEnemies = (self.enemies[r-1:r+1,r-1:r+1])[np.nonzero(self.enemies[r-1:r+1,r-1:r+1] != 0)]
        if len(adjEnemies) > 0:
            self.attackEnemy(adjEnemies[self.rg.integers(0,high=len(adjEnemies))])

        # TODO: interact with friend when close
        adjFriends = (self.friends[r-1:r+1,r-1:r+1])[np.nonzero(self.friends[r-1:r+1,r-1:r+1] != 0)]
        if len(adjFriends) > 0:
            self.tradeFriend(adjFriends[self.rg.integers(0,high=len(adjFriends))])

        # Check if creature will breed
        if self.energy > self._genome.get('energyChildrenThreshold') and self._grid.checkBounds(self.x, self.y):
            self.breed()
        

# =============================================================================
# actions
# =============================================================================
    def eatFood(self):
        self._energy = min(self._grid.foodGrid[self.gridIndex].energy + self.energy, self.maxEnergy)
        self._grid.foodGrid[self.gridIndex] = 0

    def attackEnemy(self, enemy):
        # Fight logic
        if (self.energy > enemy.energy):
            self._energy += enemy.energy
            enemy.kill()
        # Costs for attacking a creature
        self._energy -= 0.1
        pass

    def tradeFriend(self, friend):
        # Fight logic
        # Costs for attacking a creature
        mid = (friend.energy + self.energy)/2
        self.energy = mid
        friend.energy = mid

    def kill(self):
        self._isAlive = False
        self._grid.creatureList.remove(self)
        self._grid.creatureGrid[self.gridIndex] = 0

        self.data.append(self.genome.genes)

    # Move self, update grid data structure and energylevel
    def moveBy(self, vector):
        self._energy -= self.costsMove(vector)
        self._grid.creatureGrid[self.gridIndex] = 0
        self._pos = self._pos + vector
        self._grid.creatureGrid[self.gridIndex] = self

    def ckeckEnergy(self, path):
        pass

    def breed(self):
        # Adjacency field are all the fields within a distance of 1
        adj = self.adjacencyField(self._grid.creatureGrid)
        # All instances where there is no other creature
        free = adj == 0
        # Set the aim of new children, limited by the avaiable space
        nChildrenAim = min(int(self._genome.get('nChildren')), np.count_nonzero(free))
        nChildrenActual = 0

        self.kill()

        for i, j in combinations(range(3), 2):
            # Spawn creature when cell is free
            if (free[i,j]):
                if (nChildrenActual >= nChildrenAim):
                    break
                nChildrenActual += 1
                # Each child receives energy penalty
                Creature(self._grid, self._pos + np.array([i-1,j-1]), self.energy/nChildrenAim-0.1, self._genome.mutate(0.1))


# =============================================================================
# perception
# =============================================================================
    def perceptualField(self, grid):
        r = self.pfSize
        lx = self.x - r
        ly = self.y - r
        ux = self.x + r + 1
        uy = self.y + r + 1
        return grid[lx : ux, ly : uy]

    def adjacencyField(self, grid):
        r = 1
        lx = self.x - r
        ly = self.y - r
        ux = self.x + r + 1
        uy = self.y + r + 1
        return grid[lx : ux, ly : uy]

    def spotCreatures(self):
        self.creatures = self.perceptualField(self._grid.creatureGrid)
        # Make sure self is counted as other creature # is this necessary? can a creature stay at the same position? 
        if np.shape(self.creatures)[0] == 0:
            print(self.x, self.y)
        self.creatures[self.pfSize, self.pfSize] = 0

    def spotEnemies(self):
        e = self.creatures.copy()
        n = e.shape[0]
        for i, j in product(range(n), range(n)):
            # Similar genome means the two creatures are friendly
            if e[i,j] and e[i,j].genome.difference(self.genome) < self.genome.get('genomeThreshold'):
                e[i,j] = 0
        self.enemies = e

    def spotFood(self):
        self.food = self.perceptualField(self._grid.foodGrid)

    def spotFriends(self):
        f = self.creatures.copy()
        n = f.shape[0]
        for i, j in product(range(n), range(n)):
            # Similar genome means the two creatures are friendly
            if f[i,j] and self.enemies[i,j]:
                f[i,j] = 0
        self.friends = f

# =============================================================================
# costs
# =============================================================================
    def costsCreatures(self):
        # Make sure self is counted as other creature
        return (self.creatures != 0).astype(int)

    def costsDistances(self):
        for i, j in product(range(2 * self.pfSize + 1), range(2 * self.pfSize + 1)):
                self.distanceCosts[i,j] = np.linalg.norm(np.array([i - self.pfSize, j - self.pfSize]))
        # Normalize
        self.distanceCosts /= np.linalg.norm(np.array(self.pfShape))

    def costsEnemies(self):
        costs = (self.enemies != 0).astype(int) * self._genome.get('toEnemies')
        blured = gaussian_filter(costs,sigma=1, mode="nearest")
        blured[self.pfSize, self.pfSize] = 0
        return blured

    def costsFood(self):
        return -(self.food != 0).astype(int)

    def costsFriends(self):
        costs = (self.enemies != 0).astype(int) * self._genome.get('toFriends')
        blured = gaussian_filter(costs,sigma=1, mode="nearest")
        blured[self.pfSize, self.pfSize] = 0
        return blured

    def costsMove(self, path):
        return np.linalg.norm(path)*self.costsPerUnitMove

    def costsRandom(self, factor):
        return self.rg.random(np.shape(self.distanceCosts)) * factor

# =============================================================================
# getters
# =============================================================================
    @ property
    def color(self):
        return self._color

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