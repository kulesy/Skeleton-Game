from enums.global_enums import CollisionEnum

class Collision: 
    def __init__(self, has_collided=False, direction=CollisionEnum.NONE, location=[]):
      self.has_collided: bool = has_collided
      self.direction: CollisionEnum = direction
      self.position: list[int] = location