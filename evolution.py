import numpy as np
from creature import Creature
from grid import Grid

class Evolution:

    def __init__(self, N, nCreatures):

        self.__N = N

        # Init random gnerator
        self.__rg = np.random.default_rng()

        self.__creatureList = []
        self.__foodList = []

        positions = self.__rg.choice(self.__N, (nCreatures, 2))

        for i in range(nCreatures):
            self.__creatureList.append(Creature(positions[i,:]))

        # TODO: height map with perlin noise

    @ property
    def creatureList(self):
        return self.__creatureList

    def update(self):
        # Make sure no creature benefits from being picked first at all times
        indices = np.linspace(0, len(self.__creatureList)-1, num=len(self.__creatureList))
        self.__rg.shuffle(indices)

        creatureGrid = Grid(self.__N, self.__creatureList)
        for index in indices:
            creature = self.__creatureList[int(index)]

            otherCreatures = creatureGrid.sense(6, creature.x, creature.y)
            creature.process(otherCreatures)

        for creature in self.__creatureList:
            creature.move()

    def plot(self, ax):
        for creature in self.__creatureList:
            creature.plot(ax)

            