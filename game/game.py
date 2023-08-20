from typing import Dict, Set, Union

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

class Enemy(object):
    def __init__(self, name: str, hp: int, weak_to: set[str] = None, strong_against: set[str] = None, damage_type: str = None, drops: Dict[str, int] = None):
        self.hp: int = hp
        self.weak_to: set[str] = weak_to
        self.strong_against: set[str] = strong_against
        self.damage_type: str = damage_type
        self.drops: Dict[str, int] = drops

    def Instantiate(enemydef):
        return Enemy(enemydef.hp, enemydef.weak_to, enemydef.strong_against, enemydef.damage_type, enemydef.drops)

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
    def select_weapon(weapons: dict[str, Weapon], enemies: list[Enemy]) -> Weapon:
        print("You have the following weapons:", weapons, "and the following enemies:", enemies)
        weaponName: str = None
        while weaponName not in weapons:
            weaponName = input()
            print("You do not have a weapon called", weaponName, ". Please select one of", weapons)
        weapon: Weapon = [x for x in weapons if x.name == weaponName][0]
        print("You have selected", weapon)
        return weapon
    def target_enemies(weapon: Weapon, enemies: dict[str, Enemy]) -> list[Enemy]:
        print("You have", weapon.attacks_per_turn, "available with", weapon, ", and the following potential targets:", enemies)
        result: list[Enemy] = []
        remaining_attacks = weapon.attacks_per_turn
        while remaining_attacks > 0:
            pass

class Player(object):
    # todo: genes determine these properties
    def __init__(self, decider: Decider):
        # how many hits the player can take until they die
        self.hp: int = 10
        # how many times the player can use a weaapon
        self.ammo: Dict[str, int] = {}
        # the weapons available to the player
        self.weapons: dict[str, Weapon] = {}
        self.decider = Decider

def battle(player: Player, enemies: dict[str, Enemy]) -> None:
    """
    A player fights enemies until either the player is dead or all the enemies are dead.
    """
    def do_turn():
        # player selects weapon best for the situation and attacks n enemies
        # enemies each attack player once
        # player heals hp?
        pass
    while player.hp > 0 and any([x for x in enemies.values if x.hp > 0]):
        
        pass