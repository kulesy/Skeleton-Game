import pygame


class Block(object):
    def __init__(self, x, y, block_size, rotation=0):
        self.x = x * block_size
        self.y = y * block_size 
        self.rect = pygame.Rect(x, y, block_size, block_size)
        self.rotation = rotation
        self.friction = 0.2