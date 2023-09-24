from enums.global_enums import CollisionEnum
from objects.tile import Block

class TileCollision: 
    def __init__(self, tile: Block, side: CollisionEnum):
      self.tile: Block = tile
      self.side: CollisionEnum = side