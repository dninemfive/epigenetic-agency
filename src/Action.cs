using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Cryptography.X509Certificates;
using System.Text;
using System.Threading.Tasks;

namespace epigenetic_agency;
public record Action
{
    public Enemy? Enemy { get; private set; }
    public DamageType DamageType { get; private set; }
    public Action(Enemy? enemy, DamageType damageType)
    {
        Enemy = enemy;
        DamageType = damageType;
    }
    public (Action action, int result) Apply(Player player)
    {
        int result = 0;
        if(IsAttack)
        {
            player.ApplyAction(this);
            int originalEnemyHp = Enemy!.Hp;
            result = Enemy.ApplyAction(this);
            Logger.Log($"Player attacks {Enemy.Name} with {DamageType} for {Damage} damage ({originalEnemyHp} -> {Enemy.Hp})");
        }
        if(IsDefense)
        {
            int originalPlayerHp = player.HP;
            player.ApplyAction(this);
            int hpDelta = player.HP - originalPlayerHp;
            Logger.Log($"Player defends with {DamageType}, healing {hpDelta} HP ({originalPlayerHp} -> {player.HP})");
        }
        return (this, result);
    }
    public bool IsAttack => Enemy is not null;
    public bool IsDefense => Enemy is null;
    public int Damage
        => IsDefense ? 0 : DamageType.DamageAgainst(Enemy!.DamageType);
    public override string ToString()
        => $"Action({Enemy}, {DamageType})";
    public static implicit operator Action((Enemy? enemy, DamageType damageType) tuple)
        => new(tuple.enemy, tuple.damageType);
    public static IEnumerable<Action> PossibleActions(Player player, Dictionary<string, Enemy> enemies)
    {
        foreach(Enemy enemy in enemies.Values)
        {
            foreach (DamageType dt in player.AvailableAmmo)
                yield return (enemy, dt);
        }
        foreach (DamageType dt in player.AvailableAmmo)
            yield return (null, dt);
    }
}
public struct ActionResult
{
    public Action Action;
    public float Result;
    public static implicit operator ActionResult((Action a, float r) tuple) => new()
    {
        Action = tuple.a,
        Result = tuple.r
    };
    public static implicit operator (Action action, float result)(ActionResult ar)
        => (ar.Action, ar.Result);
}