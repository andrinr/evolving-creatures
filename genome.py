import numpy as np


class Allele:

    def __init__(self, dominance, val):
        self.__dominant = dominance # bool
        self.__value = val

    @ property
    def dominant(self):
        return self.__dominant

    @ property
    def value(self):
        return self.__value


class Gene:
    
    def __init__(self, alleleF, alleleM):
        self.__alleleF = alleleF
        self.__alleleM = alleleM
        self.__value = 0
        self.__getPhen()

    @ property
    def alleleF(self):
        return self.__alleleF

    @ property
    def alleleM(self):
        return self.__alleleM

    @ property
    def value(self):
        return self.__value

    def __getPhen(self):
        if self.__alleleF.dominant == self.__alleleM.dominant:
            self.__value = .5 * (self.__alleleF.value + self.__alleleM.value)  # or better max, min??
        elif self.__alleleF.dominant:
            self.__value = self.__alleleF.value
        else:
            self.__value = self.__alleleM.value


class Genome:

    def __init__(self, genes):
        self.__genes = genes
        self.__n = len(genes)

    @ property
    def genes(self):
        return self.__genes

    @ property
    def n(self):
        return self.__n


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