using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace epigenetic_agency;
public interface IDiffable<TSelf>
{
    public IDifference<TSelf> DifferenceFrom(TSelf other);
    public static IDifference<TSelf> operator -(IDiffable<TSelf> a, TSelf b)
        => a.DifferenceFrom(b);
}
public interface IDifference<TSelf>
{
    public TSelf AddedTo(TSelf instance);
    public static TSelf operator +(TSelf instance, IDifference<TSelf> diff)
        => diff.AddedTo(instance);
}