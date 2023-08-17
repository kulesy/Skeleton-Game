from marshmallow import Schema, fields, post_load
from objects.models.map.tile_type_model import TileTypeModel, TileTypeSchema

from objects.models.map.tile_model import TileModel, TileSchema

class MapModel:
    def __init__(self, tiles : dict[str, TileModel] = {}, tile_types : list[TileTypeModel] = []):
        self.tiles : dict[str, TileModel] = tiles
        self.tile_types : list[TileTypeModel] = tile_types

class MapSchema(Schema):
    tiles = fields.Dict(fields.String(), fields.Nested(TileSchema))
    tile_types = fields.Nested(TileTypeSchema(many=True))

    @post_load
    def post_load(self, data, **kwargs):
        return MapModel(**data)