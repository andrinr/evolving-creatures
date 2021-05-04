import numpy as np
from grid import GridItem

class Creature(GridItem):

    def __init__(self, pos):
        super().__init__(pos)

        # Init random gnerator
        self.__rg = np.random.default_rng()

        return

    # Creature processes senses and plans next move
    # Illegal moves (Moving into occupied field) have to be checked for in this function
    def process(self, otherCreatures):
        self.__otherCreatures = otherCreatures
        self._pos = self._pos + self.__rg.integers(low=-1, high=2, size=2)
        return


    def plot(self, ax):
        ax.scatter(self.x, self.y)

        for other in self.__otherCreatures:

            ax.plot(
                [self.x, other[0][0]],
                [self.y, other[0][1]], c="red")