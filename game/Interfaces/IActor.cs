using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace epigeneticagency;
public interface IActor : ILocationHaver
{
    public bool Try(Map initial, Action action, out Map? result);
}