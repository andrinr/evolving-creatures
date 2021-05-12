import numpy as np
from helpers import normalize, sRound, closestPoint
from scipy.ndimage import gaussian_filter
from itertools import product
from genome import Genome

class Figure(object):

    def __init__(self):
        self._color = 'red'
        self._energy = 0

    @ property
    def energy(self):
        return self._energy

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
    costsPerUnitMove = 0.1
    genomThreshold = 0.2
    pfSize = 4
    pfShape = [pfSize, pfSize]
    distanceCosts = np.zeros((pfSize*2+1, pfSize*2+1))
    rg = np.random.default_rng()

    # Used to associate each creature with an ID, NOT to keep track of total number of creatures
    # Keeping track of all creatures is done in the grid class
    count = 0

    def __init__(self, grid, pos, energy):
        super().__init__()
        self._pos = np.array(pos)
        self._genome = Genome()
        self._grid = grid

        self.food = None
        self.creatures = None
        self.enemies = None
        self.friends = None
        self.congener = None
        self.finalCosts = 0

        self._grid.creatureList.append(self)
        self._grid.creatureGrid[self.gridIndex] = self
        self._id = Creature.count
        self._energy = energy

        # Assuming all creatures have the same perceptualFieldSize
        # We calculate this here to save computing costs
        if not self.count:
            self.costsDistances()

        Creature.count += 1

    def __str__(self):
        return 'Creature ID. = {}\nEnergyLevel = {}\n'.format(self.id, self.energy)


    def update(self):

        self.spotFood()
        self.spotCreatures()
        self.spotEnemies()
        self.spotFriends()
        
        foodCosts = self.costsFood()
        creatureCosts = self.costsCreatures()
        # enCosts = self.costsEnemies()
        # frCosts = self.costsFriends()
        randomCosts = self.costsRandom(0.02)
        topoCosts = self.perceptualField(self._grid.topography)

        scentCosts = self.perceptualField(self._grid.scent)

        # Blur matrix to avoid creature from moving to food next to a threat
        creatureCosts = gaussian_filter(creatureCosts, sigma=0.5, mode="nearest")
        finalCosts = foodCosts + creatureCosts + randomCosts + topoCosts + scentCosts + self.distanceCosts
        # Avoid staying at the same place
        finalCosts[self.pfSize, self.pfSize] = 1
        # Store final costs for plotting
        self.finalCosts = finalCosts

        target = np.unravel_index(finalCosts.argmin(), finalCosts.shape) - np.array([self.pfSize, self.pfSize])
        move = sRound(normalize(target))
        self.moveBy(move)
        self._grid.scent[self.gridIndex] += 0.3

        if self._grid.foodGrid[self.gridIndex]:
            self.eat()

        # TODO: define this by genes
        if self.energy > 2.0:
            self.breed()

        

# =============================================================================
# actions
# =============================================================================
    def eat(self):
        self._energy += self._grid.foodGrid[self.gridIndex].energy
        self._grid.foodGrid[self.gridIndex] = 0

    def kill(self):
        self._grid.creatureList.remove(self)
        self._grid.creatureGrid[self.gridIndex] = 0

    # Move self, update grid data structure and energylevel
    def moveBy(self, vector):
        self._energy -= self.costsMove(vector)
        if self._energy <= 0:
            self.kill()
            return
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
        # Set the im of new children, limited by the avaiable space
        nChildrenAim = min(self.rg.integers(1, high=4), np.count_nonzero(free))
        nChildrenActual = 0

        # Randomly iterate over adjecent cells
        iRand = np.linspace(0, 2, 3, dtype=int)
        self.rg.shuffle(iRand)
        jRand = np.linspace(0, 2, 3, dtype=int)
        self.rg.shuffle(jRand)
        
        for i, j in product(iRand, jRand):
            # Spawn creature when cell is free
            if (free[i,j]):
                nChildrenActual += 1
                Creature(self._grid, self._pos + np.array([i-1,j-1]), self.energy/nChildrenAim)
                # Break loop when right amount of children is reached
                if (nChildrenActual == nChildrenAim):
                    break
            
        self.kill()

            

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
        self.creatures[self.pfSize, self.pfSize] = 0

    def spotEnemies(self):
        e = self.creatures.copy()
        n = e.shape[0]
        for i, j in product(range(n), range(n)):
            if e[i,j] and e[i,j].genome.genes['enemy'].value * self.genome.genes['enemy'].value > 0:
                # in this case the creature is not an enemy since enemies have 
                # different signs hence the product is always positive if two 
                # creatures are of the same species
                e[i,j] = 0
        self.enemies = e

    def spotFood(self):
        self.food = self.perceptualField(self._grid.foodGrid)

    def spotFriends(self):
        self.friends = self.creatures[self.enemies != self.creatures]

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
        return (self.enemies != 0).astype(int) * 100

    def costsFood(self):
        return -(self.food != 0).astype(int)

    def costsFriends(self):
        return (self.friends != 0).astype(int) * 10

    def costsMove(self, path):
        return np.linalg.norm(path)*self.costsPerUnitMove

    def costsRandom(self, factor):
        return self.rg.random(np.shape(self.distanceCosts)) * factor

# =============================================================================
# getters
# =============================================================================
    @ property
    def deathRate(self):
        return self._genome[3]

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
    def moveToEnemy(self):
        return self._genome[1]

    @ property 
    def moveToFriend(self):
        return self._genome[2]

    @ property 
    def moveToPlant(self):
         return self._genome[0]

    @ property
    def replicationRate(self):
        return self._genome[4]

    @ property
    def x(self):
        return self._pos[0]

    @ property
    def y(self):
        return self._pos[1]

# =============================================================================
# setters
# =============================================================================
    @ deathRate.setter
    def deathRate(self, p):
        self._genome[3] = p

    @ moveToEnemy.setter
    def moveToEnemy(self, p):
        self._genome[1] = p

    @ moveToFriend.setter
    def moveToFriend(self, p):
        self._genome[2] = p

    @ moveToPlant.setter
    def moveToPlant(self, p):
        self._genome[0] = p

    @ replicationRate.setter
    def replicationRate(self, p):
        self._genome[4] = p


