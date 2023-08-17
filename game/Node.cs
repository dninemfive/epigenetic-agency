using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace epigeneticagency;
public abstract class Node
{
    public IEnumerable<Node> Previous { get; private set; }
    public IEnumerable<Node> Next { get; private set; }
    public Node(IEnumerable<Node> previous,  IEnumerable<Node> next)
    {
        Previous = previous;
        Next = next;
    }
    public abstract char Icon { get; }
}
public class Node_Combat : Node
{
    IEnumerable<Enemy> Enemies;
    public Node_Combat(IEnumerable<Node> previous, IEnumerable<Node> next) : base(previous, next) { }
    public override char Icon => 'C';
}
public class Node_Empty : Node
{
    public Node_Empty(IEnumerable<Node> previous, IEnumerable<Node> next) : base(Enumerable.Empty<Node>(), Enumerable.Empty<Node>()) { }
    public override char Icon => ' ';
}