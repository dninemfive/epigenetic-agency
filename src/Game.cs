using epigenetic_agency.results;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Cryptography.X509Certificates;
using System.Text;
using System.Threading.Tasks;

namespace epigenetic_agency;
public static class Game
{
    public static void Battle(Player player, Dictionary<string, Enemy> enemies, bool disableEpigenomeFeedback = false)
    {
        Logger.IncreaseIndent();
        int originalEnemyCount = enemies.Count;
        void DoTurn(int turnNumber)
        {
            Logger.IncreaseIndent();
            List<(Action action, int result)> results = new();
            Logger.Log($"Turn {turnNumber}: {player} vs {enemies.Values.ListString()}");
            Dictionary<string, Enemy> remainingEnemies = new();
            int initialPlayerHp = player.HP;
            for(int _ = 0; _ < Player.MOVES_PER_TURN; _++)
            {
                remainingEnemies.Clear();
                foreach ((string k, Enemy v) in enemies)
                {
                    if (v.Hp > 0)
                        remainingEnemies[k] = v;
                }
                Action nextAction = player.NextAction(remainingEnemies);
                (Action action, int result) feedback = nextAction.Apply(player);
                results.Add(feedback);
            }
            foreach (Enemy enemy in remainingEnemies.Values)
            {
                player.TakeHit(enemy.DamageType);
            }
            if(!disableEpigenomeFeedback)
            {
                int healCt = results.Where(x => x.action.IsDefense).Count();
                foreach((Action action, int result) in results)
                {
                    if(action.IsAttack)
                    {
                        player.Decider.ReceiveFeedback((action, result));
                    } else if(action.IsDefense)
                    {
                        player.Decider.ReceiveFeedback((action, (player.HP - initialPlayerHp) / (float)healCt));
                    }
                } 
            }
            Logger.DecreaseIndent();
        }
        int ct = 0;
        bool battleCompleted = false;
        while (player.HP > 0 && enemies.Values.Where(x => x.Hp > 0).Any())
        {
            ct++;
            DoTurn(ct);            
            if(ct > 100)
            {
                if(player.Decider is GenomeDecider gd2)
                {
                    gd2.Genome.CompleteBattle(0.1f);
                }
                battleCompleted = true;
                break;
            }
        }
        if (!battleCompleted && player.Decider is GenomeDecider gd)
            gd.Genome.CompleteBattle(originalEnemyCount);
        player.ReloadAmmo();
        Logger.DecreaseIndent();
    }
    public static Genome? BattleToDeath(Player player, bool disableEpigenomeFeedback = false)
    {
        Logger.IncreaseIndent();
        int battleCt = 0;
        while (player.HP > 0 && battleCt < 1000)
        {
            Logger.Log($"Battle {battleCt}:");
            Dictionary<string, Enemy> enemies = new();
            for(int i = 0; i < Program.Random.Next(1, 10); i++)
            {
                EnemyTemplate template = EnemyTemplate.Database.Values.RandomElement();
                string name = $"{template.Name} {i + 1}";
                enemies[name] = new(template, name);
            }
            Battle(player, enemies, disableEpigenomeFeedback);
            Logger.Log($"Player has died after {battleCt} battles!");
            battleCt++;
        }
        if (player.Decider is GenomeDecider gd)
            Logger.Log(gd.Genome);
        Logger.DecreaseIndent();
        return (player.Decider as GenomeDecider)?.Genome;
    }

}
