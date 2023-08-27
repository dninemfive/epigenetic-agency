from damage_type import DamageType, DEFAULT_DAMAGE
from enemy import Enemy

class Action(object):
    def __init__(self, enemy: Enemy, damageType: DamageType):
        self.enemy = enemy
        self.damageType = damageType

    @property
    def is_attack(self):
        return self.enemy is not None
    
    @property
    def is_defense(self):
        return self.enemy is None
    
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