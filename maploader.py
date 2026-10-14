import curses


# Dictionary that defines the ASCII shapes and colours for map elements.
# Strings are 4 characters wide to ensure game window is not squashed.
TILE_LOOKUP = {
    # Grass
    0: (["\u2591\u2591\u2591\u2591",
         "\u2591\u2591\u2591\u2591"], curses.COLOR_GREEN),

    # Trees
    1: (["\u2663\u2663\u2663\u2663",
         "\u2663\u2663\u2663\u2663"], curses.COLOR_YELLOW),

    # Water
    2: (["\u2591\u2591\u2591\u2591",
         "\u2591\u2591\u2591\u2591"], curses.COLOR_BLUE)
}


def load_map(filename):
    """Reads a text file to convert it into a 2D matrix.

    This function strips spaces/commas to parse values into integers
    for a tile map lookup table.

    Args:
        filename (str): Filename of the textfile to be loaded.

    Returns:
        list of list of int: 2D list where grid[y][x] contains an integer."""

    grid = []
    with open(filename, "r") as f:
        for line in f:
            cleaned_line = line.strip().replace(",", " ")
            if cleaned_line:
                grid.append([int(tile) for tile in cleaned_line.split()])
    return grid
