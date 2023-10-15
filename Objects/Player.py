import math

import pygame
from consts.physicconsts import PhysicConsts
from enums.global_enums import *
from objects.arm import Arm
from objects.entities.entity import Entity
from objects.entities.hitbox import Hitbox
from objects.entities.movable import Movable
from objects.entities.sprite import Sprite
from objects.map import Map
from objects.opening_platforms import OpeningPlatforms

class Player:
    def __init__(self, map):
        self.entity = Entity()
        self.entity.x = 200
        self.entity.y = 130
        self.sprite = Sprite(self.entity , "player")
        self.hitbox = Hitbox(self.entity, 0, 0,
                             self.entity.width, self.entity.height)
        self.movable = Movable(self.hitbox)
        self.map: Map = map

        self.direction: DirectionEnum = DirectionEnum.NONE

        self.arm_offset = (4, 13)
        self.arm_left = Arm(map, self.entity)
        self.arm_right = Arm(map, self.entity)
        self.arm_max_distance: int = 6
        
        self.charge_timer: int = 100

        self.air_timer:int = 0
    
    def move(self, mouse_angle) -> None:
        collision_response = self.movable.move(self.map.blocks)

        if (collision_response.tile_collision_y != None and
            collision_response.tile_collision_y.side == CollisionEnum.TOP):
            self.air_timer = 0
            # collided_tile_key = f"{int(player_collision.position[0]/self.map.tile_size)};{int(player_collision.position[1]/self.map.tile_size)}"
            # if (collided_tile_key in self.map.disapearing_platforms):
            #     self.map.disapearing_platforms[collided_tile_key].is_disapearing = True

            # if (collided_tile_key in self.map.map_model.tiles and 
            #     self.map.map_model.tiles[collided_tile_key].tile_type_id == 5):
            #     self.friction = 0.04
            # else:
            #     self.friction = self.physics_constants.friction
        else:
            # self.friction = self.physics_constants.friction
            self.air_timer += 1

        self.check_arm_collisions(self.arm_left)
        self.check_arm_collisions(self.arm_right)

        self.update_direction(mouse_angle)

        self.connect_arms()

        return
    
    def check_arm_collisions(self, arm: Arm):
        if (arm.arm_state == ArmStateEnum.STUCK):
            arm_hitbox_rect = arm.hitbox.get_hitbox_rect()
            player_hitbox_rect = self.hitbox.get_hitbox_rect()
            arm_player_collision = arm_hitbox_rect.colliderect(player_hitbox_rect)
            if (arm_player_collision):
                arm.reset_arm()
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
        if (self.entity.is_flipped):
            x_offset += (self.entity.width / 2) - 1

        arm.entity.x = self.entity.x + x_offset
        arm.entity.y = self.entity.y + y_offset

    def render(self, display, scroll) -> None:
        if (self.entity.is_flipped):
            self.arm_left.render(display, scroll)
        else:
            self.arm_right.render(display, scroll)

        self.map.render_surface(self.sprite.current_frame, (self.entity.x, self.entity.y))
        
        if (self.entity.is_flipped):
            self.arm_right.render(display, scroll)
        else:
            self.arm_left.render(display, scroll)
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
            self.entity.is_flipped = False
        elif (self.movable.direction == DirectionEnum.LEFT):
            self.entity.is_flipped = True

        return
    
    def handle_charging_throw(self, display, scroll, 
                              is_charging_throw, mouse_angle, arm: Arm) -> None:
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

                self.render_arm_trajectory(display, scroll, arm)
            else:
                if (arm.charge > 0):
                    arm.charge -= 25
                    if (arm.charge <= 0):
                        arm.arm_state = ArmStateEnum.DETACHED
                        arm.charge = 0
        
        return

    def render_arm_trajectory(self, display, scroll, arm: Arm) -> None:
        if (arm.arm_state == ArmStateEnum.ATTACHED):
            arm_trajectory_velocity = arm.movable.velocity.copy()
            arm_trajectory_pos = [arm.entity.x, arm.entity.y]
            for i in range(20):
                trajectory_rect = pygame.Rect(arm_trajectory_pos[0] - scroll[0], arm_trajectory_pos[1]- scroll[1], 1, 1)
                arm_trajectory_pos[0] += arm_trajectory_velocity[0]
                arm_trajectory_pos[1] += arm_trajectory_velocity[1]
                arm_trajectory_velocity[1] += PhysicConsts.GRAVITY
                pygame.draw.rect(display, (255, 255, 255) , trajectory_rect)
        
        return