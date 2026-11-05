import random

ENCOUNTER_TILES = {4}
ENCOUNTER_CHANCE = 10

def check_encounter(grid, y, x):
    current_tile = grid[y][x]
    if current_tile not in ENCOUNTER_TILES:
        return False

    roll = random.randrange(100) # roll a number from 0 to 99
    if roll < ENCOUNTER_CHANCE:
        return True
    return False
