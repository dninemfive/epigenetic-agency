using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace epigeneticagency;
public interface ILocationHaver
{
    public Location Location { get; }
    public Map Map => Location.Map;
    public Point Position => Location.Point;
    public Cell Cell => Location.Cell;
    public bool InBounds => Map.IsInBounds(Position);
    public bool OutOfBounds => !InBounds;
    public IEnumerable<Cell> Neighbors => Map.NeighborsOf(this);
}