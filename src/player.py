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
        self.hp: int = 100
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
            targetedEnemy: Enemy = remainingEnemies[target]
            dmg: int = targetedEnemy.take_hit(damageType)
            if targetedEnemy.hp <= 0:
                enemies.pop(target)
                remainingEnemies.pop(target)
                print("Enemy", targetedEnemy, "died!")
            self.consume_ammo(damageType)
            self.remainingMoves -= 1
            print("Player attacks", targetedEnemy, "with", damageType, "dealing", dmg, "damage!")

    def take_hit(self, damageType: DamageType) -> None:
        """
        Represents the player taking damage. Made its own method because we'll likely want to send epigenome signals
        when this occurs.
        """
        damage_taken = damage_for(damageType, DamageType("Fire", "Frost")) # todo: player damage type weights based on genetics?
        self.hp -= damage_taken
        return damage_taken
    
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
    def __init__(self):
        self.genome = Genome({ v.name: Gene(v) for v in DAMAGE_TYPE_GENES.values() })
        self.attack_counters = {}  # {"enemy_type": {"attack_type": success_count}}

    def choose_attack(self, player: Player, remainingEnemies: dict[str, Enemy]) -> tuple[str, DamageType]:
        result_enemy = random.choice([x for x in remainingEnemies.keys()])
        # random.choices returns a list apparently, so get the first item

        enemy_type = remainingEnemies[result_enemy].damage_type  # Assuming remainingEnemies is a list of Enemy objects
        self.adapt_genome(enemy_type)
    
        result_type = random.choices(player.available_ammo_types, weights=[self.genome.genes[x.name].weight for x in player.available_ammo_types])[0]
        return (result_enemy, result_type)
    
    def update_counters(self, enemy_type, attack_type, success):
        if enemy_type not in self.attack_counters:
            self.attack_counters[enemy_type] = {}
        if attack_type not in self.attack_counters[enemy_type]:
            self.attack_counters[enemy_type][attack_type] = 0
        self.attack_counters[enemy_type][attack_type] += success  # success can be 1 or 0

    def adapt_genome(self, enemy_type):
        print(f"Enemy type: {enemy_type}")
        if enemy_type in self.attack_counters:
            for attack_type, success_count in self.attack_counters[enemy_type].items():
                # Update the gene weight based on success_count
                self.genome.genes[attack_type].weight += success_count * 0.1  # learning_rate = 0.1
                print(f"Updated {attack_type} weight to {self.genome.genes[attack_type].weight}")

