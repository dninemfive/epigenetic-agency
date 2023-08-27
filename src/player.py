from enemy import Enemy
from gene import Gene, Genome
from damage_type import DAMAGE_TYPES, DAMAGE_TYPE_GENES, damage_for, DamageType
from utils import list_str
import random

class Player(object):
    """
    This class represents the agent playing the game. It tracks the ammo and HP the agent has, and uses a
    Decider to make decisions in-game.
    """
    def __init__(self, decider):
        # how many hits the player can take until they die
        self.hp: int = 10
        # how many times the player can use a damage type
        self.ammo: dict[str, int] = dict()
        for k, _ in DAMAGE_TYPES.items():
            self.ammo[k] = 5
        self.ammo["None"] = "∞"
        # the thing which decides how the player plays
        self.decider = decider

    def do_attacks(self, enemies: dict[str, Enemy]) -> None:
        """
        Handles all the actions the agent does on their turn.
        """
        remainingEnemies: dict[str, Enemy] = enemies.copy()
        self.remainingMoves: int = 3
        while self.remainingMoves > 0 and any(remainingEnemies):
            target, damageType = self.decider.choose_attack(self, remainingEnemies)
            dmg: int = enemies[target].take_hit(damageType)
            if enemies[target].hp <= 0:
                enemies.pop(target)
                remainingEnemies.pop(target)
            self.consume_ammo(damageType)
            self.remainingMoves -= 1
            print("\t\tPlayer attacks", target, "with", damageType, "dealing", dmg, "damage!")

    def take_hit(self, damageType: DamageType) -> int:
        """
        Represents the player taking damage. Made its own method because we'll likely want to send epigenome signals
        when this occurs.
        """
        self.hp -= damage_for(damageType, "Fire") # todo: player damage type weights based on genetics?
        return damage_for(damageType, "Fire")

    def consume_ammo(self, damageType: DamageType) -> None:
        """
        Decrements the amount of ammo the player has for a specified damage type. Made its own method because we'll
        likely want to send epigenome signals when this occurs.
        """
        if damageType not in self.ammo or damageType.name == "None":
            return
        self.ammo[damageType] -= 1

    @property
    def available_ammo_types(self):
        """
        What ammo types are available for the player to use. "None" is always an option.
        """
        return [DAMAGE_TYPES[k] for k, v in self.ammo.items() if k == "None" or v > 0]
    
    def __str__(self) -> str:
        """
        Represents the player when printing the game state.
        """
        return "Player(" + str(self.hp) + ")"
    
#

class Decider(object):
    """
    Interface for the concept of selecting a weapon and targets during a turn. This base class does nothing, it is simply a template to override.
    """
    def choose_attack(self, player: Player, remainingEnemies: dict[str, Enemy]) -> tuple[str, DamageType]:
        """
        Given the game state, i.e. the player and enemies, return what attack to use.
        """
        raise NotImplementedError()
    
class Decider_CLI(Decider):
    """
    A Decider which asks the human user what to do each turn. Mainly for debugging the game.
    """
    def choose_attack(self, player: Player, remainingEnemies: dict[str, Enemy]) -> tuple[str, DamageType]:
        print("You have", player.remainingMoves, "remaining moves. Which enemy would you like to attack?", list_str(remainingEnemies.values()))
        choice: str = input()
        while choice not in remainingEnemies:
            print("That's not an available target.")
            choice = input()
        chosenEnemy: str = choice
        print("You have the following ammo available:")
        for k, v in player.ammo.items():
            print(" ",k,":",v)
        print('You can also say "none" to attack without a damage type.')
        choice: str = input()
        while choice not in player.available_ammo_types and not (choice == "none"):
            print("That's not an available ammo type.")
            choice = input()
        if choice == "none": 
            return (chosenEnemy, None)
        return (chosenEnemy, DAMAGE_TYPES[choice])
    
class Decider_Genome(Decider):
    """
    A Decider which uses the genome to make decisions about what to do.
    """
    def __init__(self, genome: Genome = None):
        if genome is not None:
            self.genome = genome
        else:
            self.genome = Genome({ v.name: Gene(v) for v in DAMAGE_TYPE_GENES.values() })

    def choose_attack(self, player: Player, remainingEnemies: dict[str, Enemy]) -> tuple[str, DamageType]:
        result_enemy = random.choice([x for x in remainingEnemies.keys()])
        # random.choices returns a list apparently, so get the first item
        # print(list_str(player.available_ammo_types, print_type=True))
        result_type = random.choices(player.available_ammo_types, weights=[self.genome.genes[x.name].weight for x in player.available_ammo_types])[0]
        return (result_enemy, result_type)
    
    def __str__(self):
        return "Decider_Genome(" + str(self.genome) + ")"