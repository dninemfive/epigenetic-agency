from action import Action
from utils import sigmoid
from damage_type import WEAK_DAMAGE, DEFAULT_DAMAGE, STRONG_DAMAGE

# gene(s) for targeting enemies based on hp and damagetype
def target_low_hp_enemies(player, enemies, action: Action) -> float:
    if action.is_attack:
        return 1 - action.enemy.hp_percentage
    return 0

def target_high_hp_enemies(player, enemies, action: Action) -> float:
    if action.is_attack:
        return action.enemy.hp_percentage
    return 0

# gene for how much the player likes to attack
def prefer_attack(player, enemies, action: Action) -> float:
    return 1 if action.is_attack else 0

# gene for how much the player likes to heal
def prefer_defense(player, enemies, action: Action) -> float:
    return 1 if action.is_defense else 0

# gene which changes the weights of attacking/healing based on hp??
def prefer_defense_low_hp(player, enemies, action: Action) -> float:
    if action.is_attack: return 0
    return 1 - player.hp_percentage

# gene(s) for targeting enemies based on hp and damagetype
def exploit_enemy_weaknesses(player, enemies, action: Action) -> float:
    if action.is_defense: return 0
    return action.damageType.damage_against(action.enemy.damage_type) - DEFAULT_DAMAGE

# prioritize enemies which do more damage to us
# (player can only be weak to enemies when healing for now)

ALL = [target_low_hp_enemies, target_high_hp_enemies, prefer_attack, prefer_defense, prefer_defense_low_hp, exploit_enemy_weaknesses]