"""Explore: walk the hero around the overworld map."""
from camera import Camera
from game_map import GameMap
from player import Player
from states.base import State

START_MAP = "map1.txt"


class ExploreState(State):
    """The hub state: the map, the camera and the walking hero."""

    def __init__(self, game):
        super().__init__(game)
        self.game_map = GameMap(START_MAP)
        self.camera = Camera()
        self.player = Player()

    def handle_key(self, key):
        if key == ord("q"):
            self.quit()  # later: open the pause menu instead
        else:
            self.player.handle_movement(key, self.game_map.tile_map_grid)

    def draw(self, screen):
        max_y, max_x = screen.getmaxyx()
        visible_tiles_y = (max_y - 1) // 2
        visible_tiles_x = max_x // 4

        self.camera.update(self.player.player_y, self.player.player_x,
                           visible_tiles_y, visible_tiles_x,
                           self.game_map.map_height,
                           self.game_map.map_width)
        self.game_map.draw(screen, self.camera,
                           visible_tiles_y, visible_tiles_x,
                           max_y, max_x, self.game.color_map)
        self.player.draw(screen, self.camera.camera_y,
                         self.camera.camera_x, max_y, max_x)
