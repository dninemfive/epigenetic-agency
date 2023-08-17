using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace epigeneticagency;
public interface IItemHaver
{
    public IEnumerable<Item> Items { get; }
}