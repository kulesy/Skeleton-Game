from marshmallow import Schema, fields, post_load

class TileModel:
    def __init__(self, position : list[int], tile_type_id : int = 0, linked_tile_key: str = "", rotation: int = 0):
        self.position : list[int] = position
        self.tile_type_id : int = tile_type_id
        self.linked_tile_key: str = linked_tile_key
        self.rotation: int = rotation

class TileSchema(Schema):
    position = fields.List(fields.Integer())
    tile_type_id = fields.Integer()
    linked_tile_key = fields.String()
    rotation = fields.Integer()
    
    @post_load
    def post_load(self, data, **kwargs):
        return TileModel(**data)