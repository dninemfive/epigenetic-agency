using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace epigeneticagency;
public class Player : IActor, IItemHaver
{
    public Location Location { get; private set; }
    public Player(Location location)
    {
        Location = location;
    }
    public bool Try(Map original, Action action, out Map? result)
    {
        result = action(original, Direction.None, this);
        return result is not null;
    }
}