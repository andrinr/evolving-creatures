from operator import attrgetter
import numpy as np
from scipy.stats import norm
import math

class Genome:
    rg =  np.random.default_rng()
    # name, min, max
    properties = np.array([
        ['nChildren', 1, 15],
        ['energyChildrenThreshold',1, 15],
        ['toEnemies', -3, 3],
        ['toFriends', -3, 3],
    ])

    def __init__(self, genes = None):
        self.genes = genes if np.any(genes) else\
            self.rg.uniform(size=len(self.properties))

    def get(self, name):
        index = np.where(self.properties[:,0] == name)[0][0]
        value = self.genes[index]
        low = float(self.properties[index,1])
        high = float(self.properties[index,2])
        return self.range(value, low, high)

    def mutate(self, strength):
        mutated = self.genes + Genome.rg.uniform(low=-strength/2, high=strength/2, size=len(self.genes))
        return Genome(mutated)

    def difference(self, other):
        return np.linalg.norm(self.genes-other.genes)

    @ staticmethod
    def range(value, low, high):
        # Logistic equation to limit in fixed range
        return value * (high - low) + low 
        l = high - low
        x_0 = 0.5
        k = 10.
        return low + l / ( 1.0 + math.exp(-k*(value-x_0)))

    def replicate(self, rate):
        childGenes = self.genes + 2 * rate *  self.rg.random(len(self.attributes)) - rate
        return Genome(self.express(childGenes))


    @ staticmethod
    def express(x):
        return norm.cdf(x, loc=0, scale=0.2)
        # L = max - min
        # x_0 = (max + min) / 2
        # return L / ( 1 + math.exp(1*(value-x_0)))