import numpy as np

class grid:

    def __init__(self, N, M):
        self.rg = np.random.default_rng()
        self.height = self.rg.random((N,M))
        self.food = self.rg.random((N,M))

