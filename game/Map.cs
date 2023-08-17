﻿using System;
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
    private readonly Cell[,] _cells;
    public int Width  => _cells.GetLength(0);
    public int Height => _cells.GetLength(1);
    public Map(int width, int height)
    {
        _cells = new Cell[width, height];
        for (int x = 0; x < width; x++)
            for (int y = 0; y < height; y++)
                _cells[x, y] = new(this, x, y);
    }
    public Map(Map parent, IReadOnlyDictionary<Point, Cell> changedCells)
    {
        _cells = new Cell[parent.Width, parent.Height];
        foreach(Cell cell in parent.Cells)
        {
            Point position = cell.Position;
            (int x, int y) = position;
            _cells[x, y] = changedCells.TryGetValue(position, out Cell? value) ? value : cell;
        }
    }
    public bool IsInBounds(int x, int y) => x >= 0 && x < Width && y >= 0 && y < Height;
    public bool IsInBounds((int x, int y) tuple) => IsInBounds(tuple.x, tuple.y);
    public Cell? this[int x, int y] => IsInBounds(x, y) ? _cells[x, y] : null;
    public Cell? this[(int x, int y) tuple] => this[tuple.x, tuple.y];
    public Cell? NeighborInDirection(Point p, Direction d) => this[p + d.Offset()];
    public IEnumerable<Cell> NeighborsOf(Point p)
    {
        foreach(Direction d in Directions.Clockwise)
        {
            Cell? neighbor = NeighborInDirection(p, d);
            if (neighbor is not null)
                yield return neighbor;
        }
    }
    public IEnumerable<Cell> NeighborsOf(ILocationHaver locHaver) => NeighborsOf(locHaver.Position);
    public IEnumerable<IEnumerable<Cell>> Rows
    {
        get
        {
            for(int x = 0;  x < Width; x++)
            {
                List<Cell> row = new();
                for (int y = 0; y < Height; y++)
                    row.Add(_cells[x, y]);
                yield return row;
            }
        }
    }
    public IEnumerable<Cell> Cells
    {
        get
        {
            foreach(IEnumerable<Cell> row in Rows)
            {
                foreach (Cell cell in row)
                    yield return cell;
            }
        }
    }
    public override string ToString()
    {
        string result = string.Empty;
        foreach(IEnumerable<Cell> row in Rows)
        {
            foreach(Cell cell in row)
            {
                result += cell.Icon;
            }
            result += "\n";
        }
        return result;
    }
}
