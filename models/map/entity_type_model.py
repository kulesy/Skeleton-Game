from marshmallow import Schema, fields, post_load

class EntityTypeModel:
    def __init__(self, id: int = 0, texture_path: str = ""):
        self.id: int = id
        self.texture_path: str = texture_path

class EntityTypeSchema(Schema):
    id = fields.Integer()
    texture_path = fields.String()

    @post_load
    def post_load(self, data, **kwargs):
        return EntityTypeModel(**data)
        