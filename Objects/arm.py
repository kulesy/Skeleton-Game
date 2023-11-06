import math
import pygame
from enums.global_enums import ArmStateEnum, CollisionEnum, DirectionEnum
from objects.entities.entity import Entity
from objects.entities.hitbox import Hitbox
from objects.entities.movable import Movable
from objects.entities.render import Render
from objects.entities.static import Static
from objects.map import Map
from objects.opening_platforms import OpeningPlatforms

class Arm():
    def __init__(self, map, player_entity):
        self.map: Map = map
        self.entity = Entity()
        self.entity.x = player_entity.x
        self.entity.y = player_entity.y
        self.image_surface = pygame.image.load('assets/animations/arm/idle/0.png')
        self.static_image = Static(self.entity, self.image_surface)
        hitbox_width = 4
        hitbox_height = 4
        self.hitbox = Hitbox(self.entity, 
                             0,
                             0,
                             hitbox_width, hitbox_height)
        self.render = Render(self.map.tile_size, self.hitbox, self.static_image, 1, 
                             False, True, (0, (self.image_surface.get_height() // 2)))
        self.map.add_to_renders(self.render)
        
        self.movable = Movable(self.hitbox, map)
        
        self.arm_max_distance: int = 6
        self.arm_state: ArmStateEnum = ArmStateEnum.ATTACHED
        self.arm_opened_platforms: list[OpeningPlatforms] = [] 
        self.charge: float = 0
        self.arm_stuck_timer: float = 0

        
    def move_arm(self) -> None:
        if (self.arm_state != ArmStateEnum.DETACHED):
            return

        hitbox_collisions = self.movable.move()
        platform_collision = next((hitbox for hitbox in hitbox_collisions if hitbox.hitbox.entity.is_platform), None)
        
        if (platform_collision != None):
            self.arm_state = ArmStateEnum.STUCK
            # if (platform_collision.side == CollisionEnum.LEFT): 
            #     self.entity.x += 3
            #     self.render.rotation = 90
            #     self.hitbox.offset_x = 0
            # elif (platform_collision.side == CollisionEnum.RIGHT):
            #     self.entity.x -= 3
            #     self.render.rotation = 90
            #     self.hitbox.offset_x = self.entity.height
            # if (platform_collision.side == CollisionEnum.TOP): 
            #     self.entity.y +=  3
            #     self.render.rotation = 0
            #     self.hitbox.offset_y = 0
            # elif (platform_collision.side == CollisionEnum.BOTTOM): 
            #     self.entity.y -= 3
            #     self.render.rotation = 180
            #     self.hitbox.offset_y = self.entity.height

            # collided_tile_key = f"{int(collision_response.position[0]/self.map.tile_size)};{int(collision_response.position[1]/self.map.tile_size)}"
            # if (collided_tile_key in self.map.map_model.tiles):
            #     collided_tile = self.map.map_model.tiles[collided_tile_key]
            #     for linked_tile_key in collided_tile.linked_tile_keys:
            #         self.map.opening_platforms[linked_tile_key].is_closing = False
            #         self.map.opening_platforms[linked_tile_key].is_open = True
            #         self.arm_opened_platforms.append(self.map.opening_platforms[linked_tile_key])

        return
    
    def handle_render(self) -> None:
        if (self.arm_state != ArmStateEnum.STUCK):
            arm_surface = pygame.Surface((self.static_image.image.get_width() * 2, self.static_image.image.get_height() * 2))
            arm_surface.set_colorkey((0, 0, 0))
            arm_surface.blit(self.static_image.image, (0, self.static_image.image.get_height()))

        return
    
    def update_arm_state(self, mouse_angle) -> None:
        arm_display_angle = mouse_angle - (math.pi/2)
        # Attached to player
        if (self.arm_state == ArmStateEnum.ATTACHED):
            self.render.rotation = math.degrees(arm_display_angle)
            if (self.render.is_flipped):
                self.render.rotation += self.charge
            if (self.render.is_flipped == False):
                self.render.rotation -= self.charge
                self.render.rotation = -self.render.rotation
        # Thrown by player
        elif (self.arm_state == ArmStateEnum.DETACHED):
            self.render.rotation -= 20
        # Stuck in wall
        elif (self.arm_state == ArmStateEnum.STUCK):
            self.velocity = [0, 0]       
            if (self.arm_stuck_timer > 250):
                self.reset_arm()
            else:
                self.arm_stuck_timer += 1
                 
        return
    
    def flip_arm(self, player_direction):
        if (self.arm_state == ArmStateEnum.ATTACHED and player_direction == DirectionEnum.LEFT):
            self.render.is_flipped = True
        elif(self.arm_state == ArmStateEnum.ATTACHED and player_direction == DirectionEnum.RIGHT):
            self.render.is_flipped = False

    def recall_arm(self) -> None:
        if (self.arm_state == ArmStateEnum.STUCK):
            self.reset_arm()

    def reset_arm(self) -> None:
        self.arm_stuck_timer = 0
        self.arm_state = ArmStateEnum.ATTACHED
        self.render.is_anchored = True
        return
    