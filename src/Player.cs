using epigenetic_agency.results;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Numerics;
using System.Text;
using System.Threading.Tasks;

namespace epigenetic_agency;
public class Player
{
    public const int DEFAULT_HP = 25,
                     DEFAULT_AMMO = 10,
                     HEAL_AMOUNT = 5,
                     MOVES_PER_TURN = 3;
    public int HP { get; private set; } = DEFAULT_HP;
    public Dictionary<DamageType, int?> Ammo { get; private set; } = new();
    public IDecider Decider { get; private set; }
    public DamageType CurrentType { get; private set; } = DamageType.None;
    public Player(IDecider decider)
    {
        foreach(DamageType damageType in DamageTypes.All)
        {
            Ammo[damageType] = DEFAULT_AMMO;
        }
        Ammo[DamageType.None] = null;
        Decider = decider;
    }
    public Action? NextAction(Dictionary<string, Enemy> enemies)
        => Decider.ChooseAction(this, enemies);
    public void ApplyAction(Action action)
    {
        if (action.IsAttack)
        {
            CurrentType = DamageType.None;
            ConsumeAmmo(action.DamageType);
        }
        else
        {
            CurrentType = action.DamageType;
            HP += HEAL_AMOUNT;
        }
    }
    public void TakeHit(DamageType dt)
    {
        HP -= dt.DamageAgainst(CurrentType);
    }
    public void ConsumeAmmo(DamageType dt)
    {
        if (!HasAmmo(dt))
            return;
        Ammo[dt]--;
    }
    public bool HasAmmo(DamageType dt)
        => Ammo[dt] is null or > 0;
    public IEnumerable<DamageType> AvailableAmmo
        => Ammo.Keys.Where(HasAmmo);
    public float HpPercentage
        => HP / (float)DEFAULT_HP;
    public override string ToString()
        => $"Player({HP})";
    public void ReloadAmmo()
    {
        foreach (DamageType k in Ammo.Keys)
        {
            if (k is DamageType.None)
                continue;
            Ammo[k] = DEFAULT_AMMO;
        }
    }
}
