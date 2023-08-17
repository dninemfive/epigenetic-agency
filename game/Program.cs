using epigeneticagency;

internal class Program
{
    private static void Main(string[] args)
    {
        static void print(Map map)
        {
            string bar = string.Empty;
            for (int _ = 0; _ < map.Width; _++)
                bar += "-";
            Console.WriteLine($"{bar}\n{map}\n{bar}");
        }
        Map initial = new(10,15);
        print(initial);
        Map withPlayer = new(initial, new Dictionary<Point, Node>()
        {
            { (4, 7), new(initial[4, 7], new Player(initial[4, 7].Location)) }
        });
        print(withPlayer);
    }
}