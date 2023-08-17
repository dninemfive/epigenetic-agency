using System;
using System.Collections;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace epigeneticagency;
public class Map
{
    private readonly Node[,] _nodes;
    public int Width  => _nodes.GetLength(0);
    public int Height => _nodes.GetLength(1);
    public Map(int width, int height)
    {
        _nodes = new Node[width, height];
        for (int x = 0; x < width; x++)
            for (int y = 0; y < height; y++)
                _nodes[x, y] = new(this, x, y);
    }
    public Map(Map parent, Point changeLocation, Node changedNode)
    {
        _nodes = new Node[parent.Width, parent.Height];
        foreach(Node node in parent.Nodes)
        {
            
        }
    }
    public bool IsInBounds(int x, int y) => x >= 0 && x < Width && y >= 0 && y < Height;
    public bool IsInBounds((int x, int y) tuple) => IsInBounds(tuple.x, tuple.y);
    public Node? this[int x, int y] => IsInBounds(x, y) ? _nodes[x, y] : null;
    public Node? this[(int x, int y) tuple] => this[tuple.x, tuple.y];
    public IEnumerable<IEnumerable<Node>> Rows
    {
        get
        {
            for(int x = 0;  x < Width; x++)
            {
                List<Node> row = new();
                for (int y = 0; y < Height; y++)
                    row.Add(_nodes[x, y]);
                yield return row;
            }
        }
    }
    public IEnumerable<Node> Nodes
    {
        get
        {
            foreach(IEnumerable<Node> row in Rows)
            {
                foreach (Node cell in row)
                    yield return cell;
            }
        }
    }
    public IEnumerable<Point> Points
    {
        get
        {
            for(int y = 0; y < Height; y++)
            {
                for(int x = 0; x < Width; x ++)
                {
                    yield return (x, y);
                }
            }
        }
    }
    public override string ToString()
    {
        string result = string.Empty;
        foreach(IEnumerable<Node> row in Rows)
        {
            foreach(Node node in row)
            {
                result += node.Icon;
            }
            result += "\n";
        }
        return result;
    }
}
