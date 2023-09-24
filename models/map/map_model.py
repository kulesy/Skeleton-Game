from marshmallow import Schema, fields, post_load
from objects.models.map.entity_model import EntityModel, EntitySchema
from objects.models.map.entity_type_model import EntityTypeModel, EntityTypeSchema
from objects.models.map.block_type_model import BlockTypeModel, BlockTypeSchema

from objects.models.map.block_model import BlockModel, BlockSchema

class MapModel:
    def __init__(self, blocks: dict[str, BlockModel] = {}, block_types: list[BlockTypeModel] = [],
                 entities: dict[str, EntityModel] = {}, entity_types: list[EntityTypeModel] = []):
        self.blocks: dict[str, BlockModel] = blocks
        self.block_types: list[BlockTypeModel] = block_types
        self.entities: dict[str, EntityModel] = entities
        self.entity_types: list[EntityTypeModel] = entity_types

class MapSchema(Schema):
    blocks = fields.Dict(fields.String(), fields.Nested(BlockSchema))
    block_types = fields.Nested(BlockTypeSchema(many=True))
    entities = fields.Dict(fields.String(), fields.Nested(EntitySchema))
    entity_types = fields.Nested(EntityTypeSchema(many=True))

    @post_load
    def post_load(self, data, **kwargs):
        return MapModel(**data)