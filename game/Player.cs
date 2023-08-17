using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace epigeneticagency;
public class Actor : ICellResident, IItemHaver
{
    public Cell Cell { get; private set; }
    public Actor(Cell cell)
    {
        Cell = cell;
    }
    public Actor(Actor original, Cell newCell)
    {
        Cell = newCell;
        _items = original._items;
    }
    public bool Try(Action action, out Map? result)
    {
        result = action(this);
        return result is not null;
    }
    private readonly List<Item> _items = new();
    public IEnumerable<Item> Items => _items;
    public char Icon => 'P';
}