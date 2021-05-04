import numpy as np
from grid import GridItem

class Creature(GridItem):

    def __init__(self, pos):
        super().__init__(pos)

        # Init random gnerator
        self.__rg = np.random.default_rng()
        return

    # These interfaces seem to make sense for world interaction
    def process(self, items):
        self._pos += self.__rg.integers(low=-1, high=2, size=2)
        return
