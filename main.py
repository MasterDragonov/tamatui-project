import curses
from maploader import load_map

TILE_MAP_FILE = "map1.txt"

# Dictionary that defines the ASCII shapes and colours for map elemts.
# Strings are 4 characters wide to ensure game window is not squashed.
TILE_LOOKUP = {
    0: (["░░░░", 
         "░░░░"], curses.COLOR_GREEN),   # Grass
    
    1: (["♣♣♣♣", 
         "♣♣♣♣"], curses.COLOR_YELLOW),  # Trees
    
    2: (["░░░░", 
         "░░░░"], curses.COLOR_BLUE)     # Water
}


def main(stdscr):

    # Curses Initialisation
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

    stdscr.keypad(True)

    # Map loading function: Read the 2D grid from the filepath
    tile_map_grid = load_map(TILE_MAP_FILE)
    map_height = len(tile_map_grid)
    map_width = len(tile_map_grid[0]) if map_height > 0 else 0

    # Track the player co-ordinates
    player_y = 5
    player_x = 5

    # Game loop
    while True:
        stdscr.clear()

        # Window size to calculate tiles to fit on screen
        max_y, max_x = stdscr.getmaxyx()
        visible_tiles_y = max_y // 2
        visible_tiles_x = max_x // 4

        # Camera viewport, center the camera over the moving player
        camera_y = player_y - (visible_tiles_y // 2)
        camera_x = player_x - (visible_tiles_x // 2)

        # Boundary clamp to restrict the camera co-ords at the edges
        camera_y = max(0, min(camera_y, map_height - visible_tiles_y))
        camera_x = max(0, min(camera_x, map_width - visible_tiles_x))

        # Map viewport rendering: Loops only over the visible tile range
        # instead of the full map size
        for screen_y in range(visible_tiles_y):
            world_y = camera_y + screen_y
            if world_y >= map_height:
                break
    
            for screen_x in range(visible_tiles_x):
                world_x = camera_x + screen_x
                if world_x >= map_width:
                    break

                tile_type = tile_map_grid[world_y][world_x]

                if tile_type in TILE_LOOKUP:
                    lines, _ = TILE_LOOKUP[tile_type]
                    color = color_map[tile_type]

                    # Convert the grid into screen character cells
                    y_pos1 = screen_y * 2
                    y_pos2 = screen_y * 2 + 1
                    x_pos = screen_x * 4

                    # Guard to ensure drawing positions dont clip past the edges
                    if y_pos2 < max_y and x_pos + 3 < max_x:
                        stdscr.addstr(y_pos1, x_pos, lines[0], color)
                        stdscr.addstr(y_pos2, x_pos, lines[1], color)

        #Player co-ordinates
        player_screen_y = (player_y - camera_y) * 2
        player_screen_x = (player_x - camera_x) * 4

        if 0 <= player_screen_y < max_y and 0 <= player_screen_x + 3 < max_x:
            player_color = curses.color_pair(4)
            stdscr.addstr(player_screen_y, player_screen_x, "++++", player_color)
            stdscr.addstr(player_screen_y + 1, player_screen_x, "++++", player_color)

        stdscr.refresh()

        #Player movement
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == curses.KEY_UP and player_y > 0:
            player_y -= 1
        elif key == curses.KEY_DOWN and player_y < map_height - 1:
            player_y += 1
        elif key == curses.KEY_LEFT and player_x > 0:
            player_x -= 1
        elif key == curses.KEY_RIGHT and player_x < map_width - 1:
            player_x += 1

curses.wrapper(main)