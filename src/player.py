from enemy import Enemy
from gene import Gene, Genome
from damage_type import DAMAGE_TYPES, DAMAGE_TYPE_GENES, damage_for, DamageType
import random

class Player(object):
    def __init__(self, decider):
        # how many hits the player can take until they die
        self.hp: int = 10
        # how many times the player can use a damage type
        self.ammo: dict[DamageType, int] = dict()
        for k, _ in DAMAGE_TYPES.items():
            self.ammo[k] = 5
        # the thing which decides how the player plays
        self.decider = decider

    def do_attacks(self, enemies: dict[str, Enemy]) -> None:
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
            print("Player attacks", target, "with", damageType, "dealing", dmg, "damage!")

    def take_hit(self, damageType: DamageType) -> None:
        self.hp -= damage_for(damageType, "Fire") # todo: player damage type weights based on genetics?

    def consume_ammo(self, damageType: DamageType) -> None:
        if damageType not in self.ammo:
            return
        self.ammo[damageType] -= 1

    @property
    def available_ammo_types(self):
        result = [None]
        result.extend([k for k, v in self.ammo.items() if v > 0])
        return result
    
    def __str__(self) -> str:
        return "Player(" + str(self.hp) + ")"
    

#

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
        result_enemy = random.choice([x for x in remainingEnemies.keys()])
        result_type = random.choices(player.available_ammo_types, weights=[self.genome.genes[x.name].weight for x in player.available_ammo_types])
        return (result_enemy, result_type)