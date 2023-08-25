from decider import Decider
from enemy import Enemy
from damage_type import DAMAGE_TYPES, damage_for, DamageType

class Player(object):
    # todo: genes determine these properties
    def __init__(self, decider: Decider):
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
    def available_ammo_types(self) -> enumerate[str]:
        yield None
        for item in [k for k, v in self.ammo.items() if v > 0]:
            yield item

    def __str__(self) -> str:
        return "Player(" + str(self.hp) + ")"