We should formalize the concept of an "action." In this game, an action is either an attack or a defense.

When attacking, the player targets an enemy with a damage type (or None). The enemy takes damage based on the damage type and, if applicable, the player consumes the appropriate ammo. This can be represented as the tuple (enemy, damageType).

When defending, the player chooses a damage type (or None). The player heals a fixed amount of HP and takes damage from enemies based on the chosen type. If applicable, the player consumes the appropriate ammo. This can be represented as the tuple (None, damageType).