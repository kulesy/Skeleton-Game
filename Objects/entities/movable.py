from typing import Optional
from consts.physicconsts import PhysicConsts
from dtos.collisiondtos.tile_collision import HitboxCollision
from dtos.collisiondtos.collision_response import CollisionResponse
from enums.global_enums import AxisEnum, CollisionEnum, DirectionEnum
from objects.entities.entity import Entity
from objects.entities.hitbox import Hitbox
from objects.block import Platform
from objects.map import Map

class Movable(object):
    def __init__(self, hitbox: Hitbox, map: Map):
        self._map: Map = map
        self._hitbox: Hitbox = hitbox
        self.velocity: list[float] = [0,0]
        self.direction = None
        self.opposing_force_x = 0

    def move(self) -> list[HitboxCollision]:
        self._hitbox.entity.x += self.velocity[0]

        hitbox_collisions_x: list[HitboxCollision] = self.collision_handler(AxisEnum.X)

        self.update_direction()

        platform_x_collision = next((collision for collision in hitbox_collisions_x if collision.hitbox.entity.is_platform), None)
        self.apply_opposing_forces_x(platform_x_collision)

        self._hitbox.entity.y += self.velocity[1]

        hitbox_collisions_y: list[HitboxCollision] = self.collision_handler(AxisEnum.Y)
            
        platform_y_collision = next((collision for collision in hitbox_collisions_y if collision.hitbox.entity.is_platform), None)
        self.apply_opposing_forces_y(platform_y_collision)

        return hitbox_collisions_x + hitbox_collisions_y
    
    def apply_opposing_forces_x(self, platform_collision_x: Optional[HitboxCollision]) -> None:
        if (platform_collision_x != None):
            if (platform_collision_x.side == CollisionEnum.LEFT):
                self._hitbox.entity.x = platform_collision_x.hitbox.get_hitbox_rect().left - self._hitbox.width - self._hitbox.offset_x
            elif (platform_collision_x.side == CollisionEnum.RIGHT):
                self._hitbox.entity.x = platform_collision_x.hitbox.get_hitbox_rect().right - self._hitbox.offset_x

        # Opposing forces x
        if (self.velocity[0] != 0):
            if (self.direction == DirectionEnum.RIGHT):
                self.velocity[0] -= self.opposing_force_x
                if (self.velocity[0] <= 0):
                    self.velocity[0] = 0
            if (self.direction == DirectionEnum.LEFT):
                self.velocity[0] += self.opposing_force_x
                if (self.velocity[0] >= 0):
                    self.velocity[0] = 0

    def apply_opposing_forces_y(self, platform_collision_y: Optional[HitboxCollision]) -> None:
        if (platform_collision_y != None):
            if platform_collision_y.side == CollisionEnum.TOP:
                self._hitbox.entity.y = platform_collision_y.hitbox.get_hitbox_rect().top - self._hitbox.height - self._hitbox.offset_y
            elif platform_collision_y.side == CollisionEnum.BOTTOM:
                self._hitbox.entity.y = platform_collision_y.hitbox.get_hitbox_rect().bottom - self._hitbox.offset_y
                self.velocity[1] = 0
        
        # Opposing forces y
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

    def collision_handler(self, axis):
        hitbox_collisions = []

        for render in self._map.get_renders():
            if (render.hitbox.get_hitbox_rect().colliderect(self._hitbox.get_hitbox_rect()) and
                render.hitbox.entity.id != self._hitbox.entity.id):
                if (axis == AxisEnum.X and (self._hitbox.entity.x <= render.hitbox.entity.x)):
                    hitbox_collisions.append(HitboxCollision(render.hitbox, CollisionEnum.LEFT))
                elif (axis == AxisEnum.X and (self._hitbox.entity.x >= render.hitbox.entity.x)):
                    hitbox_collisions.append(HitboxCollision(render.hitbox, CollisionEnum.RIGHT))
                elif (axis == AxisEnum.Y and (self._hitbox.entity.y <= render.hitbox.entity.y)):
                    hitbox_collisions.append(HitboxCollision(render.hitbox, CollisionEnum.TOP))
                elif (axis == AxisEnum.Y and (self._hitbox.entity.y >= render.hitbox.entity.y)):
                    hitbox_collisions.append(HitboxCollision(render.hitbox, CollisionEnum.BOTTOM))
        
        return hitbox_collisions