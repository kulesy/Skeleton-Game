from typing import Optional
from dtos.collisiondtos.entity_collision import EntityCollision
from dtos.collisiondtos.tile_collision import TileCollision


class CollisionResponse: 
    def __init__(self):
        self.tile_collision_x: Optional[TileCollision] = None
        self.tile_collision_y: Optional[TileCollision] = None
        self.entity_collisions: list[EntityCollision] = []
