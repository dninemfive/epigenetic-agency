using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace epigenetic_agency;
public static class Utils
{
    public static string ListString(this IEnumerable<object> items, bool printType = false, bool printBrackets = true)
    {
        string tostring(object obj)
            => printType ? $"{obj.GetType().Name} {obj}" : obj.ToString()!;
        string result = items.Select(tostring).Aggregate((x, y) => $"{x}, {y}");
        return printBrackets ? $"[{result}]" : result;
    }
    public static float WeightedAverage(float a, float b, float ratio)
    {
        if (ratio is < 0 or > 1)
            throw new ArgumentOutOfRangeException(nameof(ratio));
        return a * ratio + (b * (1 - ratio));
    }
    public static float Clamp(this float value, float? min = 0, float? max = 1)
    {
        if (min is not null && value < min)
            return min.Value;
        if (max is not null && value > max)
            return max.Value;
        return value;
    }
    public static float Sigmoid(this float x, float x_0 = 0, float L = 1, float k = 1)
        => L / (1 + (float)Math.Pow(Math.E, -(k * (x - x_0))));
    public static float Sigmoid(this int x, float x_0 = 0, float L = 1, float k = 1)
        => ((float)x).Sigmoid(x_0, L, k);
    public static float Average(params float[] vals)
        => vals.Sum() / vals.Length;
    public static T RandomElement<T>(this IEnumerable<T> items)
        => items.ElementAt(Program.Random.Next(0, items.Count()));
    public static T WeightedRandomElement<T>(this IEnumerable<(T item, float weight)> items)
    {
        float total = items.Select(x => x.weight).Sum();
        float target = (float)Program.Random.NextDouble() * total;
        float sum = 0;
        foreach((T item, float weight) in items)
        {
            sum += weight;
            if (sum >= target)
                return item;
        }
        throw new Exception($"Somehow, WeightedRandomElement ran out of weight: total {total}, target {target}, sum {sum}");
    }
}
