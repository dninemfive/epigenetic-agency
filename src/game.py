from player import Player, Decider_Genome
from enemy import Enemy, ENEMY_TEMPLATES
from utils import list_str
import random

NUMBER_OF_ENEMIES: int = 40
NUMBER_OF_GAMES: int = 100
PLAYER_HP: int = 1000

def battle(player: Player, enemies: dict[str, Enemy]) -> None:
    """
    A player fights enemies until either the player is dead or all the enemies are dead.
    """
    def do_turn(turnNumber: int):
        print("Turn", turnNumber, ":\n",player, "\n", list_str(enemies.values()))
        player.do_attacks(enemies)
        for enemy in [x for x in enemies.values() if x.hp > 0]:
            dmg: int = player.take_hit(enemy.damage_type)
            print(enemy, "attacks player for", dmg, "damage!")
            print("Player's remaining HP:", player.hp)

            if player.hp <= 0:
                print("Player died!")
                return
    
    ct: int = 0
    while player.hp > 0 and any([x for x in enemies.values() if x.hp > 0]):
        ct += 1
        print('\n\n')
        do_turn(ct)

    print("Battle over!")
    print("Total turns:", ct)
    enemies_defeated = NUMBER_OF_ENEMIES - len(enemies)
    print("Total defeated enemies:", enemies_defeated)

    if (player.hp > 0):
        print("Player wins!")
        print("Player's remaining HP:", player.hp)
        return True
    else:
        print("Player loses!")
        return False

    # player heals hp?

def setup():
    player: Player = Player(Decider_Genome(), PLAYER_HP)
    enemies: dict[str, Enemy] = {}
    enemy_types: list[str] = list(ENEMY_TEMPLATES.keys())

    for i in range(NUMBER_OF_ENEMIES):
        name: str = str(i + 1)
        chosen_enemy_type = random.choice(enemy_types)  
        enemies[name] = Enemy(ENEMY_TEMPLATES[chosen_enemy_type], name)

    return battle(player, enemies)

if __name__ == "__main__":
    winCount = 0
    for i in range(NUMBER_OF_GAMES):
        if setup():
            winCount += 1
    print('win count:', winCount)
