import numpy as np
from scipy.sparse import random


class Food(object):
    def __init__(self):
        self.__energy = 0.5
        self.__color = 'green'

    def __mul__(self, n):
        return Food() if n else False

    def __rmul__(self, n):
        return Food() if n else False

    @ property
    def energy(self):
        return self.__energy

    def color(self):
        return self.__green


# class GridItem:

#     def __init__(self, pos):
#         self.__pos = pos

#     @ property
#     def x(self):
#         return self._pos[0]

#     @ x.setter
#     def x(self, value):
#         self._pos[0] = value

#     @ property
#     def y(self):
#         return self._pos[1]

#     @ y.setter
#     def y(self, value):
#         self._pos[1] = value

#     @ property
#     def pos(self):
#         return self._pos

#     @ property
#     def itemType(self):
#         return self.__type


# Data structure to quickly find items on grid
class Grid:

    def __init__(self, N):
        self.__N = N
        self.grid = np.ones((N, N), dtype=bool)
        self.foodGrid = np.ones((N,N), dtype=object) * Food()
    
    def placeRandomFood(self, density):
        '''
        Parameters
        ----------
        density : float
            density of the food distribution

        place some food randomly in the grid
        '''
        foodMask = random(self.N, self.N, density=density, dtype=bool) # sparse boolean matrix
        self.grid = self.foodGrid * foodMask



