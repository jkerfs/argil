
class Grid:
    def __init__(self, tiles):
        self.tiles = tiles

    def draw(self, surface):
        for tile in self.tiles:
            surface.fill((0, 255, 0), tile)