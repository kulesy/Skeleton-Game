import asyncio
import pygame
from enums.global_enums import DirectionEnum, PlatformEnum


class DisapearingPlatforms:
    def __init__(self):
        self.has_disapeared = False
        self.is_disapearing = False
        self.disapear_counter = 0