from player import Player
from enemy import Enemy, ENEMY_TEMPLATES
from utils import list_str
from types import EnemyName
from decider import Decider_CLI

def battle(player: Player, enemies: dict[str, Enemy]) -> None:
    """
    A player fights enemies until either the player is dead or all the enemies are dead.
    """
    def do_turn(turnNumber: int):
        print("Turn", turnNumber, ":\n",player, "\n", list_str(enemies.values()))
        player.do_attacks(enemies)
        for enemy in [x for x in enemies.values() if x.hp > 0]:
            dmg: int = player.take_hit(enemy.damage_type)
            print(enemy.name,"attacks player for", dmg, "damage!")
    print(player.hp)
    for enemy in enemies.values():
        print(enemy.hp)
    ct: int = 0
    while player.hp > 0 and any([x for x in enemies.values() if x.hp > 0]):
        ct += 1
        do_turn(ct)
    # player heals hp?

if __name__ == "__main__":
    player: Player = Player(Decider_CLI())
    enemies: dict[EnemyName, Enemy] = {}
    for i in range(2):
        name: str = "Zombie " + str(i + 1)
        enemies[name] = Enemy(ENEMY_TEMPLATES["Zombie"], name)
    battle(player, enemies)