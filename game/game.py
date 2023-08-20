from typing import Dict, Set, Union

class Weapon(object):
    def __init__(self, damage_type: str, ammo: str = None, attacks_per_turn: int = 1):
        self.damage_type: str = damage_type
        self.required_ammo: str = ammo
        self.attacks_per_turn: int = attacks_per_turn

class Player(object):
    def __init__(self):
        self.hp: int = 10
        self.ammo: Dict[str, int] = Dict()

class Enemy(object):
    def __init__(self):
        self.hp:        int   = 3
        self.weak_to: set[str] = Set()
        self.strong_against: set[str] = Set()
        self.drops: Dict[str, int] = Dict()

def battle(player: Player, enemies: list[Enemy]) -> None:
    """
    A player fights enemies until either the player is dead or all the enemies are dead.
    """
    def do_turn():
        # player attacks each enemy once
        # enemies attack player once
        pass
    while player.hp > 0 and any([x for x in enemies if x.hp > 0]):
        
        pass