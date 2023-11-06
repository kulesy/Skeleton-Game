class Entity(object):
    def __init__(self):
        self.id: int = 0
        self.x: float = 0
        self.y: float = 0
        self.width = 0
        self.height = 0
        self.rotation = 0
        self.is_platform = False