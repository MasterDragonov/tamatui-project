from inventories import Inventory
import random

class Character:
    """A fighter in the game: the player or an enemy."""

    def __init__(self, name, level, max_hp, max_mp, attack, defence, speed, inventory):
        #Player stats
        self.name = name
        self.level = level
        self.max_hp = max_hp
        self.hp = max_hp
        self.max_mp = max_mp
        self.mp = max_mp
        self.attack = attack
        self.defence = defence
        self.speed = speed

        #Inventory and equipments
        self.inventory = inventory if inventory is not None else Inventory()
        self.equipped = {
            "weapon": None,
            "armor": None,
            "helmet": None,
            "boots": None,
            "accessory": None
        }

    def equip(self, item):
        if item not in self.inventory.items:
            print(f"{item.name} is not in {self.name}'s inventory.")
            return
        if item.slot not in self.equipped:
            print(f"{item.name} cannot be equipped.")
            return

        if self.equipped[item.slot] is not None:
            self.unequip(item.slot)

        self.inventory.remove_item(item)
        self.equipped[item.slot] = item

    def unequip(self, slot):
        item = self.equipped.get(slot)
        if item and self.inventory.add_item(item):
            self.equipped[slot] = None

    @property
    def total_attack(self):
        bonus = sum(item.b_attack for item in self.equipped.values() if item)
        return self.attack + bonus

    @property
    def total_defence(self):
        bonus = sum(item.b_defence for item in self.equipped.values() if item)
        return self.defence + bonus

    @property
    def total_speed(self):
        bonus = sum(item.b_speed for item in self.equipped.values() if item)
        return self.speed + bonus

    def take_damage(self, amount):
        """Lose HP, can't go below zero."""
        damage_taken = max(0, int(amount))
        self.hp = max(0, self.hp - damage_taken)
        return damage_taken

    def is_alive(self):
        """True while HP is more than 0."""
        return self.hp > 0

    def attack_target(self, target):
        """Attack another character and return damage dealt."""
        base_damage = (self.total_attack / 2) - (target.total_defence / 4)

        if base_damage < 1:
            damage = random.choice([0, 1])
        else:
            variance = base_damage / 16
            damage = int(random.uniform(base_damage - variance, base_damage + variance))
            damage = max(1, damage)
        return target.take_damage(damage)

    def spend_mp(self, cost):
        """Use MP if there is enough. Returns True if it was spent."""
        if self.mp < cost:
            return False
        self.mp -= cost
        return True

    def level_up(self):
        self.level+= 1
        
        


class Warrior(Character):
    """Sturdy front-line fighter"""

    def __init__(self, name):
        super().__init__(name, level=1, max_hp=40, attack=6, defence=5, max_mp=0, speed=4)
        self.job = "Warrior"


    def power_strike(self, target):
        """A heavy blow: double attack, but defence still applies."""
        damage = max(1, self.total_attack * 2 - target.total_defence)
        return target.take_damage(damage)

class Ranger(Character):
    """Quick archer: balanced stats, strikes twice with arrows."""

    def __init__(self, name):
        super().__init__(name, level=1, max_hp=32, attack=5, defence=3, max_mp=5, speed=8)
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
        super().__init__(name, level=1, max_hp=24, attack=8, defence=1, max_mp=10, speed=6)
        self.job = "Mage"

    def fireball(self, target):
        """Magic blast that ignores the target's defence."""
        if not self.spend_mp(self.FIREBALL_COST):
            return None
        damage = self.total_attack * 2
        return target.take_damage(damage)

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

