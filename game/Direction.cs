using System;
using System.Collections.Generic;
using System.Data;
using System.Diagnostics.Tracing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace epigeneticagency;
public enum Direction
{
    None, Up, Right, Left, Down
}
public static class Directions
{
    public static IEnumerable<Direction> Clockwise => Enum.GetValues<Direction>().Skip(1);
    public static IEnumerable<Direction> Counterclockwise => Clockwise.Reverse();
    public static (int x, int y) Offset(this Direction direction) => direction switch
    {
        Direction.None  => (0,  0),
        Direction.Up    => (0,  1),
        Direction.Right => (1,  0),
        Direction.Down  => (0, -1),
        Direction.Left  => (-1, 0),
        _ => throw new ArgumentOutOfRangeException(nameof(direction))
    };
}