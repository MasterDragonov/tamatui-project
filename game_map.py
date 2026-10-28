import os

class GameMap:
    def __init__(self, tile_map_file):
        self.tile_map_grid = self.load_map(tile_map_file)
        self.map_height = len(self.tile_map_grid)
        self.map_width = len(self.tile_map_grid[0]) if self.map_height > 0 else 0

    def load_map(self, filename):
        """Reads a text file to convert it into a 2D matrix.
        
        This function strips spaces/commas to parse values into integers
        for a tile map lookup table.
        
        Args:
            filename (str): Filename of the textfile to be loaded.
            
        Returns:
            list of list of int: 2D list array where grid[y][x] contains an integer.
        """
        
        grid = []
        with open(filename, "r") as f:
            for line in f:
                cleaned_line = line.strip().replace(",", " ")
                if cleaned_line:
                    grid.append([int(tile) for tile in cleaned_line.split()])
        return grid
