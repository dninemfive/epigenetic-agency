from epigene import Epigene
import random

class GeneTemplate(object):
    def __init__(self, name: str):
        pass

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
    if a.name != b.name:
        raise KeyError("Cannot cross two unrelated genes!")
    return Gene(a.template, (ratio * a.weight) + ((1 - ratio) * b.weight))

def mutate(gene: Gene, chance: float = 0.05, magnitude: float = 0.1) -> Gene:
    pass