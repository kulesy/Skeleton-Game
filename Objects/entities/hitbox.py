import pygame
from objects.entities.entity import Entity


class Hitbox:
    def __init__(self, entity, offset_x, 
                 offset_y, width, height) -> None:
        self.entity: Entity = entity
        self.offset_x: float = offset_x
        self.offset_y: float = offset_y
        self.width = width
        self.height = height

    def get_hitbox_rect(self):
        x = self.entity.x + self.offset_x
        y = self.entity.y + self.offset_y

        return pygame.Rect(x, y, self.width, self.height)