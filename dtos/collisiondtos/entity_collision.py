from enums.global_enums import CollisionEnum
from objects.entities.entity import Entity

class EntityCollision: 
    def __init__(self, entity: Entity, direction=CollisionEnum.NONE):
      self.entity: Entity = entity
      self.direction: CollisionEnum = direction