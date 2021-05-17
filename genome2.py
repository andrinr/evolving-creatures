from operator import attrgetter
import numpy as np
import math

class Genome:
    rg =  np.random.default_rng()
    nGenes = 5

    attributes = {
        'size' :            {'min' : 0,     'max' : 1,      'gen' : 0},
        'costsEnemyPF' :    {'min' : -1,    'max' : 1,      'gen' : 1},
        'blurEnemyPF' :     {'min' : 0,     'max' : 3,      'gen' : 2},
        'costsFriendlyPF' : {'min' : -1,    'max' : 1,      'gen' : 3},
        'blurFriendlyPF' :  {'min' : 0,     'max' : 3,      'gen' : 4},
        'breedThreeshold' : {'min' : 0,     'max' : 10,     'gen' : 5},
        'breedMax' :        {'min' : 1,     'max' : 9,      'gen' : 6},
    }

    def __init__(self, genes = None):
        self.genes = genes if genes else self.rg.random(len(self.attributes))

    def getAttrValue(self, name):
        attr = self.attributes[name]
        return self.express(self.genes[attr.gen], attr['min'], attr['max'])

    @staticmethod
    def mutate(genes, strength):
        mutated = genes + Genome.rg.uniform(low=-strength/2, high=strength, size=Genome.nGenes)

        return mutated

    @staticmethod
    def express(value, min, max):
        L = max - max
        x_0 = (max + min) / 2
        return L / ( 1 + math.exp(1*(value-x_0)))
