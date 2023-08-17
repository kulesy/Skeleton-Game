from marshmallow import Schema, fields, post_load

class TileTypeModel:
    def __init__(self, tile_type_id: int = 0, texture_path: str = ""):
        self.tile_type_id: int = tile_type_id
        self.texture_path: str = texture_path

class TileTypeSchema(Schema):
    tile_type_id = fields.Integer()
    texture_path = fields.String()

    @post_load
    def post_load(self, data, **kwargs):
        return TileTypeModel(**data)
        