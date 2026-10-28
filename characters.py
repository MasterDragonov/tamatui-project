class Character:
    """A fighter in the game: the player or an enemy."""

    def __init__(self, name, max_hp, attack, defence, max_mp=0):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.attack = attack
        self.defence = defence
        self.max_mp = max_mp
        self.mp = max_mp


    def take_damage(self, amount):
        """Lose HP, can't go below zero."""
        self.hp = max(0, self.hp - amount)

    def is_alive(self):
        """True while HP is more than 0."""
        return self.hp > 0

    def attack_target(self, target):
        """Attack another character and return damage dealt."""
        damage = max(1, self.attack - target.defence)
        target.take_damage(damage)
        return damage

    def spend_mp(self, cost):
        """Use MP if there is enough. Returns True if it was spent."""
        if self.mp < cost:
            return False
        self.mp -= cost
        return True


class Warrior(Character):
    """Sturdy front-line fighter"""

    def ___init__(self, name):
        super().__init__(name, max_hp=40, attack=6, defence=5)
        self.job = "Warrior"


    def power_strike(self, target):
        """A heavy blow: double attack, but defence still applies."""
        damage = max(1, self.attack * 2 - target.defence)
        target.take_damage(damage)
        return damage

class Ranger(Character):
    """Quick archer: balanced stats, strikes twice with arrows."""

    def __init__(self, name):
        super().__init__(name, max_hp=32, attack=5, defence=3)
        self.job = "Ranger"

    def double_shot(self, target):
        """Fire two arrows, each a normal attack. Returns total damage."""
        first = self.attack_target(target)
        second = 0
        if target.is_alive():
            second = self.attack_target(target)
        return first + second


class Mage(Character):
    """Fragile spellcaster: low HP and defence, powerful magic."""

    FIREBALL_COST = 3

    def __init__(self, name):
        super().__init__(name, max_hp=24, attack=8, defence=1, max_mp=10)
        self.job = "Mage"

    def fireball(self, target):
        """Magic blast that ignores the target's defence."""
        if not self.spend_mp(self.FIREBALL_COST):
            return None
        damage = self.attack * 2
        target.take_damage(damage)
        return damage

if __name__ == "__main__":
    hero = Mage("Lucas")
    slime = Character("Slime", 30, 4, 1)

    while hero.is_alive() and slime.is_alive():
        damage = hero.fireball(slime)
        if damage is None:
            print(f"{hero.name} is out of MP and swings the staff!")
            damage = hero.attack_target(slime)
        print(f"{hero.name} hits {slime.name} for {damage}. "
                f"{slime.name} HP: {slime.hp} ({hero.name} MP: {hero.mp})")


        if slime.is_alive():
            damage = slime.attack_target(hero)
            print(f"{slime.name} hits {hero.name} for {damage}. "
                  f"{hero.name} HP: {hero.hp}")

    if hero.is_alive():
        print(f"{hero.name} wins!")
    else:
         print(f"{slime.name} wins!")

