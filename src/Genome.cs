using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace epigenetic_agency;
public class Genome
{
    public Dictionary<string, Gene> Genes { get; private set; } = new();
    public float Fitness { get; private set; }
    public Genome(Dictionary<string, Gene>? genes = null, float fitness = 0)
    {
        if(genes is null)
        {
            foreach(Gene item in DefaultGenes)
            {
                Genes[item.Name] = item;
            }
        }
        else
        {
            Genes = genes;
        } 
        Fitness = fitness;
    }
    public void CompleteBattle(float reward = 1)
    {
        Fitness += reward;
        foreach(Gene g in ActionGenes)
        {
            g.Epigene?.ApplyCentralBias(Genes["Epigene Central Bias"]);
        }
    }
    public Action EvaluateActions(Player player, Dictionary<string, Enemy> enemies)
    {
        List<(Action action, float weight)> actions = new();
        foreach(Action action in Action.PossibleActions(player, enemies)) {
            actions.Add((action, EvaluateAction(player, enemies, action)));
        }
        return actions.WeightedRandomElement();
    }
    public float EvaluateAction(Player player, Dictionary<string, Enemy> enemies, Action action)
    {
        float weight = 1;
        int relevantGenes = 0;
        foreach(Gene gene in ActionGenes)
        {
            float? value = gene.EvaluateAction(player, enemies, action, Genes["Epigene Weight"]);
            if (value is not null)
            {
                relevantGenes++;
                weight += gene.Weight * value.Value;
            }
        }
        if (relevantGenes == 0)
            relevantGenes = 1;
        return (weight / relevantGenes).Clamp(min: 0, max: null);
    }
    public void ReceiveFeedback(ActionResult feedback)
    {
        foreach(Gene gene in ActionGenes)
        {
            gene.Epigene?.ReceiveFeedback(feedback, Genes["Epigene Adaptability"]);
        }
    }
    public IEnumerable<Gene> ActionGenes
        => Genes.Values.Where(x => x.IsActionGene);
    public static IEnumerable<Gene> DefaultGenes
    {
        get
        {
            yield return new("Epigene Adaptability");
            yield return new("Epigene Central Bias", 0.1f);
            yield return new("Epigene Weight");
            yield return new("Mutation Chance", 0.25f);
            yield return new("Mutation Magnitude", 0.1f);
            foreach((string name, ActionEvaluator ae) in ActionEvaluators.All)
            {
                yield return new(name, 0.5f, ae);
            }
        }
    }
    public override string ToString()
        => $"Genome({Fitness}; {Genes.Values.Select(x => x.ToString()).Aggregate((x, y) => $"{x}, {y}")})";
    public Gene this[string key] => Genes[key];
    public static Genome Cross(Genome a, Genome b)
    {
        Dictionary<string, Gene> newGenes = new();
        float ratio = a.Fitness / (float)b.Fitness;
        foreach(string key in a.Genes.Keys)
        {
            newGenes[key] = Gene.Cross(a[key], b[key], ratio)
                                .Mutate(Utils.WeightedAverage(a["Mutation Chance"], b["Mutation Chance"], ratio),
                                        Utils.WeightedAverage(a["Mutation Magnitude"], b["Mutation Magnitude"], ratio));
        }
        Genome result = new(newGenes);
        Logger.Log($"{a} cross {b} = {result}", 1);
        return result;
    }
    public static Genome BreedFrom(IEnumerable<Genome> genePool)
    {
        if (!genePool.Any())
            return new();
        if (genePool.Count() == 1)
            return genePool.First();
        Genome parentA = genePool.Select(x => (x, x.Fitness)).WeightedRandomElement(); // random.choices
        Genome parentB = genePool.Select(x => (x, x.Fitness)).WeightedRandomElement(); // random.choices
        return Cross(parentA, parentB);
    }
}
