import math
import pygame
from enums.global_enums import ArmStateEnum, CollisionEnum
from objects.entities.entity import Entity
from objects.entities.hitbox import Hitbox
from objects.entities.movable import Movable
from objects.entities.static import StaticImage
from objects.map import Map
from objects.opening_platforms import OpeningPlatforms

class Arm():
    def __init__(self, map, player_entity):
        self.map: Map = map
        self.entity = Entity()
        self.entity.x = player_entity.x
        self.entity.y = player_entity.y
        self.static_image = StaticImage(self.entity, pygame.image.load('assets/animations/arm/idle/0.png'))
        hitbox_width = 2
        hitbox_height = 2
        self.hitbox = Hitbox(self.entity, 
                             self.entity.width/2 - hitbox_width/2,
                             self.entity.width/2 - hitbox_height/2,
                             hitbox_width, hitbox_height)
        
        self.movable = Movable(self.hitbox)

        self.arm_angle: float = 0
        self.arm_max_distance: int = 6
        self.arm_state: ArmStateEnum = ArmStateEnum.ATTACHED
        self.arm_opened_platforms: list[OpeningPlatforms] = [] 
        self.charge: float = 0
        self.arm_stuck_timer: float = 0

        
    def move_arm(self, map_tile_rects) -> None:
        if (self.arm_state != ArmStateEnum.DETACHED):
            return

        collision_response = self.movable.move(map_tile_rects)

        if (collision_response.tile_collision_x != None or collision_response.tile_collision_y != None):
            self.arm_state = ArmStateEnum.STUCK

        if (collision_response.tile_collision_x != None):
            if (collision_response.tile_collision_x.side == CollisionEnum.LEFT): 
                self.entity.x -= (self.entity.height / 4)
                self.arm_angle = 90
            elif (collision_response.tile_collision_x.side == CollisionEnum.RIGHT):
                self.entity.x += (self.entity.height / 4)
                self.arm_angle = 90

        if (collision_response.tile_collision_y != None):
            if (collision_response.tile_collision_y.side == CollisionEnum.TOP): 
                self.entity.y += (self.entity.height / 4)
                self.arm_angle = 0
            elif (collision_response.tile_collision_y.side == CollisionEnum.BOTTOM): 
                self.entity.y -= (self.entity.height / 4)
                self.arm_angle = 180

            # collided_tile_key = f"{int(collision_response.position[0]/self.map.tile_size)};{int(collision_response.position[1]/self.map.tile_size)}"
            # if (collided_tile_key in self.map.map_model.tiles):
            #     collided_tile = self.map.map_model.tiles[collided_tile_key]
            #     for linked_tile_key in collided_tile.linked_tile_keys:
            #         self.map.opening_platforms[linked_tile_key].is_closing = False
            #         self.map.opening_platforms[linked_tile_key].is_open = True
            #         self.arm_opened_platforms.append(self.map.opening_platforms[linked_tile_key])
                
            self.velocity[0] = 0
            self.velocity[1] = 0

        return
    
    def render(self, display, scroll) -> None:
        arm_surface = self.static_image.image
        player_arm_image_loc = [self.entity.x, self.entity.y]
        
        if (self.arm_state != ArmStateEnum.STUCK):
            arm_surface = pygame.Surface((self.static_image.image.get_width() * 2, self.static_image.image.get_height() * 2))
            arm_surface.set_colorkey((0, 0, 0))
            arm_surface.blit(self.static_image.image, (0, self.static_image.image.get_height()))

        arm_surface = pygame.transform.flip(pygame.transform.rotate(arm_surface, self.arm_angle), self.entity.is_flipped, False)
        player_arm_image_loc = [round(self.entity.x) - int(arm_surface.get_width() / 2), self.entity.y - int(arm_surface.get_height() / 2)]
        
        display.blit(arm_surface, (player_arm_image_loc[0]- scroll[0], player_arm_image_loc[1] - scroll[1]))
        return
    
    def update_arm_state(self, mouse_angle) -> None:
        arm_display_angle = mouse_angle - (math.pi/2)
        # Attached to player
        if (self.arm_state == ArmStateEnum.ATTACHED):
            self.arm_angle = math.degrees(arm_display_angle)
            if (self.entity.is_flipped):
                self.arm_angle += self.charge
            if (self.entity.is_flipped == False):
                self.arm_angle -= self.charge
                self.arm_angle = -self.arm_angle
        # Thrown by player
        elif (self.arm_state == ArmStateEnum.DETACHED):
            self.arm_angle -= 20
        # Stuck in wall
        elif (self.arm_state == ArmStateEnum.STUCK):
            self.velocity = [0, 0]       
            if (self.arm_stuck_timer > 250):
                self.reset_arm()
            else:
                self.arm_stuck_timer += 1
                 
        return
    
    def recall_arm(self) -> None:
        if (self.arm_state == ArmStateEnum.STUCK):
            self.reset_arm()

    def reset_arm(self) -> None:
        self.arm_stuck_timer = 0
        self.arm_state = ArmStateEnum.ATTACHED
        return
    