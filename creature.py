# import numpy as np
# from grid import GridItem

# class Creature(GridItem):

#     def __init__(self, pos):
#         super().__init__(pos)

#         # Init random gnerator
#         self.__rg = np.random.default_rng()

#         return

#     # Creature processes senses and plans next move
#     # Illegal moves (Moving into occupied field) have to be checked for in this function
#     def process(self, otherCreatures):
#         self.__otherCreatures = otherCreatures
#         self._pos = self._pos + self.__rg.integers(low=-1, high=2, size=2)
#         return


#     def plot(self, ax):
#         ax.scatter(self.x, self.y)

#         for other in self.__otherCreatures:

#             ax.plot(
#                 [self.x, other[0][0]],
#                 [self.y, other[0][1]], c="red")
            

import numpy as np

class Creature:

    genomThreshold = 0.2
    maxPos = 0
    number = 0

    def __init__(self, pos, energy, N):
        Creature.number += 1
        Creature.maxPos = N-1
        self.pos = pos
        self.energy = 1
        self.radius = 2

        self.alive = True
        # self.isMale = False

        # self.parameters = np.random.random(N)

    @ property
    def x(self):
        return self.pos[1]

    @ property
    def y(self):
        return self.pos[0]

    def energyCost(self, path):
        return np.linalg.norm(path) * self.radius

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

    def died(self):
        self.alive = False
        Creature.number -= 1

    def perception(self, x, y):
        r = self.radius
        perceptualField = self.grid[x-r : x+r+1, y-r : y+r+1]
        locatedFood = np.argwhere(perceptualField)
    
    def moveRight(self, n):
        self.pos += np.array((0,1))
    
    def moveLeft(self):
        self.pos += np.array((0, -1))
    
    def moveUp(self):
        self.pos += np.array((-1,0))
    
    def moveDown(self):
        self.pos += np.array((1,0))

    def moveUpRight(self):
        self.pos += np.array((-1, 1))

    def moveUpLeft(self):
        self.pos += np.array((-1, -1))

    def moveDownRight(self):
        self.pos += np.array((1, 1))

    def moveDownLeft(self):
        self.pos += np.array((1, -1))

    def canMoveRight(self):
        return self.pos[1] != self.maxPos

    def canMoveLeft(self):
        return self.pos[1] != 0
    
    def canMoveDown(self):
        return self.pos[0] != self.maxPos
    
    def canMoveUp(self):
        return self.pos[0] != 0
