from player import Player, Decider_Genome
from enemy import Enemy, ENEMY_TEMPLATES
from damage_type import damage_for
from utils import list_str

def battle(player: Player, enemies: dict[str, Enemy]) -> None:
    """
    A player fights enemies until either the player is dead or all the enemies are dead.
    """
    def do_turn(turnNumber: int):
        print("Turn", turnNumber, ":\n",player, "\n", list_str(enemies.values()))
        player.do_attacks(enemies)
        for enemy in [x for x in enemies.values() if x.hp > 0]:
            print("SDCSDCSDC", damage_for(enemy.damage_type, None))
            dmg: int = player.take_hit(enemy.damage_type)
            print(enemy, "attacks player for", dmg, "damage!")
    print("Player HP:", player.hp)
    for enemy in enemies.values():
        print(enemy.hp)
    ct: int = 0
    while player.hp > 0 and any([x for x in enemies.values() if x.hp > 0]):
        ct += 1
        do_turn(ct)
    # player heals hp?

if __name__ == "__main__":
    player: Player = Player(Decider_Genome())
    enemies: dict[str, Enemy] = {}
    for i in range(2):
        name: str = str(i + 1)
        enemies[name] = Enemy(ENEMY_TEMPLATES["Zombie"], name)
    enemies['3'] = Enemy(ENEMY_TEMPLATES["Skeleton"], "3")
    battle(player, enemies)
