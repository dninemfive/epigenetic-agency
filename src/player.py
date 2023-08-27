from enemy import Enemy
from gene import Gene, Genome
from damage_type import DAMAGE_TYPES, DAMAGE_TYPE_GENES, damage_for, DamageType
from utils import list_str
from logger import log
import random
from action import Action, ActionResult

DEFAULT_AMMO: int = 10
PLAYER_HP: int = 25
HEAL_AMOUNT: int = 5
PLAYER_MOVES: int = 3

class Player(object):
    """
    This class represents the agent playing the game. It tracks the ammo and HP the agent has, and uses a
    Decider to make decisions in-game.
    """
    def __init__(self, decider):
        # how many hits the player can take until they die
        self.hp: int = PLAYER_HP
        # how many times the player can use a damage type
        self.ammo: dict[str, int] = dict()
        for k, _ in DAMAGE_TYPES.items():
            self.ammo[k] = DEFAULT_AMMO
        self.ammo["None"] = "∞"
        # the thing which decides how the player plays
        self.decider = decider
        self.current_type = DAMAGE_TYPES["None"]
        self.remainingMoves = PLAYER_MOVES

    def next_action(self, enemies) -> Action:
        return self.decider.choose_action(self, enemies)

    def apply_action(self, action: Action) -> None:
        if action.is_attack:
            self.current_type = DAMAGE_TYPES["None"]
            self.consume_ammo(action.damageType.name)
            # enemy damage handled separately
        if action.is_defense:
            self.current_type = action.damageType
            self.hp += HEAL_AMOUNT

    def reset_moves(self):
        self.remainingMoves = PLAYER_MOVES

    def take_hit(self, damageType: DamageType) -> int:
        """
        Represents the player taking damage. Made its own method because we'll likely want to send epigenome signals
        when this occurs.
        """
        self.hp -= damage_for(damageType, self.current_type) # todo: player damage type weights based on genetics?
        return damage_for(damageType, self.current_type)

    def consume_ammo(self, damageType: str) -> None:
        """
        Decrements the amount of ammo the player has for a specified damage type. Made its own method because we'll
        likely want to send epigenome signals when this occurs.
        """
        if not self.has_ammo(damageType):
            return
        self.ammo[damageType] -= 1

    @property
    def available_ammo(self) -> list[str]:
        return [k for k, v in self.ammo.items() if k == "None" or v > 0]
    @property
    def available_ammo_types(self) -> list[DamageType]:
        """
        What ammo types are available for the player to use. "None" is always an option.
        """
        return [DAMAGE_TYPES[x] for x in self.available_ammo]
    
    def has_ammo(self, type: str) -> bool:
        return type in self.available_ammo
    
    @property
    def hp_percentage(self):
        return self.hp / float(PLAYER_HP)
    
    def __str__(self) -> str:
        """
        Represents the player when printing the game state.
        """
        return "Player(" + str(self.hp) + ")"
    
#

class Decider(object):
    """
    Interface for the concept of selecting a an action. This base class does nothing, it is simply a template to override.
    """
    def choose_action(self, player: Player, remainingEnemies: dict[str, Enemy]) -> Action:
        """
        Given the game state, i.e. the player and enemies, return what attack to use.
        """
        raise NotImplementedError()
    
    def receive_feedback(self, feedback: ActionResult) -> None:
        pass
    
class Decider_CLI(Decider):
    """
    A Decider which asks the human user what to do each turn. Mainly for debugging the game.
    """
    def choose_action(self, player: Player, remainingEnemies: dict[str, Enemy]) -> Action:
        print(f"You have {player.remainingMoves} remaining moves. What would you like to do?")
        print(f"You can attack one of {list_str(remainingEnemies.values())} or you can defend.")
        print(f"Either way, you must provide a damage type out of {list_str(player.available_ammo_types)}.")
        choice: str = input()
        split: list[str] = choice.split()
        while True:
            if len(split) > 1 and split[0] == "defend" and split[1] in DAMAGE_TYPES:
                return Action(None, DAMAGE_TYPES[split[1]])
            if len(split) > 2 and split[0] == "attack"\
                              and split[1] in remainingEnemies\
                              and player.has_ammo(split[2]):
                return Action(remainingEnemies[split[1]], DAMAGE_TYPES[split[2]])
            print("That's not a valid command.")
            choice = input()
    
class Decider_Genome(Decider):
    """
    A Decider which uses the genome to make decisions about what to do.
    """
    def __init__(self, genome: Genome = None):
        if genome is not None:
            self.genome = genome
        else:
            self.genome = Genome({ v.name: Gene(v) for v in DAMAGE_TYPE_GENES.values() })

    def choose_action(self, player: Player, remainingEnemies: dict[str, Enemy]) -> Action:
        return self.genome.evaluate_actions(player, remainingEnemies)
    
    def receive_feedback(self, feedback: ActionResult) -> None:
        self.genome.receive_feedback(feedback)
    
    def __str__(self):
        return f"Decider_Genome({self.genome})"