class Tile(object):
    def __init__(self, x, y, tile_size, rect):
        self.x = x
        self.y = y
        self.tile_size = tile_size
        self.rect = rect
        self.rotation = 0
        self.friction = 0