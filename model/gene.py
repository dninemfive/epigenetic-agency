from epigene import Epigene

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
    def __init__(self, template: GeneTemplate):
        self.template = template
        self.epigene = Epigene