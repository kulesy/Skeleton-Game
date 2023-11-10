import json
import math
import pygame
from consts.colourconsts import BLACK
from models.map.map_model import MapModel, MapSchema
from objects.disappearing_platforms import DisapearingPlatforms
from objects.entities.entity import Entity
from objects.entities.hitbox import Hitbox
from objects.entities.render import Render
from objects.entities.static import Static
from objects.opening_platforms import OpeningPlatforms
from objects.block import Platform

class Map:
    def __init__(self, tile_size, display):
        with open('map.json') as f:
            map_json = json.load(f)
    
        self.map_model: MapModel = MapSchema().load(map_json)
        self.display = display
        self.tile_size = tile_size
        self.block_type_textures = {}
        self.block_type_rects = {}
        self.entity_type_textures = {}
        self.entity_type_rects = {}
        self.scroll = [0,0]
        self.true_scroll: list[float] = [0, 0]
        self._renders : list[Render] = []
        self.platforms : dict[int, Platform] = {}
        self.opening_platforms : dict[int, OpeningPlatforms] = {}
        self.disapearing_platforms : dict[int, DisapearingPlatforms] = {}
        self._entity_id_increment = 0
        self.init_tile_types()
        self.init_entities()

    def render(self):
        self.render_map_entities()

    def render_map_entities(self):
        for render in sorted(self._renders, key=lambda x: x.z_level):
            self.render_surface(render.get_surface(), 
                                (render.hitbox.entity.x,  render.hitbox.entity.y))
            
            # Render hitboxes
            # hitbox_rect = render.hitbox.get_hitbox_rect().copy()
            # hitbox_map_pos = self.get_map_position((hitbox_rect.x, hitbox_rect.y))
            # hitbox_rect.x = hitbox_map_pos[0]
            # hitbox_rect.y = hitbox_map_pos[1]
            # pygame.draw.rect(self.display, (255, 0, 0), hitbox_rect)

            
    def render_surface(self, surface, position):
        self.display.blit(surface, self.get_map_position(position))

    def init_entities(self):
        for entity_model in self.map_model.entities.values():
            rotation = entity_model.rotation
            position = entity_model.position.copy()

            texture: pygame.Surface = self.entity_type_textures[entity_model.type_id]
            
            tile_rect: pygame.Rect = self.entity_type_rects[entity_model.type_id]
            
            entity = Entity()
            entity.id = entity_model.id
            entity.x = position[0] * self.tile_size
            entity.y = position[1] * self.tile_size
            static_image = Static(entity, texture)

            if (entity.id > self._entity_id_increment):
                self._entity_id_increment = entity.id

            hitbox = Hitbox(entity,
                            tile_rect.x, tile_rect.y, 
                            tile_rect.width, tile_rect.height)
            
            render = Render(self.tile_size, hitbox, static_image, 0, True)
            render.rotation = rotation

            self._renders.append(render)
            
            if (self.is_entity_platform(entity_model.type_id)):
                entity.is_platform = True
                platform = Platform(static_image, hitbox)
                self.platforms[entity.id] = platform

                if (entity_model.type_id == 3):
                    self.opening_platforms[entity_model.id] = OpeningPlatforms(platform, static_image, hitbox, False)

                if (entity_model.type_id == 4):
                    self.disapearing_platforms[entity_model.id] = DisapearingPlatforms(entity, static_image, hitbox)

    def init_tile_types(self):
        for entity_type in self.map_model.entity_types:
            texture_image = pygame.image.load(entity_type.texture_path)
            texture_image.set_colorkey(BLACK)
            texture_image.convert_alpha()
            entity_rect = self.get_non_transparent_bounds(texture_image)
            self.entity_type_textures[entity_type.id] = texture_image
            self.entity_type_rects[entity_type.id] = entity_rect

    def update_scroll_pos(self, player_x, player_y, player_width, player_height):
        self.true_scroll[0] += (player_x - self.true_scroll[0] - 150 + int(player_width / 2))/20
        self.true_scroll[1] += (player_y - self.true_scroll[1] - 100 + int(player_height / 2))/20
        scroll = self.true_scroll.copy()
        self.scroll[0] = int(scroll[0])
        self.scroll[1] = int(scroll[1])
    
    def get_non_transparent_bounds(self, surface: pygame.Surface):
        """Returns a Rect encompassing the non-transparent parts of a Surface."""
        min_x = surface.get_width() - 1
        max_x = 0
        min_y = surface.get_height() - 1
        max_y = 0

        for y in range(surface.get_height()):
            for x in range(surface.get_width()):
                colour = surface.get_at((x, y))
                if ((colour.r, colour.g, colour.b) != BLACK):  # Not transparent
                    min_x = min(min_x, x)
                    max_x = max(max_x, x)
                    min_y = min(min_y, y)
                    max_y = max(max_y, y)

        if min_x > max_x or min_y > max_y:
            # All pixels are transparent; return an empty rect
            return pygame.Rect(0, 0, 0, 0)

        return pygame.Rect(min_x, min_y, max_x - min_x + 1, max_y - min_y + 1)
    
    def get_map_position(self, position):
        map_position_x = position[0] - self.scroll[0]
        map_position_y = position[1] - self.scroll[1]
        return (map_position_x, map_position_y)
    
    def is_entity_platform(self, entity_type_id):
        for type in self.map_model.entity_types:
            if (type.id == entity_type_id and type.is_platform):
                return True
    
    def add_to_renders(self, render: Render):
        if (render.hitbox.entity.id == 0):
            self._entity_id_increment += 1
            render.hitbox.entity.id = self._entity_id_increment

        self._renders.append(render)

    def get_renders(self):
        return self._renders
