using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading.Tasks;

namespace epigenetic_agency;
public record EnemyTemplate
{
    public readonly string Name;
    public readonly int BaseHp;
    public readonly DamageType DamageType;
    public EnemyTemplate(string name, int baseHp, DamageType damageType = DamageType.None)
    {
        Name = name;
        BaseHp = baseHp;
        DamageType = damageType;
    }
    public static readonly Dictionary<string, EnemyTemplate> Database = new()
    {
        { "Zombie",     new("Zombie",       5, DamageType.None  ) },
        { "Blaze",      new("Blaze",        5, DamageType.Fire  ) },
        { "Silverfish", new("Silverfish",   2, DamageType.Earth ) },
        { "Chillager",  new("Chillager",    5, DamageType.Frost ) }
    };
}
public class Enemy : IActionTarget<int>
{
    public EnemyTemplate Template { get; private set; }
    public string Name { get; private set; }
    public int Hp { get; private set; }
    public DamageType DamageType => Template.DamageType;
    public int BaseHp => Template.BaseHp;
    public float HpPercentage => Hp / (float)BaseHp;
    public Enemy(EnemyTemplate template, string name)
    {
        Template = template;
        Name = name;
        Hp = template.BaseHp;
    }
    public int ApplyAction(Action action)
    {
        int amt = action.DamageType.DamageAgainst(DamageType);
        Hp -= amt;
        return amt;
    }
    public override string ToString()
        => $"{Name} ({Template.Name}, {Hp}/{Template.BaseHp})";
}
public class Enemies
{
    public Dictionary<string, Enemy> Value { get; private set; }
    public Enemies(Dictionary<string, Enemy> value)
    {
        Value = value;
    }
    public static implicit operator Enemies(Dictionary<string, Enemy> value) => new(value);
    public static implicit operator Dictionary<string, Enemy>(Enemies enemies) => enemies.Value;
}