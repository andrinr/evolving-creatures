from operator import attrgetter
import numpy as np
from scipy.stats import norm
import math

class Genome:
    rg =  np.random.default_rng()

    # {name: (min, max)}
    bounds = {'speed':(1, 6),
              'nKids': (0, 20),
              'energyChildrenThreshold': (0, 20),
              'toEnemies': (-3, 3),
              'toFriends': (-3, 3),
              'genomeThreshold': (0, 2),
              'pfSize': (4, 10)
              }


    def __init__(self, genes=None, idx=None, names=None):
        if np.any(genes):
            self.genes = genes 
            self.idx = idx
        else:
            self.names = ['energyChildrenThreshold', 'nKids']
            self.names += names
            self.idx = {gene: i for i, gene in enumerate(self.names)}
            self.genes = self.randomGenes()


    def randomGenes(self):
        randFact = self.rg.random(len(self.names))
        bounds = np.array([self.bounds[gene] for gene in self.names])
        return bounds[:,0] + randFact * (bounds[:,1] - bounds[:,0])


    def get(self, name):
        return self.genes[self.idx[name]]


    def replicate(self, drift):
        bounds = np.array([self.bounds[gene] for gene in self.idx.keys()])

        # adapt drift to the different gene-boundaries
        drift *= (bounds[:,1] - bounds[:,0])

        mutated = self.genes + np.array([self.rg.uniform(low=-drift[i]/2, high=drift[i]/2) for i in range(len(bounds))])

        # ensure that the values are inside the boundaries
        for gene in self.idx.keys():
            lower, upper = bounds[self.idx[gene]]
            if lower > mutated[self.idx[gene]]:
                mutated[self.idx[gene]] = lower
            elif upper < mutated[self.idx[gene]]:
                mutated[self.idx[gene]] = upper

        return Genome(genes=mutated, idx=self.idx)


    def difference(self, other):
        return np.linalg.norm(self.genes-other.genes)

    def genLog(self):
        return self.genes.tolist()