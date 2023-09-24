import asyncio
import pygame
from enums.global_enums import DirectionEnum, PlatformEnum


class OpeningPlatforms:
    def __init__(self, is_open=False):
        self.is_open = is_open
        self.is_closing = False
        self.close_counter = 0