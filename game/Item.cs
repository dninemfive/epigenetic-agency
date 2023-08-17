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
    public Item(ItemDef def, Location location)
    {
        Location = location;
        Def = def;
    }
}
public class ItemDef
{
    public string Name;
    public ActionDef? Actions;
    public ItemDef(string name, ActionDef? actionDef = null) 
    {
        Name = name;
        Actions = actionDef;
    }
}