using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace epigeneticagency;
public class Cell
{
    public readonly Location Location;
    public Map Map => Location.Map;
    public Point Point => Location.Point;    
    public Cell(Location location)
    {
        Location = location;
    }
    public Cell(Map map, int x, int y) : this(new(map, (x, y))) { }
}