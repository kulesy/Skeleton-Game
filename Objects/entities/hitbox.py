import pygame


class Hitbox:
    def __init__(self, entity, offset_x, 
                 offset_y, width, height) -> None:
        self.entity = entity
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.width = width
        self.height = height

    def get_hitbox_rect(self):
        return pygame.Rect(self.entity.x + self.offset_x,
                           self.entity.y + self.offset_y,
                           self.width, self.height)