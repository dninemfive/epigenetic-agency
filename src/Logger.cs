using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace epigenetic_agency;
public class Logger
{
    private static string _currentPrefix = "";
    public const string INDENT = "  ";
    public static int CurrentIndent => _currentPrefix.Length / INDENT.Length;
    public const int DEFAULT_MAX_INDENT = 0;
    public static void IncreaseIndent()
        => _currentPrefix += INDENT;
    public static void DecreaseIndent()
        => _currentPrefix = _currentPrefix[0..^INDENT.Length];
    public static void Log(object? obj, int? indent = null, int maxIndent = DEFAULT_MAX_INDENT, bool alwaysPrint = false)
    {
        // break early up here for performance
        if (indent is not null && indent > maxIndent && !alwaysPrint)
            return;
        string prefix = _currentPrefix;
        if(indent is not null)
        {
            prefix = "";
            for(int _ = 0; _ < indent; _++)
            {
                prefix += INDENT;
            }
        }
        indent ??= CurrentIndent;
        if(alwaysPrint || indent <= maxIndent)
        {
            Console.WriteLine($"{prefix}{obj}");
        }
    }
}
