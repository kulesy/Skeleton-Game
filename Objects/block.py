from objects.entities.entity import Entity
from objects.entities.hitbox import Hitbox
from objects.entities.static import Static


class Platform(object):
    def __init__(self, static_image, hitbox):
        self.hitbox: Hitbox = hitbox
        self.static_image: Static = static_image
        self.friction = 0.5