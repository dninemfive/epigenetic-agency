from gene import GeneTemplate

class DamageType(object):
    """
    Defines a damage type, which determines how much damage an attack does against a specified enemy.
    """
    def __init__(self, name: str, strong_against: str):
        self.name: str = name
        self.strong_against: callable = lambda dt : dt.name == strong_against
    
    def damage_against(self, other) -> int:
        if self.strong_against(other):
            return 3
        if other.strong_against(self):
            return 1
        return 2
    
    def __str__(self):
        return self.name
    
_types: dict[DamageType, DamageType] = {
    "None": None,
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

DAMAGE_TYPE_GENES: dict[str, GeneTemplate] = {
    k: GeneTemplate(k) for k in _types.keys()
}

def damage_for(attackerType: str, defenderType: str):
    if attackerType not in DAMAGE_TYPES or defenderType not in DAMAGE_TYPES:
        return 1
    return DAMAGE_TYPES[attackerType].damage_against(defenderType)