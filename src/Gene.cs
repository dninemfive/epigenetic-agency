using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Cryptography.X509Certificates;
using System.Text;
using System.Threading.Tasks;

namespace epigenetic_agency;
public class Gene
{
    public string Name { get; private set; }
    private float _weight;
    public float Weight => _weight * Epigene?.Expression ?? 1;
    public ActionEvaluator? ActionEvaluator { get; private set; }
    public Epigene? Epigene { get; private set; }
    public Gene(string name, float weight = 0.5f, ActionEvaluator? evaluator = null, Epigene? epigene = null)
    {
        Name = name;
        _weight = weight;
        ActionEvaluator = evaluator;
        Epigene = epigene;
    }
    public float? EvaluateAction(Player player, Dictionary<string, Enemy> enemies, Action action, float weight)
    {
        if (ActionEvaluator is null)
            throw new InvalidOperationException("Genes without an ActionEvaluator can't evaluate actions!");
        float? result = ActionEvaluator(player, enemies, action);
        return result is null ? null : result * weight;
    }
    public override string ToString()
        => $"<{Name}:{Weight:P2}{Epigene?.ToString() ?? ""}>";
    public static Gene Cross(Gene a, Gene b, float ratio = 0.5f)
    {
        if (a.Name != b.Name)
            throw new Exception("Can only cross Genes of the same type!");
        float combinedWeight = Utils.WeightedAverage(a._weight, b._weight, ratio);
        return new(a.Name, combinedWeight, a.ActionEvaluator, ratio > 1 ? a.Epigene : b.Epigene);
    }
    public Gene Mutate(float chance = 0.25f, float magnitude = 0.1f)
    {
        if (chance is < 0 or > 1)
            throw new ArgumentOutOfRangeException(nameof(chance));
        if (magnitude < 0)
            throw new ArgumentOutOfRangeException(nameof(magnitude));
        if(Program.Random.NextDouble() < chance)
        {
            float newWeight = (_weight - magnitude / 2 + (float)Program.Random.NextDouble() * magnitude).Clamp();
            return new(Name, newWeight, ActionEvaluator, Epigene?.Copy());
        }
        return new(Name, _weight, ActionEvaluator, Epigene?.Copy());
    }
    public bool HasEpigene => Epigene is not null;
    public bool HasActionEvaluator => ActionEvaluator is not null;
    public static implicit operator float(Gene gene) => gene.Weight;
}
