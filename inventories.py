class Inventory:
        """Inventory class usable for characters shops and chests."""
        def __init__(self, capacity=10):
            self.capacity = capacity
            self.items = []

        def add_item(self, item):
            if len(self.items) < self.capacity:
                self.items.append(item)
                return True
            return False

        def remove_item(self, item):
            if item in self.items:
                self.items.remove(item)
                return True
            return False

class Item:
    def __init__(self, name, slot=None, b_hp=0, b_mp=0, b_attack=0, b_defence=0, b_speed=0):
        self.name = name
        self.slot = slot
        self.b_hp = b_hp
        self.b_mp = b_mp
        self.b_attack = b_attack
        self.b_defence = b_defence
        self.b_speed = b_speed