import numpy as np

class creature:

    def __init__(self, pos):
        self.__pos = pos
        self.__energy = 1
        return

    def vision(self, creatures, foods):
        return

    @ property
    def energy(self):
        return self.__energy

    @ property
    def x(self):
        return self.__pos[0]

    @ property
    def y(self):
        return self.__pos[1]

    @property
    def pos(self):
        return self.__pos