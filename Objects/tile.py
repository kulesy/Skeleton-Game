import pygame


class Block(object):
    def __init__(self, x, y, block_size):
        self.x = x
        self.y = y
        self.block_size = block_size
        self.rect = pygame.Rect(x, y, block_size, block_size)
        self.rotation = 0
        self.friction = 0