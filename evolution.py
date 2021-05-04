import numpy as np
from creature import Creature

class Evolution:

    def __init__(self, gridSize, vDist, nCreatures):

        self.__gridSize = gridSize
        self.__vDist = vDist

        # Init random gnerator
        self.__rg = np.random.default_rng()

        # Double bookeeping to avoid n*n checks
        self.__creatureList = []
        self.__creatureGrid = np.full(gridSize, -1)

        self.__foodGrid = np.sign(self.__rg.random(gridSize)-0.95)

        positions = self.__rg.choice(gridSize[0], (nCreatures, 2))

        print(positions)

        for i in range(nCreatures):
            self.__creatureList.append(Creature(positions[i,:]))

        self.__updateGrid()
        
        # TODO: height map with perlin noise

    @ property
    def foodGrid(self):
        return self.__foodGrid

    @ property
    def creatureList(self):
        return self.__creatureList

    def __updateGrid(self):
        self.__creatureGrid = np.full(self.__gridSize, -1)
        for i in range(len(self.__creatureList)):
            creature = self.__creatureList[i]
            self.__creatureGrid[int(creature.x), int(creature.y)] = i


    def update(self):
        # Make sure no creature benefits from being picked first at all times
        indices = np.linspace(0, len(self.__creatureList)-1, num=len(self.__creatureList))
        self.__rg.shuffle(indices)
        for index in indices:
            creature = self.__creatureList[int(index)]

            #if (self.__creatureGrid[creature.x, creature.y] != index):
            #    print("ERROR in bookeeping of creatures")

            # Vision logic
            visibleCreatures = []
            visibleFood = []
            for i in range((creature.x - self.__vDist) % self.__gridSize[0], (creature.x + self.__vDist) % self.__gridSize[0]):
                for j in range((creature.y - self.__vDist) % self.__gridSize[1], (creature.y + self.__vDist) % self.__gridSize[1]):

                    vector = np.array([i,j]) - creature.pos

                    if self.__creatureGrid[i,j] != 0:
                        visibleCreatures.append((vector, self.__creatureList[self.__creatureGrid[i,j]]))

                    if self.__foodGrid[i,j] != 0:
                        visibleFood.append((vector, self.__foodGrid[i,j]))

            self.__creatureList[int(index)].process(visibleCreatures, visibleFood, self.__gridSize)
