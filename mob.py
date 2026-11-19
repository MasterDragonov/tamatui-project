import os
from characters import Character

class Monster(Character):
    """An extension of Character containing distinct visual assets."""
    def __init__(self, name, level, max_hp, attack, defence, ascii_art):
        super().__init__(name, level, max_hp, attack, defence)
        self.ascii_art = ascii_art

def load_monster(filepath):
    if not os.path.exists(filepath):
        return None

    with open(filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    if not lines:
        return None

    config_line = lines[0].strip()
    name, level, max_hp, attack, defence = config_line.split(',')

    ascii_art = [line.rstrip('\n') for line in lines[1:]]

    return Monster(
        name=name.strip(),
        level=int(level.strip()),
        max_hp=int(max_hp.strip()),
        attack=int(attack.strip()),
        defence=int(defence.strip()),
        ascii_art=ascii_art
    )

def monster_pool():
    monster_pool = []
    mobs_dir = os.path.join("assets", "mobs")

    if os.path.exists(mobs_dir):
        for filename in os.listdir(mobs_dir):
            if filename.endswith(".txt"):
                filepath = os.path.join(mobs_dir, filename)
                monster_obj = load_monster(filepath)
                if monster_obj:
                    monster_pool.append(monster_obj)

    if not monster_pool:
        monster_pool.append(Monster("Missingno", 1, 10, 2, 0, [" [?] "]))

    return monster_pool