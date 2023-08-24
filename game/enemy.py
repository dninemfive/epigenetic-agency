from damage_type import damage_for

class EnemyTemplate(object):
    def __init__(self, name: str, base_hp: int, damage_type: str = None):
        self.name = name
        self.base_hp: int = base_hp
        self.damage_type: str = damage_type
    
ENEMY_TEMPLATES: dict[str, EnemyTemplate] = {
    "Zombie": EnemyTemplate("Zombie", 3, None)
}

class Enemy(object):
    def __init__(self, template: EnemyTemplate, name: str):
        self.template = template
        self.name = name
        self.hp = template.base_hp

    def take_hit(self, type: str) -> int:
        amt: int = damage_for(type, self.damage_type)
        self.hp -= amt
        return amt

    @property
    def damage_type(self):
        return self.template.damage_type

    def __str__(self) -> str:
        return self.name + " (" + self.template.name + ", " + str(self.hp) + "/" + str(self.template.base_hp) + ")"