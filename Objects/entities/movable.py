from typing import Optional
import pygame
from consts.physicconsts import PhysicConsts
from dtos.collisiondtos.tile_collision import TileCollision
from dtos.collisiondtos.collision_response import CollisionResponse
from enums.global_enums import CollisionEnum, DirectionEnum
from objects.entities.entity import Entity
from objects.tile import Tile

class Movable(object):
    def __init__(self, entity:Entity):
        self._entity:Entity = entity
        self.velocity = []
        self.direction = None

    def move(self, tiles: dict[str, Tile]) -> CollisionResponse:
        collision_response = CollisionResponse()

        self.x += self.velocity[0]
        self._entity.rect.x = int(round(self.x))
        collided_tile = self.collision_test(tiles.values())

        if (collided_tile != None):
            collision_response.
            if self.velocity[0] > 0:
                self._entity.rect.right = collided_tile.rect.left
                collision_response.tile_collision_x = TileCollision(collided_tile, CollisionEnum.RIGHT)
            elif self.velocity[0] < 0:
                self._entity.rect.left = collided_tile.rect.right
                collision_response.tile_collision_x = TileCollision(collided_tile, CollisionEnum.LEFT)
        
        self.x = self._entity.rect.x

        self.y += self.velocity[1]
        self._entity.rect.y = int(round(self.y))
        collided_tile = self.collision_test(tiles.values())

        if (collided_tile != None):
            if self.velocity[1] > 0:
                self._entity.rect.bottom = collided_tile.rect.top
                self.velocity[1] = 0
                collision_response.tile_collision_y = TileCollision(collided_tile, CollisionEnum.TOP)
            elif self.velocity[1] < 0:
                self._entity.rect.top = collided_tile.rect.bottom
                self.velocity[1] = 0
                collision_response.tile_collision_y = TileCollision(collided_tile, CollisionEnum.BOTTOM)

        self.y = self._entity.rect.y

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

    def collision_test(self, tile_list):
        for tile in tile_list:
            if tile.colliderect(self._entity.rect):
                return tile
        
        return None
