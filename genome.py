import numpy as np
from random import choice


class Allele:

    def __init__(self, dominance, val, description):
        self.__dominant = dominance # bool
        self.__value = val
        self.__description = description

    def __str__(self):
        return self.__description

    @ property
    def description(self):
        return self.__description

    @ property
    def dominant(self):
        return self.__dominant

    @ property
    def value(self):
        return self.__value


class Gene:

    def __init__(self, alleleM, alleleF, name):
        self.__alleleF = alleleF
        self.__alleleM = alleleM
        self.__value = 0
        self.__phenotype = ''
        self.__name = name
        self.__getPhen()
    
    def __str__(self):
        return 'Gene Nr.:{}\nPhenotype: {}\n alleleM: {}\n alleleF: {}'.format(self.name, 
                                                                               self.__phenotype, 
                                                                               self.__alleleM,
                                                                               self.__alleleF)

    def __getPhen(self):
        if self.__alleleF.dominant == self.__alleleM.dominant:
            self.__value = .5 * (self.__alleleF.value + self.__alleleM.value)  # or better max, min??
            self.__phenotype = self.__alleleM.description

        elif self.__alleleF.dominant:
            self.__value = self.__alleleF.value
            self.__phenotype = self.__alleleF.description

        else:
            self.__value = self.__alleleM.value
            self.__phenotype = self.__alleleM.description

    @ property
    def alleleF(self):
        return self.__alleleF

    @ property
    def alleleM(self):
        return self.__alleleM

    @ property
    def name(self):
        return self.__name

    @ property
    def phenotype(self):
        return self.__phenotype

    @ property
    def value(self):
        return self.__value


class Genome:

    # {name of Gene1: ((phenotype1, dominance), (phenotype2, dominance)), ...}
    phenotypes = {'gene1':[['predator', False], ['prey',True]],
                  'gene2':[['sizeM', True],['sizeL', False]],
                  'gene3':[['pFSizeM', False], ['pfSizeL', True]], 
                  'gene4':[['aggressive', False], ['peaceful', True]]}

    def __init__(self, genes=None, replication=False):
        # if we build a genome because of a replication we get the genes from the 
        # fertilisation otherwise we need am empty list.
        self.__genes = genes or []
        if not replication:
            self.randomGenes()
        self.__n = len(self.__genes)

    def randomGenes(self):
        for name, types in self.phenotypes.items():
            alleles = []
            for _ in (1,2):
                phene = choice(types)
                # dominant alleles receive a positive random value in [0,1]
                if phene[1]:
                    alleles.append(Allele(phene[1], np.random.random(), phene[0]))
                # rezessive alleles treceive a negative random value
                else:
                    alleles.append(Allele(phene[1], -np.random.random(), phene[0]))
            self.__genes.append(Gene(alleles[0], alleles[1], name))

    @ property
    def genes(self):
        keys = ['predator', 'size', 'pfSize', 'aggression']
        return dict(zip(keys, self.__genes))

    @ property
    def n(self):
        return self.__n

# =============================================================================
# Replicfation
# =============================================================================

class CellDivision:

    def __init__(self, genome):
        self.__genome = genome
        self.__father = np.array([gene.alleleF for gene in genome.genes])
        self.__mother = np.array([gene.alleleM for gene in genome.genes])
        self.__chromatids = self.__meiosis()

    @ property
    def chromatids(self):
        return self.__chromatids

    def __meiosis(self):
        # generate 4 haploid 1-chromatid chhromosomes

        chromatid11, chromatid12 = self.__father, self.__father
        chromatid21, chromatid22 = self.__mother, self.__mother
        return self.__crossingOver(chromatid11, chromatid12, chromatid21, chromatid22)

    def __crossingOver(self, chr11, chr12, chr21, chr22):
        # recombination of genetic information => genetic diversity

        low1, up1 = np.sort(np.random.randint(self.__genome.n, size=2))
        low2, up2 = np.sort(np.random.randint(self.__genome.n, size=2))

        chr11[low1:up1], chr21[low1:up1] = chr21[low1:up1], chr11[low1:up1].copy()
        chr12[low2:up2], chr22[low2:up2] = chr22[low2:up2], chr12[low2:up2].copy()

        return chr11, chr12, chr21, chr22

    def __mutation(self):
        pass


class Fertilisation:

    def __init__(self, chromatidsF, chromatidsM):
        self.__chromatidF = np.random.choice(chromatidsF)
        self.__chromatidM = np.random.choice(chromatidsM)
        self.__genome = Genome([Gene(aF, aM) for aF, aM in zip(self.__chromatidF, self.chromatidM)])

    @ property
    def genome(self):
        return self.__genome