from pygame import Surface

class StaticImage:
    def __init__(self, entity, image: Surface):
        self.image = image.convert()
        self.image.set_colorkey((0,0,0))
        entity.width = image.get_width()
        entity.height = image.get_height()