"""Explore: walk the hero around the overworld map."""
from camera import Camera
from encounter import check_encounter
from game_map import GameMap
from player import Player
from states.base import State

START_MAP = "map1.txt"

# Doorways in each map: (y, x) -> (target map, target y, target x).
# A target of None, None means "go back to where you came in".
TRANSITIONS = {
    "map1.txt": {
        (31, 22): ("map2.txt", 35, 6)  # cave doorway in map1
    },
    "map2.txt": {
        (37, 6): ("map1.txt", None, None)
    }
}


class ExploreState(State):
    """The hub state: the map, the camera and the walking hero."""

    def __init__(self, game):
        super().__init__(game)
        self.game_map = GameMap(START_MAP)
        self.game_map.transitions = TRANSITIONS[START_MAP]
        self.camera = Camera()
        self.player = Player()
        self.return_point = None
        self.message = ""

    def handle_key(self, key):
        self.message = ""
        if key == ord("q"):
            self.quit()  # later: open the pause menu instead
            return

        old_y = self.player.player_y
        old_x = self.player.player_x
        moved = self.player.handle_movement(key, self.game_map.tile_map_grid)
        if not moved:
            return

        transition = self.game_map.check_transition(self.player.player_y,
                                                    self.player.player_x)
        if transition:
            self.change_map(transition, old_y, old_x)
        elif check_encounter(self.game_map.tile_map_grid,
                             self.player.player_y, self.player.player_x):
            # Later: self.push(BattleState(...)) instead of a message.
            self.message = "You have encountered a monster!"

    def change_map(self, transition, old_y, old_x):
        """Load the target map and place the player at its doorway."""
        target_map, target_y, target_x = transition
        if target_y is None:
            target_y, target_x = self.return_point
        else:
            self.return_point = (old_y, old_x)

        self.game_map = GameMap(target_map)
        self.game_map.transitions = TRANSITIONS[target_map]
        self.player.player_y = target_y
        self.player.player_x = target_x

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
        if self.message:
            screen.addstr(0, 0, self.message[:max_x - 1])
