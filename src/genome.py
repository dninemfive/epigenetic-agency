from gene import Gene, GeneTemplate, cross, mutate

class Genome(object):
    def __init__(self, genes: dict[GeneTemplate, Gene] = [], fitness: int = 0):
        self.genes: dict[GeneTemplate, Gene] = genes
        self.fitness = fitness
        self.previous_state = None

    def complete_battle(self):
        self.fitness += 1    

    def update_epigene(self, template: GeneTemplate):
        pass

def cross(a: Genome, b: Genome) -> Genome:
    new_genes: dict[GeneTemplate, Gene] = set()
    ratio: float = float(a.fitness) / float(a.fitness + b.fitness)
    for k, _ in a.genes:
        new_genes[k] = mutate(cross(a.genes[k], b.genes[k], ratio))
    return Genome(new_genes)