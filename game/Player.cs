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
    public Player(Player original, Point newPos)
    {
        Location = new(original.Location.Map, newPos);
    }
    public bool Try(Map original, Action action, out Map? result)
    {
        result = action(original, this);
        return result is not null;
    }
    public IActor CopyAt(Point pos) => new Player(this, pos);
    private readonly List<Item> _items = new();
    public IEnumerable<Item> Items => _items;
}