from marshmallow import Schema, fields, post_load

class BlockModel:
    def __init__(self, position : list[int] = [0, 0], type_id : int = 0,
                 rotation: int = 0):
        self.position : list[int] = position
        self.type_id : int = type_id
        self.rotation: int = rotation

class BlockSchema(Schema):
    position = fields.List(fields.Integer())
    type_id = fields.Integer()
    rotation = fields.Integer()
    
    @post_load
    def post_load(self, data, **kwargs):
        return BlockModel(**data)