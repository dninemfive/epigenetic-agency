from damage_type import DamageType, DAMAGE_TYPES, DAMAGE_TYPE_GENES
from utils import list_str
from enemy import Enemy
from genome import Genome
from gene import Gene
import random
from player import Player

class Decider(object):
    """
    Interface for the concept of selecting a weapon and targets during a turn
    """
    def choose_attack(self, player: Player, remainingEnemies: dict[str, Enemy]) -> tuple[str, DamageType]:
        raise NotImplementedError()
    
class Decider_CLI(Decider):    
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
        def __init__(self):
            self.genome = Genome({ v: Gene(v) for v in DAMAGE_TYPE_GENES.values() })

        def choose_attack(self, player: Player, remainingEnemies: dict[str, Enemy]) -> tuple[str, DamageType]:
            result_enemy = random.choice(remainingEnemies.keys())
            result_type = random.choice(player.available_ammo_types, lambda x: self.genome.genes[x.name].weight)
            return (result_enemy, result_type)