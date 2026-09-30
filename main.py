import curses

TILE_MAP = [
    [0, 0, 2, 0, 0, 0, 1, 1, 1, 1, 0, 0, 2],
    [0, 0, 0, 0, 0, 0, 1, 2, 1, 0, 1, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

TILE_LOOKUP = {
    0: (["░░", 
         "░░"], curses.COLOR_GREEN),   # Tall Grass (Dense block texture)
    
    1: (["♣♣", 
         "♣♣"], curses.COLOR_YELLOW),  # Trees (Thick trees)
    
    2: (["~~", 
         "~~"], curses.COLOR_BLUE)     # Water (Clear waves)
}


def main(stdscr):
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_GREEN, -1)
    curses.init_pair(2, curses.COLOR_YELLOW, -1)
    curses.init_pair(3, curses.COLOR_BLUE, -1)
    curses.init_pair(4, curses.COLOR_RED, -1) # Player color

    color_map = {
        0: curses.color_pair(1),
        1: curses.color_pair(2),
        2: curses.color_pair(3)
    }
    curses.curs_set(0)

    while True:
        stdscr.clear()

        for r_idx, row in enumerate(TILE_MAP):
            for c_idx, tile_type in enumerate(row):
                lines, _ = TILE_LOOKUP[tile_type]
                color = color_map[tile_type]
                stdscr.addstr(r_idx * 2, c_idx * 2, lines[0], color)
                stdscr.addstr(r_idx * 2 + 1, c_idx * 2, lines[1], color)
        stdscr.refresh()
        stdscr.getch()

curses.wrapper(main)