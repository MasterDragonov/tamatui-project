import os
from tile import Tile

class GameMap:
    ASSETS_DIR = "assets"

    def __init__(self, tile_map_file):
        self.filename = tile_map_file
        self.tile_map_grid = self.load_map(tile_map_file)
        self.map_height = len(self.tile_map_grid)
        self.map_width = len(self.tile_map_grid[0]) if self.map_height > 0 else 0
        self.tile_cache = {t_type: Tile(t_type) for t_type in Tile.TILE_LOOKUP.keys()}
        self.transitions = {}

    def load_map(self, filename):
        """Reads a text file to convert it into a 2D matrix.
        
        This function strips spaces/commas to parse values into integers
        for a tile map lookup table.
        
        Args:
            filename (str): Filename of the textfile to be loaded.
            
        Returns:
            list of list of int: 2D list array where grid[y][x] contains an integer.
        """

        full_path = os.path.join(self.ASSETS_DIR, filename)

        grid = []
        with open(full_path, "r") as f:
            for line in f:
                cleaned_line = line.strip().replace(",", " ")
                if cleaned_line:
                    grid.append([int(tile) for tile in cleaned_line.split()])
        return grid

    def check_transition(self, y, x):
        return self.transitions.get((y, x))

    def draw(self, stdscr, camera, visible_tiles_y, visible_tiles_x, max_y, max_x, color_map):
        """Iterates over the visible viewport and renders tiles."""
        for screen_y in range(visible_tiles_y):
            world_y = camera.camera_y + screen_y
            if world_y >= self.map_height:
                break
    
            for screen_x in range(visible_tiles_x):
                world_x = camera.camera_x + screen_x
                if world_x >= self.map_width:
                    break

                tile_type = self.tile_map_grid[world_y][world_x]
                
                tile = Tile(tile_type)
                tile.draw(stdscr, screen_y, screen_x, max_y, max_x, color_map)
