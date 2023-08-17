using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace epigeneticagency;
public class Cell
{
    public IActor? Actor { get; private set; }
    public bool HasActor => Actor is not null;
    public Item? Item { get; private set; }
    public bool HasItem => Item is not null;
    public Cell(Location location)
    {
        Location = location;
    }
    public Cell(Cell old, Item? newItem) : this(old.Location)
    {
        Actor = old.Actor;
        Item = newItem;
    }
    public Cell(Cell old, IActor? newActor) : this(old.Location)
    {
        Actor = newActor;
        Item = old.Item;
    }
    public Cell(Cell old, IActor newActor, Item newItem) : this(old.Location)
    {
        Actor = newActor;
        Item = newItem;
    }
    public Cell(Map map, int x, int y) : this(new(map, (x, y))) { }
    public char Icon
    {
        get
        {
            if (Actor is not null)
                return Actor.Icon;
            if (Item is not null)
                return Item.Icon;
            return ' ';
        }
    }
    public Map Map => Location.Map;
    public Point Position => Location.Point;
    public bool InBounds => Map.IsInBounds(Position);
    public bool OutOfBounds => !InBounds;
    public IEnumerable<Cell> Neighbors => Map.NeighborsOf(this);
    public override string ToString() => $"{Icon}";
    public static implicit operator Point(Cell cell) => cell.Position;
}