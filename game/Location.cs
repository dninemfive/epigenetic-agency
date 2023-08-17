using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace epigeneticagency;
public readonly struct Location
{
    public readonly Map Map;
    public readonly Point Point;
    public Location(Map map, Point point)
    {
        Map = map;
        Point = point;
    }
}
