from damage_type import damage_for
from action import Action

class EnemyTemplate(object):
    """
    A template for 
    """
    def __init__(self, name: str, base_hp: int, damage_type: str = None):
        self.name = name
        self.base_hp: int = base_hp
        self.damage_type: str = damage_type
    
ENEMY_TEMPLATES: dict[str, EnemyTemplate] = {
    "Zombie": EnemyTemplate("Zombie", 5, "None"),
    "Blaze": EnemyTemplate("Blaze", 5, "Fire"),
    "Silverfish": EnemyTemplate("Silverfish", 2, "Earth"),
    "Chillager": EnemyTemplate("Chillager", 5, "Frost") 
}

class Enemy(object):
    def __init__(self, template: EnemyTemplate, name: str):
        self.template = template
        self.name = name
        self.hp = template.base_hp

    def apply_action(self, action: Action) -> int:
        amt: int = damage_for(action.damageType, self.damage_type)
        self.hp -= amt
        return amt

    @property
    def damage_type(self):
        return self.template.damage_type

    def __str__(self) -> str:
        return self.name + " (" + self.template.name + ", " + str(self.hp) + "/" + str(self.template.base_hp) + ")"
    
    @property
    def hp_percentage(self) -> float:
        return self.hp / self.template.base_hp