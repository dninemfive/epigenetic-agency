using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace epigeneticagency;
public interface ICellResident
{
    public Cell Cell { get; }
    public char Icon { get; }
}