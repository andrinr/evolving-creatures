import numpy as np
from grid import Figure, Food
from scipy.sparse import random

class Creature(Figure):

    # Creature params
    genomThreshold = 0.2

    creatureList = []
    creatureGrid = np.array([],dtype=object)
    foodGrid = np.array([],dtype=object)

    rg = np.random.default_rng()

    @staticmethod
    def updateAll():
        n = len(Creature.creatureList)
        indices = np.linspace(0, n-1, num=n, dtype=int)
        Creature.rg.shuffle(indices)

        for index in indices:
            Creature.creatureList[index].update()

        return

    @staticmethod
    def initAll(N, creatureDensity, foodDensity):
        Creature.N = N
        Creature.creatureGrid = np.zeros((N,N), dtype=object)
        Creature.foodGrid = np.zeros((N,N), dtype=object)

        for i in range(N):
            for j in range(N):
                if (Creature.rg.random() < creatureDensity):
                    Creature.creatureGrid[i,j] = Creature(np.array([i,j]), Creature.rg.random())

                if (Creature.rg.random() < foodDensity):
                    Creature.foodGrid[i,j] = Food()

    @staticmethod
    def plotAll(ax):
        for creature in Creature.creatureList:
            print(creature.color)
            ax.scatter(creature.x, creature.y)

        # Plot food
        ax.imshow(Creature.foodGrid != 0)

    def __init__(self, pos, radius):
        super().__init__()
        self._pos = pos
        self._radius = radius
        Creature.creatureList.append(self)
        Creature.creatureGrid[self._pos] = self

    def update(self):
        # TODO: Make updates
        return

    def kill(self):
        Creature.creatureList.remove(self)
        Creature.creatureGrid[self._pos] = 0

    @ property
    def x(self):
        return self._pos[0]

    @ property
    def y(self):
        return self._pos[1]

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
        r = self._radius
        perceptualField = self.foodGrid[self.x-r : self.x+r+1, self.y-r : self.y+r+1]
        locatedFood = np.argwhere(perceptualField)

    # TODO: exclude self
    def perceiveCreatures(self):
        r = self._radius
        perceptualField = self.creatureGrid[self.x-r : self.x+r+1, self.y-r : self.y+r+1]
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
        return self._pos[1] != Creature.N

    def canMoveLeft(self):
        return self._pos[1] != 0
    
    def canMoveDown(self):
        return self._pos[0] != Creature.N
    
    def canMoveUp(self):
        return self._pos[0] != 0


Creature.initAll(10, 0.1, 0.2)
Creature.updateAll()

print("Number of creatures: ", len(Creature.creatureList))