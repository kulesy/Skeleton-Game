import asyncio
import pygame
from enums.global_enums import DirectionEnum, PlatformEnum


class Platform:
    def __init__(self, tile_size=0, position=(0,0), location=(0,0), is_open=False):
        self.tile_size = tile_size
        self.position = position
        self.location : PlatformEnum = location
        self.is_open = is_open
        self.is_closing = False
        self.close_counter = 0
    
    def get_texture(self):
        if (self.is_open):
            return pygame.image.load("assets/sprites/platform-top.png")
        
        if (self.location == PlatformEnum.RIGHT):
            return pygame.image.load("assets/sprites/platform-right.png")
        elif (self.location == PlatformEnum.LEFT):
            return pygame.image.load("assets/sprites/platform-left.png")
    
    def get_size(self):
        if (self.is_open):
            return (self.tile_size, 2)
        
        if (self.location == PlatformEnum.RIGHT or 
            self.location == PlatformEnum.LEFT):
            return (2, self.tile_size)
        
        return (self.tile_size, self.tile_size)

    
    def get_rect_position(self):
        if (self.is_open):
            return (self.position[0] * self.tile_size, self.position[1] * self.tile_size)
            
        if (self.location == PlatformEnum.RIGHT):
            return (self.position[0] * self.tile_size + self.tile_size - self.get_size()[0], self.position[1] * self.tile_size)

        elif (self.location == PlatformEnum.LEFT):
            return (2, self.tile_size)
        
        return (self.tile_size, self.tile_size)