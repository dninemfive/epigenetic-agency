using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace epigenetic_agency.results;
public interface IDecider
{
    public Action ChooseAction(Player player, Dictionary<string, Enemy> enemies);
    public void ReceiveFeedback<T>(ActionResult<T> feedback);
}
public class GenomeDecider : IDecider
{
    public Genome Genome { get; private set; }
    public GenomeDecider(Genome? genome = null)
    {
        Genome = genome ?? new();
    }
    public Action ChooseAction(Player player, Dictionary<string, Enemy> enemies)
        => Genome.EvaluateActions(player, enemies);
    public void ReceiveFeedback<T>(ActionResult<T> feedback)
        => Genome.ReceiveFeedback(feedback);
    public override string ToString()
        => $"GenomeDecider({Genome})";
}
