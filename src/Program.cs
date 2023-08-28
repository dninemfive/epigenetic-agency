using epigenetic_agency;
using epigenetic_agency.results;
using System.IO;

internal class Program
{
    public static Random Random = new();
    private static void Main(string[] args)
    {
        string baseFolder = "src/results/cs/";
        for(int j = 0; j < 10; j++)
        {
            string filePath = Path.Join(baseFolder, $"epigenome{j}.txt");
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
                Logger.Log($"Generation {j}/{i}: {meanFitness:P2}");
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