import random
from utils import weighted_avg

# ================= GENE =================

class GeneTemplate(object):
    """
    A template for each gene. Basically unused right now, but might be useful if we want to give them default weights or something.
    """
    def __init__(self, name: str):
        self.name = name

    # https://stackoverflow.com/a/3076987
    # implementing these so the type can be used as a dictionary key
    def __eq__(self, other) -> bool:
        return isinstance(other, GeneTemplate) and self.name == other.name
    
    def __hash__(self):
        return hash(self.name)
    
    def __str__(self):
        return "Epigenome(" + self.name + ")"

GENE_TEMPLATES = [ 
    # epigenome weight:         amount the epigenome factors into decisions using genes
    # epigenome adaptability:   how strongly the epigenome reacts to signals
    # epigenome central bias:   how strongly the epigenome returns to expression = 0.5
    # gene for how much the player likes to attack
    # gene for how much the player likes to heal
    # gene which changes the weights of attacking/healing based on number of battles fought??
    # ? gene for how much the player likes to scavenge ? (if loot is implemented)
    # gene(s) for targeting enemies based on hp and damagetype
    # prioritize enemies which do more damage to us
]

class Gene(object):
    """
    The basic unit of the genetic model. Genes are used to weight decisions for a weighted random selection.
    """
    def __init__(self, template: GeneTemplate, weight: float = 0.5):
        self.template = template
        self.epigene = Epigene(self)    
        self.weight = weight

    @property
    def name(self):
        return self.template.name
    
    def __str__(self):
        return "Genome(" + self.name + ", " + str(self.weight) + ")"

def cross(a: Gene, b: Gene, ratio: float = 0.5) -> Gene:
    """
    Merge the values of two genes, representing crossing over in genetics.
    """
    assert a.name == b.name
    return Gene(a.template, weighted_avg(a.weight, b.weight, ratio))

def mutate(gene: Gene, chance: float = 0.05, magnitude: float = 0.1) -> Gene:
    """
    Perturb the value of a gene to some degree, representing random mutations in genetics.
    """
    assert magnitude >= 0
    if random.random() < chance:
        return Gene(gene.template, gene.weight + (random.random() * magnitude) - magnitude / 2)
    
# =================  EPIGENE =================

class Epigene(object):
    """
    One Epigene is attached to each Gene, and it modifies how much that gene is expressed based on feedback after each event,
    such as the amount of damage dealt by or to the player.
    """
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
    """
    The collection of all the genes for one agent in the model. Used to access genes and to handle reproduction when an agent dies.
    """
    def __init__(self, genes: dict[str, Gene] = [], fitness: int = 0):
        self.genes: dict[str, Gene] = genes
        self.fitness = fitness
        self.previous_state = None

    def complete_battle(self):
        self.fitness += 1    

    def update_epigene(self, template: GeneTemplate):
        pass

def cross_genome(a: Genome, b: Genome) -> Genome:
    """
    Cross two genomes, merging the relevant values as well as mutating them.

    Returns a *new* Genome, does not modify either one passed in.
    """
    new_genes: dict[str, Gene] = set()
    ratio: float = float(a.fitness) / float(a.fitness + b.fitness)
    for k, _ in a.genes:
        new_genes[k] = mutate(cross(a.genes[k], b.genes[k], ratio))
    return Genome(new_genes)
