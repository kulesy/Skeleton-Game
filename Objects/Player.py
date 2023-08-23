import math

import pygame
from enums.global_enums import *
from objects.entity import Entity
from objects.map import Map
from objects.models.map.tile_model import TileModel
from objects.platform import Platform

class Player(Entity):
    def __init__(self, spawn_point, map):
        self.map: Map = map
        self.player_image: pygame.Surface = pygame.image.load('assets/animations/player/idle/0.png').convert()
        super().__init__(spawn_point[0] * 16, spawn_point[1] * 16  - (self.player_image.get_height()/2),
                         self.player_image.get_width(), self.player_image.get_height(), self.player_image, "player", True)

        self.direction: DirectionEnum = DirectionEnum.NONE
        self.player_image.set_colorkey((0,0,0))

        self.arm_offset: tuple[int, int] = (5, 13) 
        self.arm_image: pygame.Surface = pygame.image.load('assets/animations/arm/idle/0.png').convert()
        self.arm: Entity = Entity(self.x + self.arm_offset[0], self.y + self.arm_offset[1],
                                   4, 4, self.arm_image, "arm", False)
        self.arm_angle: float = 0
        self.arm_max_distance: int = 6
        self.arm_image.set_colorkey((0,0,0))
        self.arm_state: ArmStateEnum = ArmStateEnum.ATTACHED
        self.arm_opened_platform: Platform = Platform() 
        
        self.charge: float = 0
        self.charge_timer: int = 100

        self.air_timer:int = 0
    
    def move(self, map_tile_rects) -> None:
        self.apply_opposing_forces()
        
        player_collision = super().move(map_tile_rects)
        if (player_collision.has_collided and 
            player_collision.direction == CollisionEnum.BOTTOM):
            self.velocity[1] = 0

        if (player_collision.has_collided and 
            player_collision.direction == CollisionEnum.TOP):
            self.air_timer = 0
        else:
            self.air_timer += 1

        return
    
    def move_arm(self, map_tile_rects, mouse_angle) -> None:
        self.update_direction(mouse_angle)
        if (self.arm_state == ArmStateEnum.ATTACHED):
            self.connect_arm()
            if (self.arm.flip != self.flip):
                self.arm.flip = self.flip
                if (self.flip == True):
                    self.arm.x += self.width - self.arm_offset[0] - self.arm_image.get_width()
                    self.arm.rect.x = self.arm.x - self.arm.width
                elif (self.flip == False):
                    self.arm.x -= self.width - self.arm_offset[0] - self.arm_image.get_width()
                    self.arm.rect.x = self.arm.x
        elif (self.arm_state == ArmStateEnum.DETACHED):
            arm_tiles_collision = self.arm.move(map_tile_rects)
            self.arm.velocity[1] += self.gravity

            if (arm_tiles_collision.has_collided):
                self.arm_state = ArmStateEnum.STUCK

                if (arm_tiles_collision.has_collided):

                    if (arm_tiles_collision.direction == CollisionEnum.LEFT): 
                        self.arm.x += self.arm.rect.width
                        self.arm.x -= (self.arm_image.get_height() / 4)
                        self.arm_angle = 90
                    elif (arm_tiles_collision.direction == CollisionEnum.RIGHT):
                        self.arm.x += (self.arm_image.get_height() / 4)
                        self.arm_angle = 90
                    elif (arm_tiles_collision.direction == CollisionEnum.TOP): 
                        self.arm.y += (self.arm_image.get_height() / 4)
                        self.arm_angle = 0
                    elif (arm_tiles_collision.direction == CollisionEnum.BOTTOM): 
                        self.arm.y += self.arm.rect.height
                        self.arm.y -= (self.arm_image.get_height() / 4)
                        self.arm_angle = 180

                    collided_tile_key = f"{int(arm_tiles_collision.position[0]/self.map.tile_size)};{int(arm_tiles_collision.position[1]/self.map.tile_size)}"
                    if (collided_tile_key in self.map.map_model.tiles):
                        collided_tile = self.map.map_model.tiles[collided_tile_key]
                        if (collided_tile.linked_tile_key != ""):
                            self.arm_opened_platform = self.map.platforms[collided_tile.linked_tile_key]
                            self.arm_opened_platform.is_open = True
                    
                self.arm.velocity[0] = 0
                self.arm.velocity[1] = 0
        elif (self.arm_state == ArmStateEnum.STUCK):
            arm_player_collision = self.arm.rect.colliderect(self.rect)
            if (arm_player_collision):
                self.arm_opened_platform.is_closing = True
                self.velocity[1] = -6
                self.reset_arm()

        return
    
    def connect_arm(self):
        x_offset = 4
        y_offset = 13
        if (self.arm.flip):
            x_offset += (self.width / 2) - 1

        self.arm.x = self.x + x_offset
        self.arm.y = self.y + y_offset
        self.arm.rect.x = self.x + x_offset - 2
        self.arm.rect.y = self.y + y_offset
    
    def render(self, display, scroll) -> None:
        super().render(display, scroll)
        arm_surface = self.arm_image
        player_arm_image_loc = [self.arm.x, self.arm.y]
        
        if (self.arm_state != ArmStateEnum.STUCK):
            arm_surface = pygame.Surface((self.arm_image.get_width() * 2, self.arm_image.get_height() * 2))
            arm_surface.set_colorkey((0, 0, 0))
            arm_surface.blit(self.arm_image, (0, self.arm_image.get_height()))

        arm_surface = pygame.transform.flip(pygame.transform.rotate(arm_surface, self.arm_angle), self.arm.flip, False)
        player_arm_image_loc = [round(self.arm.x) - int(arm_surface.get_width() / 2), self.arm.y - int(arm_surface.get_height() / 2)]
        
        display.blit(arm_surface, (player_arm_image_loc[0]- scroll[0], player_arm_image_loc[1] - scroll[1]))
        return

    def jump(self) -> None:
        if self.air_timer < 6:
            self.velocity[1] = -4

        return
    
    def handle_charging_throw(self, display, scroll, 
                              is_charging_throw, mouse_angle) -> None:
        if (self.air_timer > 0):
            self.charge = 0
            return
        
        if (self.arm_state == ArmStateEnum.ATTACHED):
            if (is_charging_throw):
                velocity_x = math.cos(mouse_angle) * self.arm_max_distance
                velocity_y = math.sin(mouse_angle) * self.arm_max_distance
                self.arm.velocity[0] = velocity_x  * (self.charge/100)
                self.arm.velocity[1] = velocity_y  * (self.charge/100)
                if (self.charge <= 100):
                    self.charge += 2.5

                self.render_arm_trajectory(display, scroll)
            else:
                if (self.charge > 0):
                    self.charge -= 25
                    if (self.charge <= 0):
                        self.arm_state = ArmStateEnum.DETACHED
                        self.charge = 0
        
        return

    def update_direction(self, mouse_angle) -> None:
        # Flip the player towards the direction of the mouse cursor
        if (math.degrees(mouse_angle) > -90 and math.degrees(mouse_angle) < 90):
            self.flip = False
        else:
            self.flip = True
        
        super().update_direction()
        return

    def apply_opposing_forces(self) -> None:
        if (self.velocity[0] != 0):
            if (self.direction == DirectionEnum.RIGHT):
                self.velocity[0] -= self.friction
                if (self.velocity[0] < 0):
                    self.velocity[0] = 0
            elif (self.direction == DirectionEnum.LEFT):
                self.velocity[0] += self.friction
                if (self.velocity[0] > 0):
                    self.velocity[0] = 0
        
        self.velocity[1] += self.gravity
        if (self.velocity[1] > self.terminal_velocity):
            self.velocity[1] = self.terminal_velocity

        return

    def update_arm_state(self, mouse_angle) -> None:
        arm_display_angle = mouse_angle - (math.pi/2)
        # Attached to player
        if (self.arm_state == ArmStateEnum.ATTACHED):
            self.arm_angle = math.degrees(arm_display_angle)
            if (self.arm.flip):
                self.arm_angle += self.charge
            if (self.arm.flip == False):
                self.arm_angle -= self.charge
                self.arm_angle = -self.arm_angle
        # Thrown by player
        elif (self.arm_state == ArmStateEnum.DETACHED):
            self.arm_angle -= 20
        # Stuck in wall
        elif (self.arm_state == ArmStateEnum.STUCK):
            self.arm.velocity = [0, 0]        
                 
        return
    
    def reset_arm(self) -> None:
        self.arm = Entity(self.x + 3, self.y + 15, 4, 4, self.arm_image, "arm", False)
        self.arm.flip = False
        self.arm_angle = 0
        self.arm.velocity = [0, 0]
        self.arm_state = ArmStateEnum.ATTACHED
        self.charge = 0
        return

    def render_arm_trajectory(self, display, scroll) -> None:
        if (self.arm_state == ArmStateEnum.ATTACHED):
            arm_trajectory_velocity = self.arm.velocity.copy()
            arm_trajectory_pos = [self.arm.x, self.arm.y]
            for i in range(20):
                trajectory_rect = pygame.Rect(arm_trajectory_pos[0] - scroll[0], arm_trajectory_pos[1]- scroll[1], 1, 1)
                arm_trajectory_pos[0] += arm_trajectory_velocity[0]
                arm_trajectory_pos[1] += arm_trajectory_velocity[1]
                arm_trajectory_velocity[1] += self.gravity
                pygame.draw.rect(display, (255, 255, 255) , trajectory_rect)
        
        return