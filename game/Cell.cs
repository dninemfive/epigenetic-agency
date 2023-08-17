using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace epigeneticagency;
public class Cell : ILocationHaver
{
    public Location Location { get; private set; }
    public IActor? Actor { get; private set; }
    public bool HasActor => Actor is not null;
    public Item? Item { get; private set; }
    public bool HasItem => Item is not null;
    public bool OutOfBounds => ((ILocationHaver)this).OutOfBounds;
    public Point Position => ((ILocationHaver)this).Position;
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
}