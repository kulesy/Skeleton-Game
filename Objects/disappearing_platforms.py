import asyncio
import pygame
from enums.global_enums import DirectionEnum, PlatformEnum
from objects.entities.entity import Entity
from objects.entities.hitbox import Hitbox
from objects.entities.static import StaticImage


class DisapearingPlatforms:
    def __init__(self, entity: Entity, static_image, hitbox: Hitbox):
        self.entity: Entity = entity
        self.static_image: StaticImage = static_image
        self.hitbox: Hitbox = hitbox
        self.has_disapeared = False
        self.is_disapearing = False
        self.disapear_counter = 0