using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace epigeneticagency;
public class Item : ILocationHaver
{
    public Location Location { get; private set; }
    public ItemDef Def { get; private set; }
    public string Name => Def.Name;
    public Action? Action => Def.Action;
    public Item(ItemDef def, Location location)
    {
        Location = location;
        Def = def;
    }
}
public class ItemDef
{
    public string Name;
    public Action? Action;
    public ItemDef(string name, Action? action = null) 
    {
        Name = name;
        Action = action;
    }
}