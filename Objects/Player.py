import math

import pygame
from consts.physicconsts import PhysicConsts
from dtos.collisiondtos.collision_response import CollisionResponse
from dtos.collisiondtos.tile_collision import HitboxCollision
from enums.global_enums import *
from objects.arm import Arm
from objects.entities.entity import Entity
from objects.entities.hitbox import Hitbox
from objects.entities.movable import Movable
from objects.entities.render import Render
from objects.entities.sprite import Sprite
from objects.map import Map
from objects.opening_platforms import OpeningPlatforms

class Player:
    def __init__(self, map):
        self.start_pos = (200, 100)
        self.entity = Entity()
        self.entity.x = self.start_pos[0]
        self.entity.y = self.start_pos[1]
        self.sprite = Sprite(self.entity, "player")
        self.hitbox = Hitbox(self.entity, 0, 0,
                             self.entity.width, self.entity.height)
        self.movable = Movable(self.hitbox, map)
        
        self.map: Map = map
        self.render = Render(self.map.tile_size, self.hitbox, self.sprite, 2, False)
        self.map.add_to_renders(self.render)

        self.direction: DirectionEnum = DirectionEnum.NONE

        self.arm_offset = (4, 13)
        self.arm_left = Arm(map, self.entity)
        self.arm_right = Arm(map, self.entity)
        self.arm_max_distance: int = 6
        
        self.charge_timer: int = 100

        self.air_timer:int = 0
    
    def move(self, mouse_angle) -> None:
        hitbox_collisions = self.movable.move()
        platform_collision = next((hitbox for hitbox in hitbox_collisions if hitbox.hitbox.entity.is_platform), None)

        if (platform_collision != None):
            if (platform_collision.side == CollisionEnum.TOP):
                self.air_timer = 0
                # collided_tile_key = f"{int(player_collision.position[0]/self.map.tile_size)};{int(player_collision.position[1]/self.map.tile_size)}"
                # if (collided_tile_key in self.map.disapearing_platforms):
                #     self.map.disapearing_platforms[collided_tile_key].is_disapearing = True

                # if (collided_tile_key in self.map.map_model.tiles and 
                #     self.map.map_model.tiles[collided_tile_key].tile_type_id == 5):
                #     self.friction = 0.04
                # else:
                #     self.friction = self.physics_constants.friction
                self.movable.opposing_force_x = 2
            else:
                # self.friction = self.physics_constants.friction
                self.air_timer += 1

        if (hitbox_collisions != None):
            self.check_arm_collisions(self.arm_left, hitbox_collisions)
            self.check_arm_collisions(self.arm_right, hitbox_collisions)

        self.update_direction(mouse_angle)

        self.connect_arms()

        return
    
    def check_arm_collisions(self, arm: Arm, hitbox_collisions: list[HitboxCollision]):
        if (arm.arm_state == ArmStateEnum.STUCK):
            for collision in hitbox_collisions:
                if (collision.hitbox.entity.id == arm.entity.id):
                    arm.reset_arm()
                    break
        else: 
            for opened_platform in arm.arm_opened_platforms:
                if (opened_platform.is_open):
                    opened_platform.is_closing = True

    def connect_arms(self):
        if (self.arm_left.arm_state == ArmStateEnum.ATTACHED):
            self.connect_arm_to_player(self.arm_left)
        
        if (self.arm_right.arm_state == ArmStateEnum.ATTACHED):
            self.connect_arm_to_player(self.arm_right)
            
    def connect_arm_to_player(self, arm : Arm):
        x_offset = self.arm_offset[0]
        y_offset = self.arm_offset[1]
        if (self.render.is_flipped):
            x_offset += (self.entity.width / 2)

        arm.entity.x = self.entity.x + x_offset
        arm.entity.y = self.entity.y + y_offset
        arm.hitbox.offset_x = 0
        arm.hitbox.offset_y = arm.entity.height//2

    def handle_render(self) -> None:
        if (self.render.is_flipped):
            self.arm_left.render.z_level = 1
            self.arm_right.render.z_level = 3
        else:
            self.arm_left.render.z_level = 3
            self.arm_right.render.z_level = 1

        self.arm_left.handle_render()
        self.arm_right.handle_render()
        return

    def jump(self) -> None:
        if self.air_timer < 6:
            self.movable.velocity[1] = -4

        return
    
    def update_direction(self, mouse_angle) -> None:
        # Flip the player towards the direction of the mouse cursor
        if (math.degrees(mouse_angle) > -90 and math.degrees(mouse_angle) < 90):
            self.movable.direction = DirectionEnum.RIGHT
        else:
            self.movable.direction = DirectionEnum.LEFT

        if (self.movable.direction == DirectionEnum.RIGHT):
            self.render.is_flipped = False
        elif (self.movable.direction == DirectionEnum.LEFT):
            self.render.is_flipped = True
        
        self.arm_left.flip_arm(self.movable.direction)
        self.arm_right.flip_arm(self.movable.direction)

        return
    
    def handle_charging_throw(self, is_charging_throw, mouse_angle, arm: Arm) -> None:
        if (self.air_timer > 0):
            arm.charge = 0
            return
        
        if (arm.arm_state == ArmStateEnum.ATTACHED):
            if (is_charging_throw):
                velocity_x = math.cos(mouse_angle) * self.arm_max_distance
                velocity_y = math.sin(mouse_angle) * self.arm_max_distance
                arm.movable.velocity[0] = velocity_x  * (arm.charge/100)
                arm.movable.velocity[1] = velocity_y  * (arm.charge/100)
                if (arm.charge <= 100):
                    arm.charge += 2.5

                self.render_arm_trajectory(arm)
            else:
                if (arm.charge > 0):
                    arm.charge -= 25
                    if (arm.charge <= 0):
                        arm.arm_state = ArmStateEnum.DETACHED
                        arm.render.is_anchored = False
                        arm.charge = 0
        
        return

    def render_arm_trajectory(self, arm: Arm) -> None:
        if (arm.arm_state == ArmStateEnum.ATTACHED):
            arm_trajectory_velocity = arm.movable.velocity.copy()
            arm_trajectory_pos = [arm.entity.x, arm.entity.y]
            for i in range(20):
                arm_map_pos = self.map.get_map_position(arm_trajectory_pos)
                trajectory_rect = pygame.Rect(arm_map_pos[0], arm_map_pos[1], 1, 1)
                arm_trajectory_pos[0] += arm_trajectory_velocity[0]
                arm_trajectory_pos[1] += arm_trajectory_velocity[1]
                arm_trajectory_velocity[1] += PhysicConsts.GRAVITY
                pygame.draw.rect(self.map.display, (255, 255, 255) , trajectory_rect)
        
        return
    
    def reset_player(self):
        self.entity.x = self.start_pos[0]
        self.entity.y = self.start_pos[1]
        self.arm_left.reset_arm()
        self.arm_right.reset_arm()