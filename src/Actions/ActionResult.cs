using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace epigenetic_agency;
public struct ActionResult
{
    public Action Action;
    public GameStateDifference Result;
    public static implicit operator ActionResult((Action a, GameStateDifference r) tuple) => new()
    {
        Action = tuple.a,
        Result = tuple.r
    };
    public static implicit operator (Action action, GameStateDifference result)(ActionResult ar)
        => (ar.Action, ar.Result);
}