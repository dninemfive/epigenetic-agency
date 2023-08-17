using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Text;
using System.Threading.Tasks;

namespace epigeneticagency;
public class Item : ILocationHaver
{
    public Location Location { get; private set; }
    public ItemDef Def { get; private set; }
    public string Name => Def.Name;
    public IEnumerable<Action>? Action => Def.Actions;
    public char Icon => Def.Icon;
    public Item(ItemDef def, Location location)
    {
        Location = location;
        Def = def;
    }
}
public readonly struct ItemDef
{
    public readonly string Name;
    public readonly ActionDef? Actions;
    public readonly char Icon;
    public ItemDef(string name, char icon, ActionDef? actionDef = null) 
    {
        Name = name;
        Icon = icon;
        Actions = actionDef;
    }
}