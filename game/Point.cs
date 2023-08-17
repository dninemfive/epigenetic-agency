using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace epigeneticagency;
public readonly struct Point
{
    public readonly int X, Y;
    private Point(int x, int y)
    {
        X = x;
        Y = y;
    }
    public static implicit operator Point((int x, int y) tuple) => new(tuple.x, tuple.y);
    public static implicit operator (int x, int y)(Point p) => (p.X, p.Y);
    public static Point operator +(Point a, Point b) => new(a.X + b.X, a.Y + b.Y);
    public static Point operator -(Point a, Point b) => new(a.X - b.X, a.Y - b.Y);
    public static bool operator ==(Point a, Point b) => a.X == b.X && a.Y == b.Y;
    public static bool operator !=(Point a, Point b) => !(a == b);

    public override bool Equals(object? obj) => obj is Point p && this == p;

    public override int GetHashCode() => HashCode.Combine(X.GetHashCode(), Y.GetHashCode());
}