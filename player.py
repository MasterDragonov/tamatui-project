import curses

class Player:
    def __init__(self):
        self.player_y = 5
        self.player_x = 5

    def handle_movement(self, key, map_height, map_width):
        if key == curses.KEY_UP and self.player_y > 0:
            self.player_y -= 1
        elif key == curses.KEY_DOWN and self.player_y < map_height - 1:
            self.player_y += 1
        elif key == curses.KEY_LEFT and self.player_x > 0:
            self.player_x -= 1
        elif key == curses.KEY_RIGHT and self.player_x < map_width - 1:
            self.player_x += 1

    def draw(self, stdscr, camera_y, camera_x, max_y, max_x):
        player_screen_y = (self.player_y - camera_y) * 2
        player_screen_x = (self.player_x - camera_x) * 4

        if 0 <= player_screen_y < max_y and 0 <= player_screen_x + 3 < max_x:
            player_color = curses.color_pair(4)
            stdscr.addstr(player_screen_y, player_screen_x, "++++", player_color)
            stdscr.addstr(player_screen_y + 1, player_screen_x, "++++", player_color)
