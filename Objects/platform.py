import asyncio
import pygame
from enums.global_enums import DirectionEnum, PlatformEnum


class Platform:
    def __init__(self, tile_size=0, position=(0,0), is_open=False):
        self.tile_size = tile_size
        self.position = position
        self.is_open = is_open
        self.is_closing = False
        self.close_counter = 0