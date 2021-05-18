from operator import attrgetter
import numpy as np
from scipy.stats import norm

# Rationale:
# Another creature is considered an enemy if:
# - its aggression suprpasses my aggression Threeshold
# 
class Genome:
    rg =  np.random.default_rng()
    names = [
        'size',
        'aggression',
        'aggressionThreeshold',
        'enemyCosts',
        'enemyBlur',
        'friendlyCosts',
        'friendlyBlur',
        'breedThreeshold',
        'energyChildrenRatio'
    ]

    def __init__(self, genes = None):
        self.genes = genes if np.any(genes) else\
            self.rg.uniform(size=len(self.names))

    def get(self, name):
        index = self.names.index(name, 0, len(self.names))
        return self.genes[index]

    def mutate(self, strength):
        mutated = self.genes + Genome.rg.uniform(low=-strength/2, high=strength, size=len(self.genes))
        return Genome(mutated)

    # @ staticmethod
    # def express(value, min, max):
    #     L = max - max
    #     x_0 = (max + min) / 2
    #     return L / ( 1 + math.exp(1*(value-x_0)))

    def replicate(self, rate):
        childGenes = self.genes + 2 * rate *  self.rg.random(len(self.attributes)) - rate
        return Genome(self.express(childGenes))


    @ staticmethod
    def express(x):
        return norm.cdf(x, loc=0, scale=0.2)
        # L = max - min
        # x_0 = (max + min) / 2
        # return L / ( 1 + math.exp(1*(value-x_0)))