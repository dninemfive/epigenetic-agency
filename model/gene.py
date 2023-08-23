class Gene(object):
    def __init__(self, behavior: callable, weight: float = 1):
        pass

class Genome(object):
    def __init__(self, genes: set[Gene] = [], fitness: int = 0):
        self.genes: set[Gene] = genes
        self.fitness = fitness
    def cross_with(self, other):
        pass

class Epigene(object):
    def __init__(self, damageType: str, activation: float = 1):
        pass