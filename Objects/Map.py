import json
import pygame
from consts.colourconsts import BLACK
from enums.global_enums import DirectionEnum, PlatformEnum
from objects.models.map.map_model import MapModel, MapSchema
from objects.platform import Platform

class Map:
    def __init__(self, tile_size):
        with open('map.json') as f:
            map_json = json.load(f)
    
        self.map_model: MapModel = MapSchema().load(map_json)
        self.tile_size = tile_size
        self.tile_type_textures = {}
        self.tile_type_rects = {}
        self.scroll = [0,0]
        self.tile_rects = []
        self.true_scroll: list[float] = [0, 0]
        self.init_tile_types()
        self.platforms : dict[str, Platform] = {}

    def render(self, display):
        self.tile_rects = []
        map_tiles = self.map_model.tiles

        for tile in map_tiles.values():
            tile_key = f"{tile.position[0]};{tile.position[1]}"
            rotation = tile.rotation
            if (tile.tile_type_id == 3 and tile_key in self.platforms):
                platform = self.platforms[tile_key]
                if (platform.is_open):
                    rotation = 0
                    
                if (platform.is_closing and 
                    platform.close_counter <= 300):
                    platform.close_counter += 1
                elif (platform.close_counter > 300):
                    platform.is_open = False
                    platform.is_closing = False
                    platform.close_counter = 0
            elif (tile.tile_type_id == 3):
                self.platforms[tile_key] = Platform(self.tile_size, tile.position, False)
            

            texture: pygame.Surface = self.tile_type_textures[tile.tile_type_id]
            display.blit(pygame.transform.rotate(texture, rotation), 
                         (tile.position[0] * self.tile_size - self.scroll[0],
                         tile.position[1] * self.tile_size - self.scroll[1]))
            
            tile_rect: pygame.Rect = self.tile_type_rects[tile.tile_type_id]

            rotated_rect = self.get_rotated_rect(tile_rect.copy(), rotation)
            
            self.tile_rects.append(pygame.Rect(tile.position[0] * self.tile_size + rotated_rect.x,
                                                tile.position[1] * self.tile_size + rotated_rect.y, 
                                                rotated_rect.width, rotated_rect.height))
                

    def init_tile_types(self):
        map_textures = self.map_model.tile_types

        for texture in map_textures:
            texture_image = pygame.image.load(texture.texture_path)
            texture_image.set_colorkey(BLACK)
            texture_image.convert_alpha()
            tile_rect = self.get_non_transparent_bounds(texture_image)
            self.tile_type_textures[texture.tile_type_id] = texture_image
            self.tile_type_rects[texture.tile_type_id] = tile_rect

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
