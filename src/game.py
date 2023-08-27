from player import Player, Decider_Genome
from enemy import Enemy, ENEMY_TEMPLATES
from utils import list_str
from gene import Genome, cross_genome
import random

def battle(player: Player, enemies: dict[str, Enemy]) -> None:
    """
    A player fights enemies until either the player is dead or all the enemies are dead.
    """
    def do_turn(turnNumber: int):
        print("\tTurn", turnNumber, ":",player,"vs",list_str(enemies.values()))
        player.do_attacks(enemies)
        for enemy in [x for x in enemies.values() if x.hp > 0]:
            dmg: int = player.take_hit(enemy.damage_type)
            print("\t\t", enemy.name,"attacks player for", dmg, "damage!")
    for enemy in enemies.values():
        print(enemy.hp)
    ct: int = 0
    while player.hp > 0 and any([x for x in enemies.values() if x.hp > 0]):
        ct += 1
        do_turn(ct)
    if isinstance(player.decider, Decider_Genome): 
        player.decider.genome.complete_battle()
    # player heals hp?

def battles_until_death(player: Player) -> Genome:
    assert isinstance(player.decider, Decider_Genome)
    battle_ct: int = 0
    while player.hp > 0:
        print("\tBattle",battle_ct)
        enemies: dict[str, Enemy] = {}
        for i in range(int(random.random() * 2) + 1):
            name: str = str(i + 1)
            enemies[name] = Enemy(ENEMY_TEMPLATES["Zombie"], name)
        battle(player, enemies)
        print("\tPlayer has died after",player.decider.genome.fitness - 1,"battles!")
        battle_ct += 1
    return player.decider.genome

def new_genome(gene_pool: list[Genome]):
    assert len(gene_pool) > 0
    if len(gene_pool) == 1:
        return gene_pool[0]
    else:
        parents = random.choices(gene_pool, weights=[x.fitness for x in gene_pool], k=2)
        return cross_genome(parents[0], parents[1])

if __name__ == "__main__":
    gene_pool: list[Genome] = []
    next_genome = Decider_Genome().genome
    for i in range(10):
        print("Generation",i)
        player: Player = Player(Decider_Genome(next_genome))
        gene_pool.append(battles_until_death(player))
        next_genome = new_genome(gene_pool)