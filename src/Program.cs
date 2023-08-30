using epigenetic_agency;
using epigenetic_agency.results;
using System.IO;

internal class Program
{
    public static Random Random = new();
    private static void Main(string[] args)
    {
        int n = 10;
        if (args.Length > 0 && int.TryParse(args[0], out int val))
            n = val;
        string baseFolder = "results/";
        DateTime startTime = DateTime.Now;
        for(int j = 0; j < n; j++)
        {
            string filePath = Path.Join(baseFolder, $"epigenome{j}.txt");
            _ = Directory.CreateDirectory(baseFolder);
            using FileStream fs = File.Open(filePath, FileMode.OpenOrCreate);
            using StreamWriter sw = new(fs);
            List<Genome> genePool = new();
            Genome nextGenome = new GenomeDecider().Genome;
            for(int i = 0; i < 7500; i++)
            {
                Player player = new(new GenomeDecider(nextGenome));
                genePool.Add(Game.BattleToDeath(player)!);
                nextGenome = Genome.BreedFrom(genePool);
                float meanFitness = genePool.Select(x => x.Fitness).Average();
                if(i % 69 == 0)
                {
                    Logger.Log($"Generation {j}-{i}: {meanFitness:F2} ({(DateTime.Now - startTime)})");
                    startTime = DateTime.Now;
                }
                sw.WriteLine(meanFitness);
                List<Genome> newGenePool = genePool.Where(x => x.Fitness > meanFitness).ToList();
                if(newGenePool.Count > 10)
                {
                    genePool = newGenePool;
                }
            }
        }
    }
}