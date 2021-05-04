import numpy as np
from grid import GridItem

class Creature(GridItem):

    def __init__(self, pos):
        super().__init__(pos)

        # Init random gnerator
        self.__rg = np.random.default_rng()

        return

    # Creature processes senses and plans next move
    def process(self, otherCreatures):
        self.__otherCreatures = otherCreatures
        self.__nextPos = self._pos + self.__rg.integers(low=-1, high=2, size=2)
        return

    # Creature makes next move
    # This cannot be made in the process() method since then we would 
    # need to update the the grid n times, which is very ineffcient
    # Theoretically creatures could update their positions inside the grid themselves
    def move(self):
        self._pos = self.__nextPos

    def plot(self, ax):
        ax.scatter(self.x, self.y)

        for other in self.__otherCreatures:

            ax.plot(
                [self.x, other[0][0]],
                [self.y, other[0][1]], c="red")