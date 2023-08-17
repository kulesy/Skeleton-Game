from marshmallow import Schema, fields, post_load

class TileModel:
    def __init__(self, position : list[int], tile_type_id : int = 0, linked_tile_key: str = ""):
        self.position : list[int] = position
        self.tile_type_id : int = tile_type_id
        self.linked_tile_key: str = linked_tile_key

class TileSchema(Schema):
    position = fields.List(fields.Integer())
    tile_type_id = fields.Integer()
    linked_tile_key = fields.String()
    
    @post_load
    def post_load(self, data, **kwargs):
        return TileModel(**data)