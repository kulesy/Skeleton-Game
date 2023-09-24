from typing import Optional
from consts.physicconsts import PhysicConsts
from dtos.collisiondtos.tile_collision import TileCollision
from dtos.collisiondtos.collision_response import CollisionResponse
from enums.global_enums import CollisionEnum, DirectionEnum
from objects.entities.entity import Entity
from objects.entities.hitbox import Hitbox
from objects.block import Block

class Movable(object):
    def __init__(self, hitbox):
        self._hitbox: Hitbox = hitbox
        self.velocity = []
        self.direction = None

    def move(self, tiles: dict[str, Block]) -> CollisionResponse:
        collision_response = CollisionResponse()
        
        self._hitbox.entity.x += self.velocity[0]
        collided_tile = self.collision_test(list(tiles.values()))

        if (collided_tile != None):
            if self.velocity[0] > 0:
                self._hitbox.entity.x = collided_tile.rect.right + self._hitbox.width + self._hitbox.offset_x
                collision_response.tile_collision_x = TileCollision(collided_tile, CollisionEnum.RIGHT)
            elif self.velocity[0] < 0:
                self._hitbox.entity.x = collided_tile.rect.left - self._hitbox.width - self._hitbox.offset_x
                collision_response.tile_collision_x = TileCollision(collided_tile, CollisionEnum.LEFT)
            self.velocity[0] = 0

        self._hitbox.entity.y += self.velocity[1]
        collided_tile = self.collision_test(list(tiles.values()))

        if (collided_tile != None):
            if self.velocity[1] > 0:
                self._hitbox.entity.y = collided_tile.rect.top + self._hitbox.height + self._hitbox.offset_y
                collision_response.tile_collision_y = TileCollision(collided_tile, CollisionEnum.TOP)
            elif self.velocity[1] < 0:
                self._hitbox.entity.y = collided_tile.rect.bottom - self._hitbox.height - self._hitbox.offset_y
                collision_response.tile_collision_y = TileCollision(collided_tile, CollisionEnum.BOTTOM)
            self.velocity[1] = 0

        self.y = self._hitbox.entity.y

        self.apply_opposing_forces(collision_response.tile_collision_y)
        self.update_direction()

        return collision_response
    
    def apply_opposing_forces(self, tile_collision_y: Optional[TileCollision]) -> None:
        if (self.velocity[0] != 0 and tile_collision_y != None and tile_collision_y.side == CollisionEnum.TOP):
            if (self.direction == DirectionEnum.RIGHT):
                self.velocity[0] -= tile_collision_y.tile.friction
                if (self.velocity[0] < 0):
                    self.velocity[0] = 0
            elif (self.direction == DirectionEnum.LEFT):
                self.velocity[0] += tile_collision_y.tile.friction
                if (self.velocity[0] > 0):
                    self.velocity[0] = 0
        
        self.velocity[1] += PhysicConsts.GRAVITY
        if (self.velocity[1] > PhysicConsts.TERMINAL_VELOCITY):
            self.velocity[1] = PhysicConsts.TERMINAL_VELOCITY
    
    def update_direction(self):
        if (self.velocity[0] > 0):
            self.direction = DirectionEnum.RIGHT
        elif (self.velocity[0] < 0):
            self.direction = DirectionEnum.LEFT
        elif (self.velocity[0] == 0):
            self.direction = DirectionEnum.NONE

    def collision_test(self, tile_list: list[Block]):
        for tile in tile_list:
            if tile.rect.colliderect(self._hitbox.get_hitbox_rect()):
                return tile
        
        return None

