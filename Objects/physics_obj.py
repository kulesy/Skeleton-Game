import pygame
from enums.global_enums import CollisionEnum
from objects.collision import Collision

from objects.physics_constants import PhysicsConstants

class PhysicsObj(object):
   
    def __init__(self, x, y, width, height, img):
        self.width = width
        self.height = height
        self.img: pygame.Surface = img
        self.rect = pygame.Rect(self.center_pos(x, self.width, x, self.img.get_width()), 
                                self.center_pos(y, self.height, x, self.img.get_height()), 
                                self.width, 
                                self.height)
        self.x = x
        self.y = y
        self.velocity: list[float] = [0, 0]

        physics_constants = PhysicsConstants()
        self.gravity = physics_constants.gravity
        self.friction = physics_constants.friction
        self.terminal_velocity = physics_constants.terminal_velocity
       
    def move(self, platforms):
        collision = Collision()

        self.x += self.velocity[0]
        self.rect.x = int(round(self.x))
        block_hit_list = self.collision_test(self.rect, platforms)

        for block in block_hit_list:
            if self.velocity[0] > 0:
                self.rect.right = block.left
                collision = Collision(True, CollisionEnum.RIGHT, [block.x, block.y])
            elif self.velocity[0] < 0:
                self.rect.left = block.right
                collision = Collision(True, CollisionEnum.LEFT, [block.x, block.y])
        
        self.x = self.rect.x

        self.y += self.velocity[1]
        self.rect.y = int(round(self.y))
        block_hit_list = self.collision_test(self.rect, platforms)

        for block in block_hit_list:
            if self.velocity[1] > 0:
                self.rect.bottom = block.top
                collision = Collision(True, CollisionEnum.TOP, [block.x, block.y])
            elif self.velocity[1] < 0:
                self.rect.top = block.bottom
                collision = Collision(True, CollisionEnum.BOTTOM, [block.x, block.y])

        self.y = self.rect.y

        return collision
    
    def collision_test(self, object_1, object_list):
        collision_list = []
        for obj in object_list:
            if obj.colliderect(object_1):
                collision_list.append(obj)
        return collision_list
    
    def center_pos(self, target_pos, target_size, obj_pos, obj_size):
        if (target_size > obj_size):
            width_diff = target_size - obj_size
            if (target_pos < obj_pos):
                target_pos = target_pos + (width_diff/2) 
            else:
                target_pos = target_pos - (width_diff/2) 
        elif (obj_size > target_size):
            width_diff = obj_size - target_size
            if (target_pos < obj_pos):
                target_pos = target_pos - (width_diff/2) 
            else:
                target_pos = target_pos + (width_diff/2) 

        return target_pos

