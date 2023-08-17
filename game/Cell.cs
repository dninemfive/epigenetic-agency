using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace epigeneticagency;
public class Cell : ILocationHaver
{
    public Location Location { get; private set; }
    public Map Map => Location.Map;
    public Point Position => Location.Point;
    public IActor? Actor { get; private set; }
    public Item? Item { get; private set; }
    public Cell(Location location)
    {
        Location = location;
    }
    public Cell(Map map, int x, int y) : this(new(map, (x, y))) { }
    public IEnumerable<Cell> Neighbors => Map.NeighborsOf(this);
}