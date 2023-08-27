from damage_type import DamageType, DAMAGE_TYPES, DEFAULT_DAMAGE
from logger import log

class Action(object):
    def __init__(self, enemy, damageType: DamageType):
        self.enemy = enemy
        self.damageType = damageType

    def apply(self, player):
        result: int = 0
        if self.is_attack:            
            player.apply_action(self)
            original_enemy_hp: int = self.enemy.hp
            result = self.enemy.apply_action(self)
            log(f"Player attacks {self.enemy.name} for {self.damage} damage ({original_enemy_hp} -> {self.enemy.hp})")
        if self.is_defense:            
            original_player_hp: int = player.hp
            player.apply_action(self)
            hp_delta: int = player.hp - original_player_hp
            log(f"Player defends with {self.damageType.name}, healing {hp_delta} HP ({original_player_hp} -> {player.hp})")
        return (self, result)

    @property
    def is_attack(self):
        return self.enemy is not None
    
    @property
    def is_defense(self):
        return self.enemy is None
    
    @property
    def damage(self):
        if self.is_defense:
            return 0
        return self.damageType.damage_against(self.enemy.damage_type)
    
    def __str__(self):
        return f"Action({self.enemy}, {self.damageType})"
    
ActionResult = tuple[Action, int]

def action_result(action: Action, result: int) -> ActionResult:
    if action.is_attack:
        # weak attacks should be penalized, so subtract default damage to make them negative
        return (action, result - DEFAULT_DAMAGE)
    else:
        # heal actions could just cause negative HP gain, so leave as is
        return (action, result)
    
def possible_actions(player, enemies) -> list[Action]:
    result = []
    for enemy in enemies.values():
        for damageType in DAMAGE_TYPES.values():
            result.append(Action(enemy, damageType))
    for damageType in DAMAGE_TYPES.values():
        result.append(Action(None, damageType))
    return result