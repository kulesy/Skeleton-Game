from marshmallow import Schema, fields, post_load

from models.map.entity_model import EntityModel, EntitySchema
from models.map.entity_type_model import EntityTypeModel, EntityTypeSchema

class MapModel:
    def __init__(self, entities: dict[str, EntityModel] = {}, entity_types: list[EntityTypeModel] = []):
        self.entities: dict[str, EntityModel] = entities
        self.entity_types: list[EntityTypeModel] = entity_types

class MapSchema(Schema):
    entities = fields.Dict(fields.String(), fields.Nested(EntitySchema))
    entity_types = fields.Nested(EntityTypeSchema(many=True))

    @post_load
    def post_load(self, data, **kwargs):
        return MapModel(**data)