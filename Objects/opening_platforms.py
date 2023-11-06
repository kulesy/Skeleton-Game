import asyncio
import pygame
from enums.global_enums import DirectionEnum, PlatformEnum
from objects.block import Platform
from objects.entities.entity import Entity
from objects.entities.hitbox import Hitbox
from objects.entities.static import Static


class OpeningPlatforms:
    def __init__(self, platform: Platform, static_image, hitbox: Hitbox, is_open=False):
        self.platform: Platform = platform
        self.static_image: Static = static_image
        self.hitbox: Hitbox = hitbox
        self.is_open = is_open
        self.is_closing = False
        self.close_counter = 0