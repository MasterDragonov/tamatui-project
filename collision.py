WALKABLE_TILES = {0}

def is_walkable(grid, y, x):
    map_height = len(grid) - 1 # find the map height -1 for buffer
    map_length = len(grid[0]) - 1 # find the map length -1 for buffer 
    if y > map_height or y < 0: # if y position is not within limits
        return False
    if x > map_length or x < 0: # if x position is not within limits
        return False
    tile = grid[y][x]
    if tile in WALKABLE_TILES:
        return True
    return False
