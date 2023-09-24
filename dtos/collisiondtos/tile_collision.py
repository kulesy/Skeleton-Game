from enums.global_enums import CollisionEnum
from objects.tile import Tile

class TileCollision: 
    def __init__(self, tile: Tile, side: CollisionEnum):
      self.tile: Tile = tile
      self.side: CollisionEnum = side