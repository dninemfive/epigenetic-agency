using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Cryptography.X509Certificates;
using System.Text;
using System.Threading.Tasks;

namespace epigenetic_agency;
public delegate GameStateDifference Action(IActor source, IActor target, GameState state);
public Action Heal = delegate(IActor source, IActor _, GameState state)
{
    
}
public record Act
{
    public IActor Source { get; private set; }
    private Func<GameState, GameStateDifference> _action;
    public Action(IActor source, Func<GameState, GameStateDifference> action)
    {
        Source = source;
        _action = action;
    }
}