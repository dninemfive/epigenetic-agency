from player import Player, Decider_Genome, DEFAULT_AMMO
from enemy import Enemy, EnemyTemplate, ENEMY_TEMPLATES
from utils import list_str
from gene import Genome, cross_genome
import random
from typing import Any
from logger import increase_indent, decrease_indent, log

def battle(player: Player, enemies: dict[str, Enemy]) -> None:
    """
    A player fights enemies until either the player is dead or all the enemies are dead.
    """
    increase_indent()
    def do_turn(turnNumber: int):
        increase_indent()
        log(f"Turn {turnNumber}: {player} vs {list_str(enemies.values())}")
        player.do_attacks(enemies)
        for enemy in [x for x in enemies.values() if x.hp > 0]:
            dmg: int = player.take_hit(enemy.damage_type)
            log(f"{enemy.name} attacks player for {dmg} damage!")
        decrease_indent()
    ct: int = 0
    while player.hp > 0 and any([x for x in enemies.values() if x.hp > 0]):
        ct += 1
        do_turn(ct)
    if isinstance(player.decider, Decider_Genome): 
        player.decider.genome.complete_battle()
    # refill ammo
    for k in player.ammo.keys():
        if k == "None": continue
        player.ammo[k] = DEFAULT_AMMO
    # player heals hp?
    decrease_indent()

def battles_until_death(player: Player) -> Genome:
    assert isinstance(player.decider, Decider_Genome)
    increase_indent()
    battle_ct: int = 0
    while player.hp > 0:
        log(f"Battle {battle_ct}:")
        enemies: dict[str, Enemy] = {}
        while sum([x.hp for x in enemies.values()]) < 3:
            template: EnemyTemplate = random.choice([x for x in ENEMY_TEMPLATES.values()])
            name: str = template.name + " " + str(i + 1)
            enemies[name] = Enemy(template, name)
        battle(player, enemies)
        log(f"Player has died after {player.decider.genome.fitness - 1} battles!")
        battle_ct += 1
    log(player.decider.genome)
    decrease_indent()
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
    next_genome: Genome = Decider_Genome().genome
    for i in range(10000):        
        player: Player = Player(Decider_Genome(next_genome))
        gene_pool.append(battles_until_death(player))
        next_genome: Genome = new_genome(gene_pool)
        mean_fitness: float = sum([x.fitness for x in gene_pool]) / len(gene_pool)
        # https://stackoverflow.com/a/46062115
        log(f"Generation {i}: fitness {mean_fitness:.2f}")
        new_gene_pool: list[Genome] = [x for x in gene_pool if x.fitness > mean_fitness]
        if len(new_gene_pool) > 10:
            log(f"Dropping {list_str([x for x in gene_pool if x not in new_gene_pool])}", 1)
            gene_pool = new_gene_pool
    print("Final gene pool:")
    i: int = 1
    for item in gene_pool:
        print(i,":",item)
        i += 1