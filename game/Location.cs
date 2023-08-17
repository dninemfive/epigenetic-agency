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
    /// <summary>
    /// The <see cref="epigeneticagency.Cell"/> this location is associated with.
    /// </summary>
    /// <remarks>
    /// Known to be non-null because <see cref="epigeneticagency.Map"/>[<see cref="epigeneticagency.Point"/>] is 
    /// <see langword="null"/> if and only if point is out-of-bounds, which is checked in the constructor.
    /// </remarks>
    public Cell Cell => Map[Point]!;
    public Location(Map map, Point point)
    {
        Map = map;
        if (!Map.IsInBounds(Point))
            throw new ArgumentOutOfRangeException(nameof(point));
        Point = point;
    }
}