import random
from utils import weighted_avg
from typing import Any

# ================= GENE =================

class GeneTemplate(object):
    """
    A template for each gene. Basically unused right now, but might be useful if we want to give them default weights or something.
    """
    def __init__(self, name: str, epigeneSignalHandler: callable):
        self.name = name
        # more precisely, callable(Any, float) -> float
        self.epigeneSignalHandler = epigeneSignalHandler

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
    GeneTemplate("Epigenome Weight", None),
    # epigenome adaptability:   how strongly the epigenome reacts to signals
    GeneTemplate("Epigenome Adaptability", None),
    # epigenome central bias:   how strongly the epigenome returns to expression = 0.5
    GeneTemplate("Epigenome Central Bias", None),
    # gene for how much the player likes to attack
    # signal: float = amount of damage done by an attack
    GeneTemplate("Attack Bias", lambda f: (f - 2) / 100),
    # gene for how much the player likes to heal
    # gene which changes the weights of attacking/healing based on hp??
    # ? gene for how much the player likes to scavenge ? (if loot is implemented)
    # gene(s) for targeting enemies based on hp and damagetype
    GeneTemplate("Target Weak Enemies", None)
    # prioritize enemies which do more damage to us
]

class Gene(object):
    """
    The basic unit of the genetic model. Genes are used to weight decisions for a weighted random selection.
    """
    def __init__(self, template: GeneTemplate, weight: float = 0.5):
        self.template = template
        self.epigene = Epigene(self, template.epigeneSignalHandler)    
        self.weight = weight

    @property
    def name(self):
        return self.template.name
    
    def __str__(self):
        return "<" + self.name + ":" + str(int(self.weight * 100)) + ">"

def cross(a: Gene, b: Gene, ratio: float = 0.5) -> Gene:
    """
    Merge the values of two genes, representing crossing over in genetics.
    """
    assert a.name == b.name
    return Gene(a.template, weighted_avg(a.weight, b.weight, ratio))

def mutate(gene: Gene, chance: float = 0.25, magnitude: float = 0.1) -> Gene:
    """
    Perturb the value of a gene to some degree, representing random mutations in genetics.
    """
    assert magnitude >= 0
    if random.random() < chance:
        modified_val: float = gene.weight + (random.random() * magnitude) - magnitude / 2
        if modified_val <= 0: modified_val = 0.000001
        if modified_val > 1: modified_val = 1
        return Gene(gene.template, modified_val)
    return gene
    
# =================  EPIGENE =================

class Epigene(object):
    """
    One Epigene is attached to each Gene, and it modifies how much that gene is expressed based on feedback after each event,
    such as the amount of damage dealt by or to the player.
    """
    def __init__(self, parent: Gene, signalHandler: callable = None, expression: float = 0.5):
        # the gene this epigene affects
        self.parent: Gene = parent
        self.signalHandler = signalHandler
        # to what degree the epigene affects the parent gene.
        # plug into a sigmoid curve, probably
        self.expression: float = expression

    def receive_signal(self, signal: Any, delta: float = 0.5) -> None:
        if self.signalHandler is None: return
        expression += self.signalHandler(signal, delta)

    def __str__(self):
        return "Epigene for " + str(self.parent)

# =================  GENOME  =================                    
class Genome(object):
    """
    The collection of all the genes for one agent in the model. Used to access genes and to handle reproduction when an agent dies.
    """
    def __init__(self, genes: dict[str, Gene] = {}, fitness: int = 0):
        self.genes: dict[str, Gene] = genes
        self.fitness = fitness

    def complete_battle(self):
        self.fitness += 1    

    def update_epigene(self, template: GeneTemplate):
        pass

    def __str__(self):
        result: str = "Genome(fitness=" + str(self.fitness) + ", "
        for v in self.genes.values():
            result += str(v) + ", "
        return result[:-2] + ")"

def cross_genome(a: Genome, b: Genome) -> Genome:
    """
    Cross two genomes, merging the relevant values as well as mutating them.

    Returns a *new* Genome, does not modify either one passed in.
    """
    print("Crossing",a,"and",b,":")
    new_genes: dict[str, Gene] = dict()
    ratio: float = float(a.fitness) / float(a.fitness + b.fitness)
    for k, _ in a.genes.items():
        new_genes[k] = mutate(cross(a.genes[k], b.genes[k], ratio))
    result: Genome = Genome(new_genes)
    print("\t",result)
    return result