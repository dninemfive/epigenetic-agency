using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace epigeneticagency;

public delegate Map? Action(Map map, Direction direction, IActor source);
public record ActionDef
{
    public bool TakesDirectionArguments;
    public ActionDef(Action action, bool takesDirections = true)
    {

    }
}