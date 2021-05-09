import numpy as np
# from scipy.sparse import random
from helpers import normalize, sRound, closestPoint
from scipy.ndimage import gaussian_filter

class Figure(object):

    def __init__(self, pos):
        self._color = 'red'
        self._energy = 0
        self._pos = np.array(pos)

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
    distanceCosts = np.zeros((perceptualFieldSize*2+1, perceptualFieldSize*2+1))
    rg = np.random.default_rng()

    # Used to associate each creature with an ID, NOT to keep track of total number of creatures
    # Keeping track of all creatures is done in the grid class
    count = 0

    def __init__(self, grid, pos, radius, genome=rg.random(5)):
        super().__init__(pos)
        self._grid = grid
        self._radius = radius
        self._genome = genome
        self._grid.creatureList.append(self)
        self._id = Creature.count
        self._energy = 1
        # Assuming all creatures have the same perceptualFieldSize
        # We calculate this here to save computing costs
        if self.count == 0:
            for i in range(2 * self.perceptualFieldSize + 1):
                for j in range(2 * self.perceptualFieldSize + 1):
                    self.distanceCosts[i,j] = np.linalg.norm(np.array([i - self.perceptualFieldSize, j - self.perceptualFieldSize]))
            
            # Normalize
            self.distanceCosts /= np.linalg.norm(np.array([self.perceptualFieldSize, self.perceptualFieldSize]))

        Creature.count += 1

    def update(self):
        foodCosts = -self.perceiveFood()
        creatureCosts = self.perceiveCreatures()
        randomCosts = self.rg.random(np.shape(self.distanceCosts)) * 0.02
        topoCosts = self.perceptualField(self._grid.topography)
        scentCosts = self.perceptualField(self._grid.scent)
        #finalCosts = np.multiply(Creature.costMatrix, (foodCosts + randomCosts ))
        
        # Wird randomCosts für random moves benutzt? falls ja, ev. besser wir individualisieren die Bewegungen.
        # foodcosts + costmatrix kann dazuführen, dass es günstiger ist, sich an einen andere Ort zu bewegen als direkt zum food. 
        # Die Idee ist genial, aber muss noch gut durchdacht werden, vorallem weil wir später noch Predators hinzufügen. Wie entscheidet sie, 
        # ob sie nun zum food läuft, davonläuft oder angreift? 
        
        # Antwort:
        # Die randomCosts werden für zufällige Bewegungen genutzt wenn keine anderen Objekte in der Nähe sind
        # Die randomCosts können mit einem sehr kleinen Faktor multipliziert werden, somit kann verhindert werden dass dumme entscheidungen getroffen werden

        # Objekte denen man sich annähern soll haben ein negatives gewicht, objekte von denen man sich entfernen soll ein positives gewicht
        # Die cost matrix wird geblurt und nacher das minimum gesucht. So kann verindert werden, dass sich eine Creatur in die nähe eines Feindes bewegt,
        # Weil daneben essen liegt

        # Blur matrix to avoid creature from moving to food next to a threat
        creatureCosts = gaussian_filter(creatureCosts, sigma=0.5, mode="nearest")
        finalCosts = foodCosts + creatureCosts + randomCosts + topoCosts + scentCosts + self.distanceCosts
        # Avoid staying at the same place
        finalCosts[self.perceptualFieldSize, self.perceptualFieldSize] = 2
        # Store final costs for plotting
        self.finalCosts = finalCosts

        target = np.unravel_index(finalCosts.argmin(), finalCosts.shape) - np.array([self.perceptualFieldSize, self.perceptualFieldSize])
        move = sRound(normalize(target))
        self.moveBy(move)
        self._grid.scent[self.gridIndex] += 0.3

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
    def perceiveEnemies(self):
        field = self.perceptualField(self._grid.creatureGrid)
        fieldCreatures = field != 0

        def distance(a):
            if a != 0:  
                print(a)
                return np.linalg.norm(a.genome, self.genome, ord='fro')
            else:
                return 1000
        
        vfunc = np.vectorize(distance)
        #print(vfunc(field))

        #enmemyCreatures = np.logical_and(distance(field) > self.genomThreshold, fieldCreatures)

        #print(enemyCreatures)
        # Make sure self is counted as other creature
        return fieldCreatures.astype(int)

    # TODO: exclude self
    def perceiveFriends(self):
        fieldCreatures = self.perceptualField(self._grid.creatureGrid) != 0
        # Make sure self is counted as other creature
        return fieldCreatures.astype(int)

    # TODO: exclude self
    def perceiveCreatures(self):
        fieldCreatures = self.perceptualField(self._grid.creatureGrid) != 0
        # Make sure self is counted as other creature
        return fieldCreatures.astype(int)

    @ property 
    def genome(self):
         return self._genome

    @ property 
    def moveToPlant(self):
         return self._genome[0]

    @ property 
    def moveToEnemy(self):
        return self._genome[1]

    @ property 
    def moveToFriend(self):
        return self._genome[2]

    @ property
    def deathRate(self):
        return self._genome[3]

    @ property
    def replicationRate(self):
        return self._genome[4]

    @ moveToPlant.setter
    def moveToPlant(self, p):
        self._genome[0] = p

    @ moveToEnemy.setter
    def moveToEnemy(self, p):
        self._genome[1] = p

    @ moveToFriend.setter
    def moveToFriend(self, p):
        self._genome[2] = p

    @ deathRate.setter
    def deathRate(self, p):
        self._genome[3] = p

    @ replicationRate.setter
    def replicationRate(self, p):
        self._genome[4] = p