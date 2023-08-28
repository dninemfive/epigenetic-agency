using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace epigenetic_agency;
public delegate float? ActionEvaluator(Player player, Enemies enemies, Action action);
public static class ActionEvaluators
{
    public static readonly IEnumerable<(string name, ActionEvaluator ae)> All = new List<(string name, ActionEvaluator ae)>()
    {
        ("target low hp enemies",
            (p, e, a) => a.IsAttack ? 1 - a.Enemy!.HpPercentage : null),
        ("target high hp enemies",
            (p, e, a) => a.IsAttack ? a.Enemy!.HpPercentage : null),
        ("prefer attack",
            (p, e, a) => a.IsAttack ? 1 : 0),
        ("prefer defense",
            (p, e, a) => a.IsDefense ? 1 : 0),
        ("prefer defense when at low HP",
            (p, e, a) => a.IsDefense ? 1 - p.HpPercentage : null),
        ("exploit enemy weaknesses",
            (p, e, a) => a.IsAttack ? a.Damage - (int)Damage.Default : null)
    };
}
