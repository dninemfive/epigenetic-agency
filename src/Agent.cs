using epigenetic_agency.Actions;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace epigenetic_agency;
public class Agent : IActor, IHitPointHaver, ISnapshotable<AgentSnapshot>, IDiffable<Agent>
{
    public int HitPoints { get => throw new NotImplementedException(); set => throw new NotImplementedException(); }

    public void Apply(Action action, bool isSource = false)
    {
        throw new NotImplementedException();
    }
    public IDifference<Agent> DifferenceFrom(Agent other)
    {
        throw new NotImplementedException();
    }

    public Action NextAction(GameState state)
    {
        throw new NotImplementedException();
    }

    public AgentSnapshot Snapshot()
    {
        throw new NotImplementedException();
    }
}
public readonly struct AgentSnapshot
{

}