using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace epigenetic_agency;
internal interface ISnapshotable<T> where T : struct // i want to make it readonly too but idk how??
{
    public T Snapshot();
}
