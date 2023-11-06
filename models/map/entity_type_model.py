from marshmallow import Schema, fields, post_load

class EntityTypeModel:
    def __init__(self, id: int = 0, texture_path: str = "", is_platform: bool = False):
        self.id: int = id
        self.texture_path: str = texture_path
        self.is_platform: bool = is_platform

class EntityTypeSchema(Schema):
    id = fields.Integer()
    texture_path = fields.String()
    is_platform = fields.Boolean()

    @post_load
    def post_load(self, data, **kwargs):
        return EntityTypeModel(**data)
        