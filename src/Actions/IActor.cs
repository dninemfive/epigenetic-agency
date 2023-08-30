using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace epigenetic_agency;

public interface IActor
{
    public Action NextAction(GameState state);
    public void Apply(Action action, bool isSource = false);
}