from typing import Dict, Set, Union, Any

# ====================================
def ask_for_input(resources: dict[str, Any], failMsg: str) -> Any:
    key: str = None
    while key not in resources.keys():
        key = input()
        if key in resources.keys(): break
        print(failMsg, key, ". Please select one of", list_str(resources.keys()))
    result: Any = resources[key]
    print("You have selected", key)
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
    return "[" + result + "]"

# ====================================

DamageType = str | None
EnemyName = str
Attack = tuple[EnemyName, DamageType]

DAMAGE_TYPE_BONUSES: dict[DamageType, DamageType] = {
    "Fire": "Frost",
    "Water": "Fire",
    "Earth": "Water",
    "Wind": "Earth",
    "Lightning": "Wind",
    "Frost": "Lightning"
}

def damage_modifier_for(attackerType: DamageType, defenderType: DamageType):
    if attackerType not in DAMAGE_TYPE_BONUSES: return 0
    if DAMAGE_TYPE_BONUSES[attackerType] == defenderType: return 1
    if DAMAGE_TYPE_BONUSES[defenderType] == attackerType: return -1
    return 0 

class EnemyTemplate(object):
    def __init__(self, name: str, base_hp: int, damage_type: str = None):
        self.name = name
        self.base_hp: int = base_hp
        self.damage_type: str = damage_type
    
ENEMY_TEMPLATES: dict[str, EnemyTemplate] = {
    "Zombie": EnemyTemplate("Zombie", 3, None)
}

class Enemy(object):
    def __init__(self, template: EnemyTemplate, name: EnemyName):
        self.template = template
        self.name = name
        self.hp = template.base_hp

    def take_hit(self, type: DamageType):
        self.hp -= 1 + damage_modifier_for(type, self.damage_type)

    @property
    def damage_type(self):
        return self.template.damage_type

    def __str__(self) -> str:
        return "Enemy(template: " + self.template.name + ", name: " + self.name + ", hp: " + str(self.hp) + "/" + str(self.template.base_hp) + ")"

class Decider(object):
    """
    Interface for the concept of selecting a weapon and targets during a turn
    """
    def choose_attack(self, player, remainingEnemies: list[Enemy]) -> tuple[EnemyName, DamageType]:
        raise NotImplementedError()
    
class Decider_CLI(Decider):    
    def choose_attack(self, player, remainingEnemies: list[Enemy]) -> tuple[EnemyName, DamageType]:
        print("You have", player.remainingMoves, "remaining moves. Which enemy would you like to attack?", list_str(remainingEnemies))
        choice: str = input()
        while choice not in remainingEnemies:
            print("That's not an available target.")
            choice = input()
        chosenEnemy: EnemyName = choice
        remainingEnemies.remove(choice)
        print("You have the following ammo available:")
        for k, v in player.ammo:
            print("\n",k,":",v)
        print('You can also say "none" to attack without a damage type.')
        choice: str = input()
        while choice not in [x for x in player.ammo.keys() if player.ammo[x] > 0]:
            print("That's not an available ammo type.")
            choice = input()
        chosenDamageType: DamageType = choice
        return (chosenEnemy, chosenDamageType)

class Player(object):
    # todo: genes determine these properties
    def __init__(self, decider: Decider):
        # how many hits the player can take until they die
        self.hp: int = 10
        # how many times the player can use a damage type
        self.ammo: dict[DamageType, int] = dict()
        for k, _ in DAMAGE_TYPE_BONUSES:
            self.ammo[k] = 5
        # the thing which decides how the player plays
        self.decider = decider

    def do_attacks(self, enemies: dict[EnemyName, Enemy]) -> None:
        remainingEnemies: list[EnemyName] = [x.name for x in enemies.values() if x.hp > 0]
        self.remainingMoves: int = 3
        while self.remainingMoves > 0 and any(remainingEnemies):
            target, damageType = self.decider.choose_attack(self, remainingEnemies)
            enemies[target].take_hit(damageType)
            self.ammo[damageType] -= 1

    def take_hit(self, damageType: DamageType) -> None:
        self.hp -= damage_modifier_for(damageType, "Fire") # todo: player damage type weights based on genetics?

    def __str__(self) -> str:
        return "Player(hp: " + self.hp + ")"

def battle(player: Player, enemies: dict[str, Enemy]) -> None:
    """
    A player fights enemies until either the player is dead or all the enemies are dead.
    """
    def do_turn():
        player.do_attacks(enemies)
        for enemy in [x for x in enemies.values() if x.hp > 0]:
            player.take_hit(enemy.damage_type)

    print(player.hp)
    for enemy in enemies.values():
        print(enemy.hp)
    while player.hp > 0 and any([x for x in enemies.values() if x.hp > 0]):
        do_turn()
    # player heals hp?

if __name__ == "__main__":
    player: Player = Player(Decider_CLI())
    enemies: dict[EnemyName, Enemy] = {}
    for i in range(2):
        name: str = "Zombie " + str(i + 1)
        enemies[name] = Enemy(ENEMY_TEMPLATES["Zombie"], name)
    battle(player, enemies)