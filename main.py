TRANSITIONS = {
    "map1.txt": {
        (31,22): ("map2.txt", 35, 6) # (31,22) is the doorway to the cave in map1 and reappear at (35,6) of map2
    },
    "map2.txt": {
        (37,6): ("map1.txt", None, None)
    }
}

import curses
from game_map import GameMap
from player import Player
from camera import Camera
from encounter import check_encounter

class GameEngine:
    def __init__(self, tile_map_file):
        self.tile_map_file = tile_map_file
        self.game_map = GameMap(tile_map_file)
        self.game_map.transitions = TRANSITIONS[tile_map_file] # doorways located in each map that will trigger transitions
        self.player = Player()
        self.camera = Camera()

    def run(self, stdscr):
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_GREEN, -1)
        curses.init_pair(2, curses.COLOR_YELLOW, -1)
        curses.init_pair(3, curses.COLOR_BLUE, -1)
        curses.init_pair(4, curses.COLOR_RED, -1) 
        curses.init_pair(5, curses.COLOR_WHITE, -1) 

        color_map = {
            0: curses.color_pair(1),
            1: curses.color_pair(2),
            2: curses.color_pair(3),
            3: curses.color_pair(5),
            4: curses.color_pair(1),
            5: curses.color_pair(5)
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

            self.game_map.draw(
                stdscr, self.camera, visible_tiles_y, visible_tiles_x, 
                max_y, max_x, color_map
            )

            stdscr.noutrefresh()
            self.player.draw(stdscr, self.camera.camera_y, self.camera.camera_x, max_y, max_x)

            key = stdscr.getch()
            if key == ord('q'):
                break

            old_y =self.player.player_y
            old_x = self.player.player_x
    
            player_has_moved = self.player.handle_movement(key, self.game_map.tile_map_grid)

            if player_has_moved:
                transition = self.game_map.check_transition(self.player.player_y, self.player.player_x)
                if transition:
                    target_map = transition[0]
                    target_y = transition[1]
                    target_x = transition[2]

                    if target_y is None:
                        target_y = self.return_point[0]
                        target_x = self.return_point[1]
                    else:
                        self.return_point = (old_y, old_x)

                    self.game_map = GameMap(target_map)
                    self.game_map.transitions = TRANSITIONS[target_map]

                    self.player.player_y = target_y
                    self.player.player_x = target_x

                else:
                    player_will_encounter = check_encounter(self.game_map.tile_map_grid, self.player.player_y, self.player.player_x)
                    if player_will_encounter:
                        stdscr.addstr(0,0,"you have encountered a monster")
                        stdscr.getch()



if __name__ == "__main__":
    engine = GameEngine("map1.txt")
    curses.wrapper(engine.run)