import curses
from collision import is_walkable

class Player:
    def __init__(self):
        self.player_y = 5
        self.player_x = 5

    def handle_movement(self, key, tile_map_grid):

        new_y = self.player_y
        new_x = self.player_x

        if key == curses.KEY_UP:
            new_y -= 1
        elif key == curses.KEY_DOWN:
            new_y += 1
        elif key == curses.KEY_LEFT:
            new_x -= 1
        elif key == curses.KEY_RIGHT:
            new_x += 1
        else:
            return False

        can_move = is_walkable(tile_map_grid, new_y, new_x)
        
        if can_move:
            self.player_y = new_y
            self.player_x = new_x
            return True
        else:
            return False

    def draw(self, stdscr, camera_y, camera_x, max_y, max_x):
        player_screen_y = (self.player_y - camera_y) * 2
        player_screen_x = (self.player_x - camera_x) * 4

        if 0 <= player_screen_y < max_y and 0 <= player_screen_x + 3 < max_x:
            player_color = curses.color_pair(4)
            stdscr.addstr(player_screen_y, player_screen_x, "++++", player_color)
            stdscr.addstr(player_screen_y + 1, player_screen_x, "++++", player_color)
