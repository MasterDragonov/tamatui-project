class Character:
    """A fighter in the game: the player or an enemy."""

    def __init__(self, name, max_hp, attack, defence):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.attack = attack
        self.defence = defence


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


if __name__ == "__main__":
    hero = Character("Lucas", 30, 6, 3,)
    slime = Character("SLime", 12, 4, 1)

    while hero.is_alive() and slime.is_alive():
