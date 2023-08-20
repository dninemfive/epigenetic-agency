from typing import Dict, Set, Union, Any

# ====================================
def ask_for_input(resources: dict[str, Any], failMsg: str) -> Any:
    key: str = None
    while key not in resources.keys():
        key = input()
        if key in resources.keys(): break
        print(failMsg, key, ". Please select one of", resources.keys())
    result: Any = resources[key]
    print("You have selected", result)
    return result

def list_str(items: enumerate) -> str:
    result: str = ""
    first: bool = True
    for item in items:
        if first: 
            result = item
        else:
            result = result + ", " + item
        first = False
    return result

# ====================================

class Weapon(object):
    def __init__(self, name: str, damage_type: str, ammo: str = None, attacks_per_turn: int = 1):
        # the name of the weapon, used to reference it in output
        self.name = name
        # damage type determines whether the weapon is strong or weak against an enemy
        self.damage_type: str = damage_type
        # if required ammo is not None, can only be used when the player has the corresponding ammo
        self.required_ammo: str = ammo
        # how many times the player can attack per turn if they choose this weapon
        self.attacks_per_turn: int = attacks_per_turn

    def has_ammo(self, ammo: dict[str, int]) -> bool:
        return self.required_ammo is None or ammo[self.required_ammo] > 0

class Enemy(object):
    def __init__(self, name: str, hp: int, weak_to: set[str] = set(), strong_against: set[str] = set(), damage_type: str = None, drops: Dict[str, int] = None):
        self.name = name
        self.hp: int = hp
        self.weak_to: set[str] = weak_to
        self.strong_against: set[str] = strong_against
        self.damage_type: str = damage_type
        self.drops: Dict[str, int] = drops

    def Instantiate(enemydef, name: str):
        return Enemy(name, enemydef.hp, enemydef.weak_to, enemydef.strong_against, enemydef.damage_type, enemydef.drops)
    
    def take_hit(self, weapon: Weapon) -> int:
        dmg: int = 2
        damageType = weapon.damage_type
        if damageType in self.weak_to:
            dmg = 3
        if damageType in self.strong_against:
            dmg = 1
        self.hp -= dmg
        return dmg

class Decider(object):
    def __init__(self):
        """
        Interface for the concept of selecting a weapon and targets during a turn
        """
    def select_weapon(weapons: list[Weapon], enemies: list[Enemy]) -> Weapon:
        raise NotImplementedError()
    def target_enemies(weapon: Weapon, enemies: dict[str, Enemy]) -> list[Enemy]:
        raise NotImplementedError()
    
class Decider_CLI(Decider):
    def select_weapon(self, weapons: dict[str, Weapon], enemies: list[Enemy]) -> Weapon:
        print("You have the following weapons:", list_str(weapons.keys()), "and the following enemies:", list_str([x.name for x in enemies]))
        return ask_for_input(weapons, "You don't have a weapon called")
    
    def target_enemies(self, weapon: Weapon, enemies: dict[str, Enemy]) -> list[Enemy]:
        print("You have", weapon.attacks_per_turn, "attacks available with", weapon.name, ", and the following potential targets:", list_str(enemies))
        availableEnemies: list[Enemy] = list(enemies.values())
        result: list[Enemy] = []
        remaining_attacks = weapon.attacks_per_turn
        while remaining_attacks > 0 and len(availableEnemies) > 0:
            print("You can attack the following enemies:", availableEnemies)
            enemy: Enemy = ask_for_input(enemies, "There isn't an enemy called")
            result.append(enemy)
            availableEnemies.remove(enemy)
        return result

class Player(object):
    # todo: genes determine these properties
    def __init__(self, decider: Decider):
        # how many hits the player can take until they die
        self.hp: int = 10
        # how many times the player can use a weaapon
        self.ammo: Dict[str, int] = {
            "9mm": 5
        }
        # the weapons available to the player
        self.weapons: dict[str, Weapon] = {
            "knife": Weapon("knife", "blade"),
            "gun": Weapon("gun", "bullet", "9mm", 2)
        }
        # the thing which decides how the player plays
        self.decider = decider

    def attack(self, enemy: Enemy, weapon: Weapon):
        if not weapon.has_ammo(self.ammo):
            return
        if weapon.required_ammo is not None:
            self.ammo[weapon.required_ammo] -= 1
        result: int = enemy.take_hit(weapon)
        print("Player deals", result, "damage to", enemy.name, "leaving them with", enemy.hp, "hp")
        # todo: update epigenome with damage taken
    
    @property
    def usable_weapons(self):
        result = dict()
        for k, v in self.weapons.items():
            if v.has_ammo(self.ammo):
                result[k] = v
        return result


def battle(player: Player, enemies: dict[str, Enemy]) -> None:
    """
    A player fights enemies until either the player is dead or all the enemies are dead.
    """
    def do_turn():
        weapon: Weapon = player.decider.select_weapon(player.usable_weapons, enemies.values())
        targets: list[Enemy] = player.decider.target_enemies(weapon, enemies)
        for target in targets:
            player.attack(target, weapon)
        # enemies each attack player once
    print(player.hp)
    for enemy in enemies.values():
        print(enemy.hp)
    while player.hp > 0 and any([x for x in enemies.values() if x.hp > 0]):
        do_turn()
    # player heals hp?

if __name__ == "__main__":
    Zombie: Enemy = Enemy("Zombie", 5, "bullet")
    player: Player = Player(Decider_CLI())
    enemies: dict[str, Enemy] = {}
    for i in range(2):
        name: str = "Zombie " + str(i + 1)
        enemies[name] = Zombie.Instantiate(name)
    battle(player, enemies)