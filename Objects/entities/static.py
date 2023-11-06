from pygame import Surface
import pygame

from objects.entities.image import Image

class Static(Image):
    def __init__(self, entity, image: Surface):
        self.entity = entity
        self.image = image.convert()
        self.image.set_colorkey((0,0,0))
        entity.width = image.get_width()
        entity.height = image.get_height()

    def get_surface(self):
        return self.image