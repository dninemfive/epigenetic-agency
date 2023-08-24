from damage_type import DamageType, DAMAGE_TYPES
from utils import list_str
from enemy import Enemy

class Decider(object):
    """
    Interface for the concept of selecting a weapon and targets during a turn
    """
    def choose_attack(self, player, remainingEnemies: dict[str, Enemy]) -> tuple[str, DamageType]:
        raise NotImplementedError()
    
class Decider_CLI(Decider):    
    def choose_attack(self, player, remainingEnemies: dict[str, Enemy]) -> tuple[str, DamageType]:
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
        while choice not in [x for x in player.ammo.keys() if player.ammo[x] > 0] and not (choice == "none"):
            print("That's not an available ammo type.")
            choice = input()
        if choice == "none": 
            return (chosenEnemy, None)
        return (chosenEnemy, DAMAGE_TYPES[choice])