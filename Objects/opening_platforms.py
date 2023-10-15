import asyncio
import pygame
from enums.global_enums import DirectionEnum, PlatformEnum
from objects.entities.entity import Entity
from objects.entities.hitbox import Hitbox
from objects.entities.static import StaticImage


class OpeningPlatforms:
    def __init__(self, entity: Entity, static_image, hitbox: Hitbox, is_open=False):
        self.entity: Entity = entity
        self.static_image: StaticImage = static_image
        self.hitbox: Hitbox = hitbox
        self.is_open = is_open
        self.is_closing = False
        self.close_counter = 0