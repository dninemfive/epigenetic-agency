using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace epigenetic_agency;
public readonly struct GameState : IDiffable<GameState>
{
    public IEnumerable<Action> PossibleActions { get; }
    public IDifference<GameState> DifferenceFrom(GameState other)
    {
    }
}
public readonly struct GameStateDifference : IDifference<GameState>
{

}