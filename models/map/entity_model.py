from marshmallow import Schema, fields, post_load

class EntityModel:
    def __init__(self, id: int = 0, type_id: int = 0, position: list[int] = [0, 0],
                 rotation: int = 0, linked_entity_ids: list[int] = []):
        self.id: int = id
        self.type_id: int = type_id
        self.position: list[int] = position
        self.rotation: int = rotation
        self.linked_entity_ids: list[int] = linked_entity_ids

class EntitySchema(Schema):
    id = fields.Integer()
    type_id = fields.Integer()
    position = fields.List(fields.Integer())
    rotation = fields.Integer()
    linked_entity_ids = fields.List(fields.Integer())
    
    @post_load
    def post_load(self, data, **kwargs):
        return EntityModel(**data)