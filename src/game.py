from player import Player, Decider_Genome, DEFAULT_AMMO, HEAL_AMOUNT
from enemy import Enemy, EnemyTemplate, ENEMY_TEMPLATES
from utils import list_str
from gene import Genome, cross
import random
from typing import Any
from logger import increase_indent, decrease_indent, log
from action import Action, ActionResult

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

if __name__ == "__main__":
    for j in range(10):
        filename: str = f"src/results/without_epigenome_{j}.txt"
        # I HATE PYTHON!!!! AAAAAAAAAAAAAAAA
        with open(filename, "x"):
            pass
        with open(filename, "a") as file:
            gene_pool: list[Genome] = []
            next_genome: Genome = Decider_Genome().genome
            for i in range(7500):        
                player: Player = Player(Decider_Genome(next_genome))
                gene_pool.append(battles_until_death(player, disable_epigenome_feedback=True))
                next_genome: Genome = new_genome(gene_pool)
                mean_fitness: float = sum([x.fitness for x in gene_pool]) / len(gene_pool)
                # https://stackoverflow.com/a/46062115
                log(f"Generation {j}.{i}: fitness {mean_fitness:.2f}")
                file.write(f"{mean_fitness}\n")
                new_gene_pool: list[Genome] = [x for x in gene_pool if x.fitness > mean_fitness]
                if len(new_gene_pool) > 10:
                    # log(f"Dropping {list_str([x for x in gene_pool if x not in new_gene_pool])}", 1)
                    gene_pool = new_gene_pool