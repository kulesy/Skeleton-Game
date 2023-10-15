import json
import math
import pygame
from consts.colourconsts import BLACK
from models.map.map_model import MapModel, MapSchema
from objects.disappearing_platforms import DisapearingPlatforms
from objects.entities.entity import Entity
from objects.entities.hitbox import Hitbox
from objects.entities.static import StaticImage
from objects.opening_platforms import OpeningPlatforms
from objects.block import Block

class Map:
    def __init__(self, tile_size, display):
        with open('map.json') as f:
            map_json = json.load(f)
    
        self.map_model: MapModel = MapSchema().load(map_json)
        self.blocks: dict[str, Block] = {}
        self.entity_hitboxes: list[Hitbox] = []
        self.display = display
        self.tile_size = tile_size
        self.block_type_textures = {}
        self.block_type_rects = {}
        self.entity_type_textures = {}
        self.entity_type_rects = {}
        self.scroll = [0,0]
        self.true_scroll: list[float] = [0, 0]
        self.init_tile_types()
        self.opening_platforms : dict[str, OpeningPlatforms] = {}
        self.disapearing_platforms : dict[str, DisapearingPlatforms] = {}

    def render(self):
        self.entity_hitboxes = []
        self.render_map_tiles()
        self.render_map_entities()

    def render_map_tiles(self):
         for block_model in self.map_model.blocks.values():
            rotation = block_model.rotation
            position = block_model.position.copy()
            block_key = f"{block_model.position[0]};{block_model.position[1]}"
            texture: pygame.Surface = self.block_type_textures[block_model.type_id]
            self.render_surface(pygame.transform.rotate(texture, rotation),
                                (position[0] * self.tile_size, position[1] * self.tile_size))

            if (block_key not in self.blocks):
                block = Block(block_model.position[0],
                              block_model.position[1], 
                              self.tile_size, 
                              block_model.rotation)
                
                self.blocks[block_key] = block

    def render_map_entities(self):
        for entity_model in self.map_model.entities.values():
            rotation = entity_model.rotation
            position = entity_model.position.copy()
            is_visible = True
            entity_model_key = f"{entity_model.position[0]};{entity_model.position[1]}"

            texture: pygame.Surface = self.entity_type_textures[entity_model.type_id]
            
            tile_rect: pygame.Rect = self.entity_type_rects[entity_model.type_id]

            rotated_rect = self.get_rotated_rect(tile_rect.copy(), rotation)
            
            entity = Entity()
            entity.x = position[0] * self.tile_size
            entity.y = position[1] * self.tile_size
            static_image = StaticImage(entity, texture)

            hitbox = Hitbox(entity,
                            rotated_rect.x, rotated_rect.y, 
                            rotated_rect.width, rotated_rect.height)

            if (entity_model.type_id == 3):
                platform = self.opening_platforms[entity_model_key]
                if (platform.is_open):
                    if (entity_model.rotation == 0):
                        rotation = 90
                        position[1] -= 1
                    elif (entity_model.rotation == 90):
                        rotation = 180
                        position[0] -= 1
                    elif (entity_model.rotation == 180):
                        rotation = 270
                        position[1] += 1
                    elif (entity_model.rotation == 270):
                        rotation = 0
                        position[0] += 1
                if (platform.is_closing and 
                    platform.close_counter <= 300):
                    platform.close_counter += 1
                elif (platform.close_counter > 300):
                    platform.is_open = False
                    platform.is_closing = False
                    platform.close_counter = 0
                else: 
                    platform.close_counter = 0
            elif (entity_model.type_id == 3):
                self.opening_platforms[entity_model_key] = OpeningPlatforms(entity, static_image, hitbox, False)
            
            if (entity_model.type_id == 4 and entity_model_key in self.disapearing_platforms):
                platform = self.disapearing_platforms[entity_model_key]
                if (platform.has_disapeared):
                    is_visible = False
                elif (platform.is_disapearing and 
                    platform.disapear_counter <= 70):
                    platform.disapear_counter += 1
                elif (platform.disapear_counter > 70):
                    platform.has_disapeared = True
                    platform.is_disapearing = False
                    platform.disapear_counter = 0
            elif (entity_model.type_id == 4):
                self.disapearing_platforms[entity_model_key] = DisapearingPlatforms(entity, static_image, hitbox)

            if (is_visible):
                self.entity_hitboxes.append(hitbox)
                
                self.render_surface(pygame.transform.rotate(texture, rotation), 
                                                           (position[0] * self.tile_size, position[1] * self.tile_size))
    def render_surface(self, surface, position):
        self.display.blit(surface, self.get_map_position(position))

    def init_tile_types(self):
        for block_type in self.map_model.block_types:
            texture_image = pygame.image.load(block_type.texture_path)
            texture_image.set_colorkey(BLACK)
            texture_image.convert_alpha()
            block_rect = self.get_non_transparent_bounds(texture_image)
            self.block_type_textures[block_type.id] = texture_image
            self.block_type_rects[block_type.id] = block_rect

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
    
    def get_rotated_rect(self, rect: pygame.Rect, rotation):
        offset_x = self.tile_size - (rect.x + rect.width)
        offset_y = self.tile_size - (rect.y + rect.height)
        width = rect.width
        height = rect.height
        x = rect.x
        y = rect.y

        if (rotation == 90):
            rect.x = y
            rect.y = offset_x

            rect.width = height
            rect.height = width
            
        if (rotation == 180):
            rect.x = offset_x
            rect.y = offset_y

        if (rotation == 270):
            rect.x = offset_y
            rect.y = x

            rect.width = height
            rect.height = width

        return rect
    
    def get_map_position(self, position):
        map_position_x = position[0] - self.scroll[0]
        map_position_y = position[1] - self.scroll[1]
        return (map_position_x, map_position_y)
