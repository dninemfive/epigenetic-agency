from epigene import Epigene
import random
from utils import weighted_avg

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