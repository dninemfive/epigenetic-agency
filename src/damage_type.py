WEAK_DAMAGE, DEFAULT_DAMAGE, STRONG_DAMAGE = 1, 2, 3

class DamageType(object):
    """
    Defines a damage type, which determines how much damage an attack does against a specified enemy.
    """
    def __init__(self, name: str, strong_against: str):
        self.name: str = name
        self.strong_against: callable = lambda dt : dt.name == strong_against
    
    def damage_against(self, other) -> int:
        if other is None: return DEFAULT_DAMAGE
        if isinstance(other, str): return self.damage_against(DAMAGE_TYPES[other])
        if self.strong_against(other):
            return STRONG_DAMAGE
        if other.strong_against(self):
            return WEAK_DAMAGE
        return DEFAULT_DAMAGE
    
    def __str__(self):
        return "DamageType(" + self.name + ")"
    
    def __repr__(self):
        return self.__str__()
    
_types: dict[DamageType, DamageType] = {
    "None": "not strong against anything",
    "Fire": "Frost",
    "Water": "Fire",
    "Earth": "Water",
    "Wind": "Earth",
    "Lightning": "Wind",
    "Frost": "Lightning"
}

DAMAGE_TYPES: dict[str, DamageType] = {
    k: DamageType(k, v) for k, v in _types.items()
}

def damage_for(attackerType: str, defenderType: str):
    if attackerType not in DAMAGE_TYPES or defenderType not in DAMAGE_TYPES:
        return DEFAULT_DAMAGE
    return DAMAGE_TYPES[attackerType].damage_against(defenderType)