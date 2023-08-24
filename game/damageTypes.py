from types import DamageType

DAMAGE_TYPE_BONUSES: dict[DamageType, DamageType] = {
    "Fire": "Frost",
    "Water": "Fire",
    "Earth": "Water",
    "Wind": "Earth",
    "Lightning": "Wind",
    "Frost": "Lightning"
}

def damage_modifier_for(attackerType: DamageType, defenderType: DamageType):
    if attackerType not in DAMAGE_TYPE_BONUSES or defenderType not in DAMAGE_TYPE_BONUSES: return 0
    if DAMAGE_TYPE_BONUSES[attackerType] == defenderType: return 1
    if DAMAGE_TYPE_BONUSES[defenderType] == attackerType: return -1
    return 0 