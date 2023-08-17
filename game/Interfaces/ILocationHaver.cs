using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace epigeneticagency;
public interface ILocationHaver
{
    public Location Location { get; }
    public char Icon { get; }
    public Point Position() => Location.Point;
    public Cell Cell => Location.Cell;
}