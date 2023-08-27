import random
from utils import weighted_avg, clamp, sigmoid, avg
from typing import Any
from logger import log
from action import Action, ActionResult, possible_actions
from damage_type import DamageType
import action_evaluators

# ================= GENE =================


class Gene(object):
    """
    The basic unit of the genetic model. Genes are used to weight decisions for a weighted random selection.
    """
    def __init__(self, name: str, _weight: float = 0.5):
        self.name = name
        self._weight = _weight

    # used so that ActionGene can override this with epigene weight
    @property
    def weight(self):
        return self._weight
    
    def __str__(self):
        return "<" + self.name + ":" + str(int(self.weight * 100)) + ">"

def cross_genes(a: Gene, b: Gene, ratio: float = 0.5) -> Gene:
    """
    Merge the values of two genes, representing crossing over in genetics.
    """
    assert a.name == b.name
    return Gene(a.template, weighted_avg(a.weight, b.weight, ratio))

def mutate_gene(gene: Gene, chance: float = 0.25, magnitude: float = 0.1) -> Gene:
    """
    Perturb the value of a gene to some degree, representing random mutations in genetics.
    """
    assert magnitude >= 0
    if random.random() < chance:
        return Gene(gene.template, clamp(gene.weight + (random.random() * magnitude) - magnitude / 2))
    return gene
    
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

    def receive_feedback(self, feedback: ActionResult, adaptability: float) -> None:
        self.expression = clamp(self.expression + sigmoid(feedback) * adaptability)

    def apply_central_bias(self, central_bias: float) -> None:
        self.expression = weighted_avg(self.expression, 0.5, central_bias)

    def __str__(self):
        return "Epigene for " + str(self.parent)
    
class ActionGene(Gene):
    def __init__(self, name: str, _weight: float, action_evaluator: callable, epigene: Epigene = None):
        super().__init__(name, _weight)
        self.epigene = epigene if epigene is not None else Epigene(self)
        self.action_evaluator = action_evaluator

    # the gene tells you how good an action will be and then the epigenome receives feedback on whether that was true
    def evaluate_action(self, player, enemies, action: Action) -> float:
        self.action_evaluator(player, enemies, action)

    @property
    def weight(self):
        return self._weight * self.epigene.expression

# =================  GENOME  =================                    
class Genome(object):
    """
    The collection of all the genes for one agent in the model. Used to access genes and to handle reproduction when an agent dies.
    """
    def __init__(self, genes: dict[str, Gene] = None, fitness: int = 0):
        self.genes: dict[str, Gene] = genes
        self.fitness = fitness

    def complete_battle(self):
        self.fitness += 1
        for gene in self.action_genes:
            gene.epigene.apply_central_bias(self.genes["Epigene Central Bias"])

    def evaluate_actions(self, player, enemies) -> Action:
        actions: list[tuple[Action, float]] = []
        for action in possible_actions(player, enemies):
            actions.append((action, self.evaluate_action(player, enemies, action)))
        return random.choices([x[0] for x in actions], [x[1] for x in actions])[0]

    def evaluate_action(self, player, enemies, action: Action) -> float:
        weight: float = 1
        relevant_ct: float = 0
        for gene in self.action_genes:
            value: float = gene.evaluate_action(player, enemies, action)
            if value != 0: relevant_ct += 0
            weight += gene.weight * gene.evaluate_action(player, enemies, action)
        relevant_ct = 1 if relevant_ct == 0 else relevant_ct
        return clamp(weight / relevant_ct, min_val=0, max_val=None)
    
    def receive_feedback(self, feedback: ActionResult) -> None:
        for gene in self.action_genes:
            gene.epigene.receive_feedback(feedback)

    @property
    def action_genes(self) -> list[ActionGene]:
        return [x for x in self.genes.values() if isinstance(x, ActionGene)]
    
    def default():
        normal_genes = [
            Gene("Epigene Adaptability"),
            Gene("Epigene Central Bias", 0.1),
            Gene("Epigene Weight"),
            Gene("Mutation Chance", 0.25),
            Gene("Mutation Magnitude", 0.1)
        ]
        action_genes = [ActionGene(x.__name__, 0.5, x) for x in action_evaluators.ALL]
        default_gene_dict: dict[str, Gene] = {}
        for gene in normal_genes:
            default_gene_dict[gene.name] = gene
        for gene in action_genes:
            default_gene_dict[gene.name] = action_genes
        return Genome(default_gene_dict)

    def __str__(self):
        result: str = "Genome(fitness=" + str(self.fitness) + ", "
        for v in self.genes.values():
            result += str(v) + ", "
        return result[:-2] + ")"

def cross(a: Genome, b: Genome) -> Genome:
    """
    Cross two genomes, merging the relevant values as well as mutating them.

    Returns a *new* Genome, does not modify either one passed in.
    """
    new_genes: dict[str, Gene] = dict()
    ratio: float = float(a.fitness) / float(a.fitness + b.fitness)
    for k, _ in a.genes.items():
        new_genes[k] = mutate_gene(cross_genes(a.genes[k], b.genes[k], ratio),\
                                    chance=weighted_avg(a.genes["Mutation Chance"],b.genes["Mutation Chance"], ratio),\
                                    magnitude=weighted_avg(a.genes["Mutation Magnitude"], b.genes["Mutation Magnitude"], ratio))
    result: Genome = Genome(new_genes)
    log(f"crossing {a} and {b}: {result}", 1)
    return result