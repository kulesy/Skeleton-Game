from typing import Optional
from dtos.collisiondtos.entity_collision import EntityCollision
from dtos.collisiondtos.tile_collision import HitboxCollision


class CollisionResponse: 
    def __init__(self):
        self.hitbox_collision_x: Optional[HitboxCollision] = None
        self.hitbox_collision_y: Optional[HitboxCollision] = None
