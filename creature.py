import numpy as np
# from scipy.sparse import random
from helpers import normalize, sRound, closestPoint

class Figure(object):

    def __init__(self, pos):
        self._color = 'red'
        self._energy = 0
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

    @ property
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
        self._energy = 1

class Creature(Figure):

    # Static
    maxMoves = 10
    genomThreshold = 0.2
    perceptualFieldSize = 4
    costMatrix = np.zeros((perceptualFieldSize*2+1, perceptualFieldSize*2+1))
    rg = np.random.default_rng()

    # Used to associate each creature with an ID, NOT to keep track of total number of creatures
    # Keeping track of all creatures is done in the grid class
    count = 0

    def __init__(self, grid, pos, radius):
        super().__init__(pos)
        self._grid = grid
        self._radius = radius
        self._grid.creatureList.append(self)
        self._id = Creature.count
        self._energy = 1
        # Assuming all creatures have the same perceptualFieldSize
        # We calculate this here to save computing costs
        if self.count == 0:
            for i in range(2 * self.perceptualFieldSize + 1):
                for j in range(2 * self.perceptualFieldSize + 1):
                    self.costMatrix[i,j] = np.linalg.norm(np.array([i - self.perceptualFieldSize, j - self.perceptualFieldSize]))

            self.costMatrix[self.perceptualFieldSize, self.perceptualFieldSize] = 1

        Creature.count += 1

    def update(self):
        foodCosts = -self.perceiveFood()
        randomCosts = self.rg.random(np.shape(self.costMatrix)) * 0.1
        topoCosts = self.perceptualField(self._grid.topography)
        # TODO: get this working
        #finalCosts = np.multiply(Creature.costMatrix, (foodCosts + randomCosts ))
        
        # Wird randomCosts für random moves benutzt? falls ja, ev. besser wir individualisieren die Bewegungen.
        # foodcosts + costmatrix kann dazuführen, dass es günstiger ist, sich an einen andere Ort zu bewegen als direkt zum food. 
        # Die Idee ist genial, aber muss noch gut durchdacht werden, vorallem weil wir später noch Predators hinzufügen. Wie entscheidet sie, 
        # ob sie nun zum food läuft, davonläuft oder angreift? 

        finalCosts = foodCosts + randomCosts + topoCosts + self.costMatrix*0.1

        target = np.unravel_index(finalCosts.argmin(), finalCosts.shape) - np.array([Creature.perceptualFieldSize, self.perceptualFieldSize])
        move = sRound(normalize(target))
        self.moveBy(move)

        if self._grid.foodGrid[self.gridIndex]:
            self.eat()

    def eat(self):
        self._energy += self._grid.foodGrid[self.gridIndex].energy
        self._grid.foodGrid[self.gridIndex] = 0

    def kill(self):
        self._grid.creatureList.remove(self)
        self._grid.creatureGrid[self.gridIndex] = 0

    def energyCost(self, path):
        return np.linalg.norm(path)/self.maxMoves

    # Move self, update grid data structure and energylevel
    def moveBy(self, vector):
        self._energy -= self.energyCost(vector)
        if self._energy <= 0:
            self.kill()
        self._grid.creatureGrid[self.gridIndex] = 0
        self._pos = self._pos + vector
        self._grid.creatureGrid[self.gridIndex] = self

    def ckeckEnergy(self, path):
        pass

    @ property
    def id(self):
        return self._id

    def perceptualField(self, grid):
        r = Creature.perceptualFieldSize
        lx = self.x - r
        ly = self.y - r
        ux = self.x + r + 1
        uy = self.y + r + 1
        return grid[lx : ux, ly : uy]

    # Assuming: creature cannot perceive food when another creatures is located there
    def perceiveFood(self):
        r = self.perceptualFieldSize
        fieldFood = self.perceptualField(self._grid.foodGrid)
        fieldCreatures = self.perceptualField(self._grid.creatureGrid)
        # Make sure self is counted as other creature
        fieldCreatures[r, r] = 0
        field = np.logical_and(fieldFood != 0, fieldCreatures == 0)
        return field.astype(int)

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
        return self._pos[1] != self._grid.N + self._grid.ghostZone

    def canMoveLeft(self):
        return self._pos[1] != self._grid.ghostZone
    
    def canMoveDown(self):
        return self._pos[0] != self._grid.N + self._grid.ghostZone
    
    def canMoveUp(self):
        return self._pos[0] != self._grid.ghostZone

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