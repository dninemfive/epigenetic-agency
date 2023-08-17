using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace epigeneticagency;

public delegate Map? Action(Map map, IActor source);
public delegate Action DirectedAction(Direction direction);
public record ActionDef : IEnumerable<Action>
{
    private readonly HashSet<Action> _actions = new();
    #region constructors
    public ActionDef(Action action)
    {
        _actions.Add(action);
    }
    public ActionDef(DirectedAction directedAction)
    {
        foreach (Direction direction in Directions.Clockwise)
            _ = _actions.Add(directedAction(direction));
    }
    #endregion
    #region IEnumerable
    public IEnumerator<Action> GetEnumerator() 
        =>((IEnumerable<Action>)_actions).GetEnumerator();
    IEnumerator IEnumerable.GetEnumerator() 
        => ((IEnumerable)_actions).GetEnumerator();
    #endregion
}
public static class ActionDefs
{
    public static readonly ActionDef Move = new(direction => delegate(Map map, IActor actor)
            {
                Dictionary<Point, Cell> changes = new();
                Cell source = actor.Cell;
                Cell? dest = map[source.Position + direction.Offset()];
                if(dest is null || dest.OutOfBounds || dest.HasActor)
                {
                    return null;
                }
                changes[dest.Position] = new(dest, actor.CopyAt(dest.Position));
                changes[source.Position] = new(source, newActor: null);
                return new(map, changes);
            }
        );
}