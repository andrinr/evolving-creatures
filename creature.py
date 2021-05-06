import numpy as np
from scipy.sparse import random

class Figure(object):
    def __init__(self, pos):
        self._energy = 0.5
        self._color = 'red'
        self._pos = pos

    # Vectors to food objects are easier to calculate thus I did 
    # include the position in the superclass
    @ property
    def x(self):
        return self._pos[0]

    @ property
    def y(self):
        return self._pos[1]

    @ property
    def energy(self):
        return self._energy

    @ property
    def color(self):
        return self._color

    def update():
        return

class Food(Figure):
    def __init__(self, pos):
        super().__init__(pos)
        self._color = 'green'

class Creature(Figure):

    # Creature params
    genomThreshold = 0.2
    perceptualFieldSize = 3
    rg = np.random.default_rng()

    def __init__(self, grid, pos, radius):
        super().__init__(pos)
        self._grid = grid
        self._radius = radius
        self._grid.creatureList.append(self)

    def update(self):
        foods = self.perceiveFood()
        return

    def kill(self):
        self.grid.creatureList.remove(self)
        self.grid.creatureGrid[self._pos] = 0

    def energyCost(self, path):
        return np.linalg.norm(path) * self._radius

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

    def perceiveFood(self):
        r = perceptualFieldSize
        perceptualField = self.grid.foodGrid[self.x-r : self.x+r+1, self.y-r : self.y+r+1]
        locatedFood = np.argwhere(perceptualField)

    # TODO: exclude self
    def perceiveCreatures(self):
        r = perceptualFieldSize
        perceptualField = self.grid.creatureGrid[self.x-r : self.x+r+1, self.y-r : self.y+r+1]
        locatedCreatures = np.argwhere(perceptualField)
    
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
        return self._pos[1] != self.grid.N

    def canMoveLeft(self):
        return self._pos[1] != 0
    
    def canMoveDown(self):
        return self._pos[0] != self.grid.N
    
    def canMoveUp(self):
        return self._pos[0] != 0
