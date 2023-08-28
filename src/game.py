from player import Player, Decider_Genome, DEFAULT_AMMO
from enemy import Enemy, EnemyTemplate, ENEMY_TEMPLATES
from utils import list_str
from gene import Genome, cross
import random
from typing import Any
from logger import increase_indent, decrease_indent, log
from action import Action, ActionResult
import time
import numpy as np

def battle(player: Player, enemies: dict[str, Enemy], disable_epigenome_feedback: bool = False) -> None:
    """
    A player fights enemies until either the player is dead or all the enemies are dead.
    """
    increase_indent()
    original_enemy_count: int = len(enemies)
    def do_turn(turnNumber: int):
        increase_indent()
        actionResults: list = []
        log(f"Turn {turnNumber}: {player} vs {list_str(enemies.values())}")
        remainingEnemies: dict[str, Enemy] = {k: v for k, v in enemies.items() if v.hp > 0}
        initial_player_hp: int = player.hp
        for _ in range(player.remainingMoves):
            next_action: Action = player.next_action(remainingEnemies)
            result: ActionResult = next_action.apply(player)
            actionResults.append(result)
            remainingEnemies: dict[str, Enemy] = {k: v for k, v in enemies.items() if v.hp > 0}
        for enemy in remainingEnemies.values():
            dmg: int = player.take_hit(enemy.damage_type)        
        # performed at the end of the turn to avoid having the model change during a turn
        # maybe should change that back, except that healing feedback won't be available at the end of turn
        if not disable_epigenome_feedback:
            healct = len([x for x in actionResults if x[0].is_defense])
            for result in actionResults:
                if result[0].is_attack:
                    player.decider.receive_feedback(result[1])
                if result[0].is_defense:
                    player.decider.receive_feedback((player.hp - initial_player_hp) / float(healct))
        decrease_indent()
    def finalize(reward: float = 1):
        if isinstance(player.decider, Decider_Genome):
            player.decider.genome.complete_battle(reward)
    ct: int = 0
    finalized: bool = False
    while player.hp > 0 and any([x for x in enemies.values() if x.hp > 0]):
        ct += 1
        do_turn(ct)
        if ct > 100:
            finalize(0.1)
            finalized = True
            break
    if not finalized: finalize(original_enemy_count)
    # refill ammo
    for k in player.ammo.keys():
        if k == "None": continue
        player.ammo[k] = DEFAULT_AMMO
    decrease_indent()

def battles_until_death(player: Player, disable_epigenome_feedback: bool = False) -> Genome:
    assert isinstance(player.decider, Decider_Genome)
    increase_indent()
    battle_ct: int = 0
    while player.hp > 0 and battle_ct < 1000:
        log(f"Battle {battle_ct}:")
        enemies: dict[str, Enemy] = {}
        for i in range(int(random.random() * 10)):
            template: EnemyTemplate = random.choice([x for x in ENEMY_TEMPLATES.values()])
            name: str = template.name + " " + str(i + 1)
            enemies[name] = Enemy(template, name)
        battle(player, enemies, disable_epigenome_feedback)
        log(f"Player has died after {player.decider.genome.fitness - 1} battles!")
        battle_ct += 1
    log(player.decider.genome)
    decrease_indent()
    return player.decider.genome

def new_genome(gene_pool: list[Genome]):
    assert len(gene_pool) > 0
    if len(gene_pool) == 1:
        return gene_pool[0]
    elif len(gene_pool) == 2:
        # handle the 2-parent case for performance
        return cross(gene_pool[0], gene_pool[1])
    else:
        parents = random.choices(gene_pool, weights=[x.fitness for x in gene_pool], k=2)
        return cross(parents[0], parents[1])
    
TEST_LENGTH: int = 10000
DataItem = list[float]

def do_test(name: str, data_out: list[list[DataItem]], epigenome: bool, index: int) -> Genome:
    gene_pool: list[Genome] = []
    next_genome: Genome = Decider_Genome().genome
    start_time: float = None
    def log_data(gene_pool: list[Genome], i: int, start_time: float) -> float:
        gene_pool_size = len(gene_pool)
        fitnesses: list[float] = [x.fitness for x in gene_pool]        
        mean_fitness: float = sum(fitnesses) / gene_pool_size
        data_line: DataItem = [mean_fitness]
        for quartile in [0, 1, 2, 3, 4]:
            data_line.append(np.quantile(fitnesses, quartile / 4))
        if i % 69 == 0:
            timestr = "n/a" if start_time is None else f"{time.time() - start_time:.2f}s"
            data_line_str = ""
            for item in data_line:
                data_line_str += f"{item:6.1f}\t"
            log(f"{name} {index:02}-{i:04}:\t{data_line_str}({timestr})")
            start_time: float = time.time()
        data_out[i].append(data_line)
        return start_time
    for i in range(TEST_LENGTH):
        player: Player = Player(Decider_Genome(next_genome))
        gene_pool.append(battles_until_death(player, disable_epigenome_feedback=not epigenome))
        gene_pool_size: int = len(gene_pool)
        if gene_pool_size > 20:
            gene_pool = sorted(gene_pool, key=lambda x: x.fitness, reverse=True)
            for i in range(gene_pool_size // 2):
                gene_pool.pop()
        start_time = log_data(gene_pool, i, start_time)
        next_genome: Genome = new_genome(gene_pool)
    best_epigenome_of_pool: Genome = max(gene_pool, key=lambda x: x.fitness)
    return best_epigenome_of_pool

def write_data(data: list[list[DataItem]], filename: str):
    with open(f"src/results/{filename}.tsv", "w") as _:
        pass
    with open(f"src/results/{filename}.tsv", "a") as file:
        for dataLine in data:
            line: str = ""
            for item in dataLine:
                for f in item:
                    line += f"{f}\t"
                line += "\t"
            file.write(f"{line}\n")

if __name__ == "__main__":
    epigenome_data: list[list[DataItem]] = []
    non_epigenome_data: list[list[DataItem]] = []
    for i in range(TEST_LENGTH):
        epigenome_data.append([])
        non_epigenome_data.append([])
    best_epigenome_genome: Genome = None
    best_non_epigenome_genome: Genome = None    
    def write_all_data():
        write_data(epigenome_data, "epigenome_data")
        write_data(non_epigenome_data, "non-epigenome_data")
        with open("src/results/best_genomes.txt", "w") as file:
            file.writelines([str(best_epigenome_genome), "", str(best_non_epigenome_genome)])
    for i in range(10):
        start_time: float = time.time()
        genome: Genome = do_test("epi", epigenome_data, True, i)
        print(f"Total time elapsed: {time.time() - start_time:.2f}s")
        if best_epigenome_genome is None or genome.fitness > best_epigenome_genome.fitness:
            best_epigenome_genome = genome
        start_time: float = time.time()
        genome = do_test("non", non_epigenome_data, False, i)
        print(f"Total time elapsed: {time.time() - start_time:.2f}s")
        if best_non_epigenome_genome is None or genome.fitness > best_non_epigenome_genome.fitness:
            best_non_epigenome_genome = genome
        write_all_data()
    