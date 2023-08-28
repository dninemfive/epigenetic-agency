using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace epigenetic_agency;
public class Epigene
{
    public float Expression { get; private set; }
    public Epigene(float expression = 0.5f)
    {
        Expression = expression;
    }
    public void ReceiveFeedback(ActionResult feedback, float adaptability)
        => Expression = (Expression + feedback.Result.Sigmoid() * adaptability).Clamp();
    public void ApplyCentralBias(float centralBias)
        => Expression = Utils.WeightedAverage(Expression, 0.5f, centralBias);
    public override string ToString()
        => $"<{Expression:P2}>";
    public Epigene Copy()
    {
        return new(Expression);
    }
}
