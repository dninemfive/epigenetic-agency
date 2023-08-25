import random
from utils import weighted_avg

# ================= GENE =================

class GeneTemplate(object):
    def __init__(self, name: str):
        self.name = name

    # https://stackoverflow.com/a/3076987
    # implementing these so the type can be used as a dictionary key
    def __eq__(self, other) -> bool:
        return isinstance(other, GeneTemplate) and self.name == other.name
    
    def __hash__(self):
        return hash(self.name)

GENE_TEMPLATES = [
    # epigenome weight:         amount the epigenome factors into decisions using genes
    # epigenome adaptability:   how strongly the epigenome reacts to signals
    # epigenome central bias:   how strongly the epigenome returns to expression = 0.5
    # gene for how much the player likes to attack
    # gene for how much the player likes to heal
    # gene which changes the weights of attacking/healing based on number of battles fought??
    # ? gene for how much the player likes to scavenge ? (if loot is implemented)
    # gene(s) for targeting enemies based on hp and damagetype
]

class Gene(object):
    def __init__(self, template: GeneTemplate, weight: float = 0.5):
        self.template = template
        self.epigene = Epigene(self)    
        self.weight = weight

    @property
    def name(self):
        return self.template.name

def cross(a: Gene, b: Gene, ratio: float = 0.5) -> Gene:
    assert a.name == b.name
    return Gene(a.template, weighted_avg(a.weight, b.weight, ratio))

def mutate(gene: Gene, chance: float = 0.05, magnitude: float = 0.1) -> Gene:
    assert magnitude >= 0
    if random.random() < chance:
        return Gene(gene.template, gene.weight + (random.random() * magnitude) - magnitude / 2)
    
# =================  EPIGENE =================

class Epigene(object):
    def __init__(self, parent: Gene, expression: float = 0.5):
        # the gene this epigene affects
        self.parent: Gene = parent
        # to what degree the epigene affects the parent gene.
        # plug into a sigmoid curve, probably
        self.expression: float = expression

    def receive_signal(self, delta: float = 0.5):
        pass

    def __str__(self):
        return "Epigene for " + str(self.parent)

# =================  GENOME  =================                    
class Genome(object):
    def __init__(self, genes: dict[GeneTemplate, Gene] = [], fitness: int = 0):
        self.genes: dict[GeneTemplate, Gene] = genes
        self.fitness = fitness
        self.previous_state = None

    def complete_battle(self):
        self.fitness += 1    

    def update_epigene(self, template: GeneTemplate):
        pass

def cross_genome(a: Genome, b: Genome) -> Genome:
    new_genes: dict[GeneTemplate, Gene] = set()
    ratio: float = float(a.fitness) / float(a.fitness + b.fitness)
    for k, _ in a.genes:
        new_genes[k] = mutate(cross(a.genes[k], b.genes[k], ratio))
    return Genome(new_genes)