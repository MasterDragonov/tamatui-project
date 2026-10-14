import curses
import os

def load_map(filename):
    """Reads a text file to convert it into a 2D matrix.
    
    This function strips spaces/commas to parse values into integers
    for a tile map lookup table.
    
    Args:
        filename (str): Filename of the textfile to be loaded.
        
    Returns:
        list of list of int: 2D list array where grid[y][x] contains an integer.
    """
    
    grid = []
    with open(filename, "r") as f:
        for line in f:
            cleaned_line = line.strip().replace(",", " ")
            if cleaned_line:
                grid.append([int(tile) for tile in cleaned_line.split()])
    return grid
