import numpy as np

class Evolution:

    def __init__(self, gridSize, vDist):

        self.__gridSize = gridSize
        self.__vDist = vDist

        # Init random gnerator
        self.__rg = np.random.default_rng()

        # Double bookeeping to avoid n*n checks
        self.__creatureList = []
        self.__creatureGrid = np.zeros(gridSize)

        self.__foodGrid = np.sign(self.__rg.random(gridSize)-0.95)
        
        # TODO: height map with perlin noise

    @ property
    def foodGrid(self):
        return self.__foodGrid

    @ property
    def creatureList(self):
        return self.__creatureList

    def update(self):
        # Make sure no creature benefits from being picked first at all times
        indices = np.linspace(0, len(self.__creatureList), num=len(self.__creatureList))
        print(indices)
        self.__rg.shuffle(indices)
        print(indices)
        for index in indices:
            print(int(index))
            creature = self.__creatureList[int(index)]
            if (self.__creatureGrid[creature.x, creature.y] != creature):
                print("ERROR in bookeeping of creatures")

            # Vision logic
            visibleCreatures = []
            visibleFood = []
            for i in range((creature.x - self.__vDist) % self.__gridSize[0], (creature.x + self.__vDist) % self.__gridSize[0]):
                for j in range((creature.y - self.__vDist) % self.__gridSize[1], (creature.y + self.__vDist) % self.__gridSize[1]):

                    vector = np.array(i,j) - creature.pos

                    if self.__creatureGrid[i,j] != 0:
                        visibleCreatures.append((vector, self.__creatureGrid[i,j]))

                    if self.__foodGrid[i,j] != 0:
                        visibleFood.append((vector, self.__foodGrid[i,j]))

            self.__creatureList[index].vision(visibleCreatures, visibleFood)
