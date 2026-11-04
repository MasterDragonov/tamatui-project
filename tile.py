import curses

class Tile:
    TILE_LOOKUP = {
        0: (["░░░░", "░░░░"], curses.COLOR_GREEN),   # Grass
        1: (["♣♣♣♣", "♣♣♣♣"], curses.COLOR_YELLOW),  # Trees
        2: (["░░░░", "░░░░"], curses.COLOR_BLUE),    # Water
        3: (["· ° ", "   ·"], curses.COLOR_WHITE)    # Cave
    }

    def __init__(self, tile_type):
        self.tile_type = tile_type

    def draw(self, stdscr, screen_y, screen_x, max_y, max_x, color_map):
        if self.tile_type in self.TILE_LOOKUP:
            lines, _ = self.TILE_LOOKUP[self.tile_type]
            color = color_map[self.tile_type]

            y_pos1 = screen_y * 2
            y_pos2 = screen_y * 2 + 1
            x_pos = screen_x * 4

            if y_pos2 < max_y and x_pos + 3 < max_x:
                stdscr.addstr(y_pos1, x_pos, lines[0], color)
                stdscr.addstr(y_pos2, x_pos, lines[1], color)