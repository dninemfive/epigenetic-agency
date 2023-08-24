The basic model for the game to be played.

The rules are as follows:
- The Player fights in a sequence of Battles until they are defeated, i.e. their HP drops to zero.
- During each Battle, Turns are played until either the Player or all Enemies are Defeated.
    - Each turn consists of the following steps:
        1. The Player attacks a randomly generated set of Enemies with an associated Damage Type, or No Type, until their Moves counter hits 0 or all Enemies are Defeated.
            - Each Damage Type has associated Ammo the Player must expend if the Damage Type is used. 
            - A Damage Type may only be used if the player has at least one Ammo for that Type.
            - The Player may always attack with No Type, which does not require or consume ammo.
            - The Player must use a Move each time they Attack, until either they run out of Moves for the Turn or all Enemies are defeated.
        2. Each Enemy makes one Attack with their own hardcoded Damage Type against the Player.
    - If at any point the Player or all Enemies are Defeated, the Battle ends, and the side which has not been Defeated wins.
- Damage Types have one associated type they are Strong against, and one they are Weak against. 
    - Attacks against a Strong type deal +1 Damage (3 vs 2);
    - Attacks against a Weak type deal -1 Damage (2 vs 1);
    - All other Attacks deal 2 Damage.