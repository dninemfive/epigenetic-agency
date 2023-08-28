using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace epigenetic_agency;
public enum Damage
{
    Weak = 1,
    Default = 2,
    Strong = 3
}
public enum DamageType
{
    None,
    Fire,
    Water,
    Earth,
    Wind,
    Lightning,
    Frost
}
public static class DamageTypes
{
    public static IEnumerable<DamageType> All
        => Enum.GetValues<DamageType>();
    public static readonly Dictionary<DamageType, DamageType?> TypeStrengths = new()
    {
        { DamageType.None, null },
        { DamageType.Fire,      DamageType.Frost    },
        { DamageType.Water,     DamageType.Fire     },
        { DamageType.Earth,     DamageType.Water    },
        { DamageType.Wind,      DamageType.Earth    },
        { DamageType.Lightning, DamageType.Wind     },
        { DamageType.Frost,     DamageType.Fire     }
    };
    public static bool IsStrongAgainst(this DamageType attacker, DamageType defender)
        => TypeStrengths[attacker] == defender;
    public static int DamageAgainst(this DamageType attacker, DamageType defender)
    {
        if (attacker.IsStrongAgainst(defender))
            return (int)Damage.Strong;
        if (defender.IsStrongAgainst(attacker))
            return (int)Damage.Weak;
        return (int)Damage.Default;
    }
}
