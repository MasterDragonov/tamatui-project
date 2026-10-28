import curses
from game_map import GameMap
from player import Player
from camera import Camera
from tile import Tile

class GameEngine:
    def __init__(self, tile_map_file):
        self.tile_map_file = tile_map_file
        self.game_map = GameMap(tile_map_file)
        self.player = Player()
        self.camera = Camera()

    def run(self, stdscr):
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_GREEN, -1)
        curses.init_pair(2, curses.COLOR_YELLOW, -1)
        curses.init_pair(3, curses.COLOR_BLUE, -1)
        curses.init_pair(4, curses.COLOR_RED, -1) 

        color_map = {
            0: curses.color_pair(1),
            1: curses.color_pair(2),
            2: curses.color_pair(3)
        }
        curses.curs_set(0)
        stdscr.keypad(True)

        while True:
            stdscr.clear()

            max_y, max_x = stdscr.getmaxyx()
            visible_tiles_y = max_y // 2
            visible_tiles_x = max_x // 4

            self.camera.update(
                self.player.player_y, self.player.player_x, 
                visible_tiles_y, visible_tiles_x, 
                self.game_map.map_height, self.game_map.map_width
            )

            for screen_y in range(visible_tiles_y):
                world_y = self.camera.camera_y + screen_y
                if world_y >= self.game_map.map_height:
                    break
        
                for screen_x in range(visible_tiles_x):
                    world_x = self.camera.camera_x + screen_x
                    if world_x >= self.game_map.map_width:
                        break

                    tile_type = self.game_map.tile_map_grid[world_y][world_x]
                    
                    tile = Tile(tile_type)
                    tile.draw(stdscr, screen_y, screen_x, max_y, max_x, color_map)

            stdscr.noutrefresh()
            self.player.draw(stdscr, self.camera.camera_y, self.camera.camera_x, max_y, max_x)

            key = stdscr.getch()
            if key == ord('q'):
                break
            
            self.player.handle_movement(key, self.game_map.map_height, self.game_map.map_width)

if __name__ == "__main__":
    engine = GameEngine("map1.txt")
    curses.wrapper(engine.run)