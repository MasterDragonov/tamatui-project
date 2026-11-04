class Camera:
    def __init__(self):
        self.camera_y = 0
        self.camera_x = 0

    def update(self, player_y, player_x, visible_tiles_y, visible_tiles_x, map_height, map_width):
        self.camera_y = player_y - (visible_tiles_y // 2)
        self.camera_x = player_x - (visible_tiles_x // 2)

        self.camera_y = max(0, min(self.camera_y, map_height - visible_tiles_y))
        self.camera_x = max(0, min(self.camera_x, map_width - visible_tiles_x))
