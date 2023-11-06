import pygame
from objects.entities.hitbox import Hitbox

from objects.entities.image import Image


class Render():
    def __init__(self, tile_size, hitbox: Hitbox, 
                 image: Image, z_level, is_auto_hitbox, 
                 is_anchored = False, anchor_point = (0, 0)):
        self.tile_size = tile_size
        self.hitbox = hitbox
        self.image = image 
        self.z_level = z_level
        self._is_auto_hitbox = is_auto_hitbox
        self.is_flipped = False
        self.is_anchored = is_anchored
        self.is_centered = is_anchored
        self.anchor_point : tuple[int, int] = anchor_point
        self._rotation = 0
        self.original_offset = (hitbox.offset_x, hitbox.offset_y)

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, value):
        self._rotation = value

        if (self._is_auto_hitbox):
            offset_rect = pygame.Rect(self.hitbox.offset_x, self.hitbox.offset_y, self.hitbox.width, self.hitbox.height)
            new_offset_rect = self.get_rotated_offset(offset_rect) 
            self.hitbox.width = new_offset_rect.width
            self.hitbox.height = new_offset_rect.height
            self.hitbox.offset_x = new_offset_rect.x
            self.hitbox.offset_y = new_offset_rect.y

    def get_surface(self):
        surface = pygame.transform.flip(pygame.transform.rotate(self.image.get_surface(), self._rotation), self.is_flipped, False)
        rotation = None
        if (self.is_flipped):
            rotation = self.rotation
        else: 
            rotation = -self.rotation
            
        if (self.is_anchored):
            # Center render position and apply offset
            offset = pygame.math.Vector2(self.anchor_point[0], self.anchor_point[1])
            rotated_offset = offset.rotate(rotation)

            self.hitbox.entity.x = (round(self.hitbox.entity.x) - int(surface.get_width() / 2))  + rotated_offset.x
            self.hitbox.entity.y = (self.hitbox.entity.y - int(surface.get_height() / 2))  + rotated_offset.y

        if (self.is_centered):
            # Center hitbox and apply offset
            hitbox_offset = pygame.math.Vector2(self.original_offset[0], self.original_offset[1])
            rotated_hitbox_offset = hitbox_offset.rotate(rotation)

            self.hitbox.offset_x = rotated_hitbox_offset.x + int(surface.get_width() / 2)
            self.hitbox.offset_y = rotated_hitbox_offset.y + int(surface.get_height() / 2)

        return surface

    def get_rotated_offset(self, rect: pygame.Rect) -> pygame.Rect:
        offset_x = self.tile_size - (rect.x + rect.width)
        offset_y = self.tile_size - (rect.y + rect.height)
        width = rect.width
        height = rect.height
        x = rect.x
        y = rect.y

        if (self.rotation == 90):
            rect.x = y
            rect.y = offset_x

            rect.width = height
            rect.height = width
            
        if (self.rotation == 180):
            rect.x = offset_x
            rect.y = offset_y

        if (self.rotation == 270):
            rect.x = offset_y
            rect.y = x

            rect.width = height
            rect.height = width

        return rect