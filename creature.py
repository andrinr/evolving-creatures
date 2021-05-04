import numpy as np

class Creature:

    def __init__(self, pos):
        self.__pos = pos

        # Init random gnerator
        self.__rg = np.random.default_rng()
        return

    # These interfaces seem to make sense for world interaction
    def process(self, creatures, foods, gridSize):
        self.pos[0] = (self.pos[0] + self.__rg.integers(low=-1,high=2) ) % gridSize[0]
        self.pos[1] = (self.pos[1] + self.__rg.integers(low=-1,high=2) ) % gridSize[1]

        return

    @ property
    def x(self):
        return self.__pos[0]

    @ property
    def y(self):
        return self.__pos[1]

    @property
    def pos(self):
        return self.__pos