import math

import pygame
from Enums.ArmState import ArmState
from Enums.Collision import *
from Enums.Direction import Direction 
import scripts.engine as e

class Player:
    def __init__(self, entity, friction, gravity, terminal_velocity):
        self.velocity = [0, 0]
        self.entity : e.entity = entity
        self.arm = e.entity(entity.x + 3, entity.y + 15, 4, 4, "arm")
        self.arm_flip = False
        self.arm_angle = 0
        self.arm_velocity = [0, 0]
        self.arm_max_distance = 6
        self.arm_image = pygame.image.load('animations/arm/idle/idle-1.png').convert()
        self.arm_image.set_colorkey((0,0,0))
        self.arm_state = ArmState.ATTACHED
        self.direction = Direction.NONE
        self.charge = 0
        self.charge_timer = 100
        self.friction = friction
        self.gravity = gravity
        self.terminal_velocity = terminal_velocity
        self.air_timer = 0

    def jump(self):
        if self.air_timer < 6:
            self.velocity[1] = -4
    
    def handle_charging_throw(self, display, scroll, is_charging_throw, mouse_angle):
        if (self.air_timer > 0):
            self.charge = 0
            return
        
        if (self.arm_state == ArmState.ATTACHED):
            if (is_charging_throw):
                velocity_x = math.cos(mouse_angle) * self.arm_max_distance
                velocity_y = math.sin(mouse_angle) * self.arm_max_distance
                self.arm_velocity[0] = velocity_x  * (self.charge/100)
                self.arm_velocity[1] = velocity_y  * (self.charge/100)
                if (self.charge <= 100):
                    self.charge += 2.5

                self.render_arm_trajectory(display, scroll)
            else:
                if (self.charge > 0):
                    self.charge -= 25
                    if (self.charge <= 0):
                        self.arm_state = ArmState.DETACHED
                        self.charge = 0
        

    def update_direction(self, mouse_angle):
        # Flip the player towards the direction of the mouse cursor
        if (math.degrees(mouse_angle) > -90 and math.degrees(mouse_angle) < 90):
            self.entity.flip = False
        else:
            self.entity.flip = True

        if (self.velocity[0] > 0):
            self.direction = Direction.RIGHT
            self.entity.set_flip(False)
            self.entity.set_action("run")
            self.entity.flip = False
        elif (self.velocity[0] < 0):
            self.direction = Direction.LEFT
            self.entity.set_flip(True)
            self.entity.set_action("run")
            self.entity.flip = True
        elif (self.velocity[0] == 0):
            self.direction = Direction.NONE
            self.entity.set_action("idle")

    def apply_opposing_forces(self):
        if (self.velocity[0] != 0):
            if (self.direction == Direction.RIGHT):
                self.velocity[0] -= self.friction
                if (self.velocity[0] < 0):
                    self.velocity[0] = 0
            elif (self.direction == Direction.LEFT):
                self.velocity[0] += self.friction
                if (self.velocity[0] > 0):
                    self.velocity[0] = 0
        
        self.velocity[1] += self.gravity
        if (self.velocity[1] > self.terminal_velocity):
            self.velocity[1] = self.terminal_velocity

    def update_arm_state(self, mouse_angle):
        arm_display_angle = mouse_angle - (math.pi/2)
        # Attached to player
        if (self.arm_state == ArmState.ATTACHED):
            self.arm_angle = math.degrees(arm_display_angle)
            if (self.arm_flip):
                self.arm_angle += self.charge
            if (self.arm_flip == False):
                self.arm_angle -= self.charge
                self.arm_angle = -self.arm_angle
        # Thrown by player
        elif (self.arm_state == ArmState.DETACHED):
            self.arm_angle -= 20
        # Stuck in wall
        elif (self.arm_state == ArmState.STUCK):
            self.arm_velocity = [0, 0]             
    
    def reset_arm(self):
        self.arm = e.entity(self.entity.x + 3, self.entity.y + 15, 4, 4, "arm")
        self.arm_flip = False
        self.arm_angle = 0
        self.arm_velocity = [0, 0]
        self.arm_state = ArmState.ATTACHED
        self.charge = 0
    
    def move(self, map_tile_rects, mouse_angle):
        self.apply_opposing_forces()
        self.update_direction(mouse_angle)
        
        player_pos_before = [self.entity.x, self.entity.y].copy()
        player_collisions = self.entity.move(self.velocity, map_tile_rects)
        if (self.arm_state == ArmState.ATTACHED):
            player_pos_dif = (self.entity.x - player_pos_before[0], self.entity.y - player_pos_before[1])
            self.arm.x += player_pos_dif[0]
            self.arm.y += player_pos_dif[1]
            self.arm.obj.rect.x += player_pos_dif[0]
            self.arm.obj.rect.y = self.arm.y
            if (self.arm_flip != self.entity.flip):
                self.arm_flip = self.entity.flip
                if (self.entity.flip == True):
                    self.arm.x += 9
                    self.arm.obj.rect.x = self.arm.x - self.arm.size_x
                elif (self.entity.flip == False):
                    self.arm.x -= 9
                    self.arm.obj.rect.x = self.arm.x
        elif (self.arm_state == ArmState.DETACHED):
            arm_tiles_collision = self.move_arm(map_tile_rects)
            self.arm_velocity[1] += self.gravity

            if (arm_tiles_collision != Collision.NONE):
                self.arm_state = ArmState.STUCK

                if (self.arm_velocity[0] < 0):
                    self.arm_flip = True
                if (self.arm_velocity[0] > 0):
                    self.arm_flip = False

                if (arm_tiles_collision == Collision.LEFT or arm_tiles_collision == Collision.RIGHT): 
                    self.arm_angle = 90
                elif (arm_tiles_collision == Collision.TOP): 
                    self.arm_angle = 180
                elif (arm_tiles_collision == Collision.BOTTOM): 
                    self.arm_angle = 0
                    
                self.arm_velocity[0] = 0
                self.arm_velocity[1] = 0
        elif (self.arm_state == ArmState.STUCK):
            arm_player_collision = self.arm.obj.rect.colliderect(self.entity.obj.rect)
            if (arm_player_collision):
                self.velocity[1] = -6
                self.reset_arm()

        if player_collisions['top']:
            self.velocity[1] = 0

        if player_collisions['bottom']:
            self.air_timer = 0
        else:
            self.air_timer += 1
    
    def render(self, display, scroll):
        self.entity.change_frame(1)
        self.entity.display(display, scroll)
        player_arm_image_copy = pygame.transform.rotate(self.arm_image, self.arm_angle)
        player_arm_image_loc = [round(self.arm.x) - int(player_arm_image_copy.get_width() / 2), self.arm.y - int(player_arm_image_copy.get_height() / 2)]
        display.blit(pygame.transform.flip(player_arm_image_copy, self.arm_flip, False), (player_arm_image_loc[0]- scroll[0], player_arm_image_loc[1] - scroll[1]))
    
    def move_arm(self, tiles):
        self.arm.x += self.arm_velocity[0]
        self.arm.obj.rect.x = round(self.arm.x)
        block_collisions = e.collision_test(self.arm.obj.rect, tiles)
        for block in block_collisions:
            if (self.arm_velocity[0] > 0):
                self.arm.x = block.left - 6
                self.arm.y = block.top + 8
                self.arm.obj.rect.x = self.arm.x - self.arm.size_x / 2
                self.arm.obj.rect.y = self.arm.y
                return Collision.LEFT
            elif (self.arm_velocity[0] < 0):
                self.arm.x = block.right + 6
                self.arm.y = block.top + 8
                self.arm.obj.rect.x = self.arm.x - self.arm.size_x / 2
                self.arm.obj.rect.y = self.arm.y
                return Collision.RIGHT
            
        self.arm.y += self.arm_velocity[1]
        self.arm.obj.rect.y = round(self.arm.y)
        block_collisions = e.collision_test(self.arm.obj.rect, tiles)
        for block in block_collisions:
            if (self.arm_velocity[1] < 0):
                self.arm.y = block.bottom + self.arm.size_x / 2
                self.arm.x = block.left + 8
                self.arm.obj.rect.x = self.arm.x
                self.arm.obj.rect.y = self.arm.y
                return Collision.TOP
            elif (self.arm_velocity[1] > 0):
                self.arm.y = block.top - self.arm.size_x / 2
                self.arm.x = block.left + 8
                self.arm.obj.rect.x = self.arm.x
                self.arm.obj.rect.y = self.arm.y
                return Collision.BOTTOM
        
        return Collision.NONE

    def render_arm_trajectory(self, display, scroll):
        if (self.arm_state == ArmState.ATTACHED):
            arm_trajectory_velocity = self.arm_velocity.copy()
            arm_trajectory_pos = [self.arm.x, self.arm.y]
            for i in range(20):
                trajectory_rect = pygame.Rect(arm_trajectory_pos[0] - scroll[0], arm_trajectory_pos[1]- scroll[1], 1, 1)
                arm_trajectory_pos[0] += arm_trajectory_velocity[0]
                arm_trajectory_pos[1] += arm_trajectory_velocity[1]
                arm_trajectory_velocity[1] += self.gravity
                pygame.draw.rect(display, (255, 255, 255) , trajectory_rect)