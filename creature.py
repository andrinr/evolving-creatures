import numpy as np

class creature:

    def __init__(self, pos):
        return

    
    # These interfaces seem to make sense for world interaction
    def vision(self, creatures, foods):
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