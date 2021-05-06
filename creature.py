import numpy as np
from scipy.sparse import random
from helpers import normalize, sRound

class Figure(object):
    def __init__(self, pos):
        self._energy = 0.5
        self._color = 'red'
        self._pos = np.array(pos)

    # Vectors to food objects are easier to calculate thus I did 
    # include the position in the superclass
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

        if (len(foods) > 1):
            vector = foods[0]
            print(normalize(vector))
            move = sRound(normalize(vector))
            print("move: ", move)
            self.move(move)

        return

    def kill(self):
        self.grid.creatureList.remove(self)
        self.grid.creatureGrid[self.gridIndex] = 0

    def energyCost(self, path):
        return np.linalg.norm(path) * self._radius

    def move(self, vector):
        self._grid.creatureGrid[self.gridIndex] = 0
        self._pos = self._pos + vector
        self._grid.creatureGrid[self.gridIndex] = self

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
        r = Creature.perceptualFieldSize
        x = int(self.x)
        y = int(self.y)
        perceptualField = self._grid.foodGrid[x-r : x+r+1, y-r : y+r+1]
        return np.argwhere(perceptualField) - np.array([r,r])

    # TODO: exclude self
    def perceiveCreatures(self):
        r = Creature.perceptualFieldSize
        perceptualField = self._grid.creatureGrid[self.x-r : self.x+r+1, self.y-r : self.y+r+1]
        return np.argwhere(perceptualField)
    
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
