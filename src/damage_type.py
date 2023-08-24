class DamageType(object):
    def __init__(self, name: str, strong_against: str):
        self.name: str = name
        self.strong_against: callable = lambda dt : dt.name == strong_against
    
    def damage_against(self, other):
        if self.strong_against(other):
            return 3
        if other.strong_against(self):
            return 1
        return 2
    
    def __str__(self):
        return self.name
    
_types: dict[DamageType, DamageType] = {
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
        return 1
    return DAMAGE_TYPES[attackerType].damage_against(defenderType)