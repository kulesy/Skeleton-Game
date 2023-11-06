from enums.global_enums import CollisionEnum
from objects.entities.hitbox import Hitbox

class HitboxCollision: 
    def __init__(self, tile: Hitbox, side: CollisionEnum):
      self.hitbox: Hitbox = tile
      self.side: CollisionEnum = side