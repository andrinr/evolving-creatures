import numpy as np
from scipy.sparse import random


class Figure(object):
    def __init__(self):
        self._energy = 0.5
        self._color = 'red'

    def __mul__(self, value):
        return self if value != 0 else False

    def __rmul__(self, n):
        return Figure() if n else False

    @ property
    def energy(self):
        return self._energy

    @ property
    def color(self):
        return self._color

class Food(Figure):
    def __init__(self):
        super().__init__()
        self._color = 'green'

