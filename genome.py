import numpy as np

class Genome:
    rg =  np.random.default_rng()
    # name, min, max
    properties = np.array([
        ['nChildren', 1, 15],
        ['energyChildrenThreshold',1, 15],
        ['toEnemies', -3, 3],
        ['toFriends', -3, 3],
        ['genomeThreshold', 0, 2]
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
        return value * (high - low) + low 

    def list(self):
        out = []
        for name in self.properties[:,0]:
            out.append(self.get(name))

        return out

