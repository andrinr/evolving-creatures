import numpy as np
from scipy.sparse import random
from helpers import normalize, sRound, closestPoint

class Figure(object):
    def __init__(self, pos):
        self._energy = 0.5
        self._color = 'red'
        self._pos = np.array(pos)

    def __mul__(self, value):
        return self if value != 0 else 0

    def __rmul__(self, value):
        return self if value != 0 else 0

    # Positions could proably be removed from superclass
    @ property
    def x(self):
        return self._pos[0]

    @ property
    def y(self):
        return self._pos[1]

    @property
    def gridIndex(self):
        return (self.x, self.y)

    @ property
    def energy(self):
        return self._energy

    @ property
    def color(self):
        return self._color

    def update(self):
        return

class Food(Figure):
    def __init__(self, pos):
        super().__init__(pos)
        self._color = 'green'

class Creature(Figure):

    # Creature params
    genomThreshold = 0.2
    perceptualFieldSize = 2
    rg = np.random.default_rng()

    # Used to associate each creature with an ID, NOT to keep track of total number of creatures
    # Keeping track of all particles is done in the grid class
    count = 0

    def __init__(self, grid, pos, radius):
        super().__init__(pos)
        self._grid = grid
        self._radius = radius
        self._grid.creatureList.append(self)
        self._id = Creature.count
        Creature.count += 1

    def update(self):
        foods = self.perceiveFood()
        # If there is a piece of food within the perception field, move there
        if (np.shape(foods)[0] > 0):
            # Shuffle foods to avoid bias from same distanced food positions
            Creature.rg.shuffle(foods)
            closest = foods[np.argmin(np.linalg.norm(foods, axis=1))]
            move = sRound(normalize(closest))
            if (np.linalg.norm(move) == 0):
                self.eat(self._pos + move)
            else:
                self.moveBy(move)
        else:
            # TODO: Creatures can move out of grid
            move = Creature.rg.integers(-1, high=2, size=2)
            self.moveBy(move)


    def eat(self, pos):
        self._grid.foodGrid[self.gridIndex] = 0

    def kill(self):
        self._grid.creatureList.remove(self)
        self._grid.creatureGrid[self.gridIndex] = 0

    def energyCost(self, path):
        return np.linalg.norm(path) * self._radius

    # Move self and update grid data structure
    def moveBy(self, vector):
        self._grid.creatureGrid[self.gridIndex] = 0
        self._pos = self._pos + vector
        self._grid.creatureGrid[self.gridIndex] = self

    @ property
    def id(self):
        return self._id

    # @ property 
    # def moveToPlant(self):
    #     return self.paramters[0]

    # @ property 
    # def moveToEnemy(self):
    #     return self.paramters[1]

    # @ property 
    # def moveToFriend(self):
    #     return self.paramters[2]

    # @ property
    # def deathRate(self):
    #     return self.parameters[3]

    # @ property
    # def replicationRate(self):
    #     return self.parameters[4]

    # @ moveToPlant.setter
    # def moveToPlant(self, p):
    #     self.parameters[0] = p

    # @ moveToEnemy.setter
    # def moveToEnemy(self, p):
    #     self.parameters[1] = p

    # @ moveToFriend.setter
    # def moveToFriend(self, p):
    #     self.parameters[2] = p

    # @ deathRate.setter
    # def deathRate(self, p):
    #     self.parameters[3] = p

    # @ replicationRate.setter
    # def replicationRate(self, p):
    #     self.parameters[4] = p

    def perceptualField(self, grid):
        r = Creature.perceptualFieldSize
        lx = self.x - r
        ly = self.y - r
        ux = self.x + r + 1
        uy = self.y + r + 1
        return grid[lx : ux, ly : uy]

    # Assuming: creature cannot perceive food when another creatures is located there
    def perceiveFood(self):
        r = Creature.perceptualFieldSize
        fieldFood = self.perceptualField(self._grid.foodGrid)
        fieldCreatures = self.perceptualField(self._grid.creatureGrid)
        # Make sure self is counted as other creature
        fieldCreatures[r,r] = 0
        field = np.logical_and(fieldFood != 0, fieldCreatures == 0)
        # Offset to have self centered coordinates
        return np.argwhere(field.astype(int)) - np.array([r,r])

    # TODO: exclude self
    def perceiveCreatures(self):
        r = Creature.perceptualFieldSize
        field = self.perceptualField(self._grid.foodGrid)
        return np.argwhere(field) - np.array([r,r])
    
    def moveRight(self, n):
        self._pos += np.array((0,1))
    
    def moveLeft(self):
        self._pos += np.array((0, -1))
    
    def moveUp(self):
        self._pos += np.array((-1,0))
    
    def moveDown(self):
        self._pos += np.array((1,0))

    def moveUpRight(self):
        self._pos += np.array((-1, 1))

    def moveUpLeft(self):
        self._pos += np.array((-1, -1))

    def moveDownRight(self):
        self._pos += np.array((1, 1))

    def moveDownLeft(self):
        self._pos += np.array((1, -1))

    def canMoveRight(self):
        return self._pos[1] != self._grid.N

    def canMoveLeft(self):
        return self._pos[1] != 0
    
    def canMoveDown(self):
        return self._pos[0] != self._grid.N
    
    def canMoveUp(self):
        return self._pos[0] != 0
