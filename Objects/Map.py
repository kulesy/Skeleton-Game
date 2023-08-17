import json
import pygame
from enums.global_enums import DirectionEnum, PlatformEnum
from objects.models.map.map_model import MapModel, MapSchema
from objects.platform import Platform

class Map:
    def __init__(self, tile_size):
        with open('map.json') as f:
            map_json = json.load(f)
    
        self.map_model: MapModel = MapSchema().load(map_json)
        self.tile_size = tile_size
        self.tile_textures = {}
        self.scroll = [0,0]
        self.tile_rects = []
        self.true_scroll: list[float] = [0, 0]
        self.get_tile_textures()
        self.platforms = { "17;1": Platform(tile_size, [17,1], PlatformEnum.RIGHT, False),
                           "16;1": Platform(tile_size, [16,1], PlatformEnum.LEFT, False)}

    def render(self, display):
        self.tile_rects = []
        self.get_tile_textures()
        map_tiles = self.map_model.tiles

        for tile in map_tiles.values():
            display.blit(self.tile_textures[tile.tile_type_id], 
                         (tile.position[0] * self.tile_size - self.scroll[0],
                         tile.position[1] * self.tile_size - self.scroll[1]))
            self.tile_rects.append(pygame.Rect((tile.position[0] * self.tile_size,
                                      tile.position[1] * self.tile_size), 
                                      (16, 16)))
        
        for platform in self.platforms.values():
            if (platform.is_closing and 
                platform.close_counter <= 300):
                platform.close_counter += 1
            elif (platform.close_counter > 300):
                platform.is_open = False
                platform.is_closing = False
                platform.close_counter = 0
            
            display.blit(platform.get_texture(), 
                         (platform.position[0] * self.tile_size - self.scroll[0],
                         platform.position[1] * self.tile_size - self.scroll[1]))
            
            self.tile_rects.append(pygame.Rect((platform.get_rect_position()[0], platform.get_rect_position()[1]), platform.get_size()))

    def get_tile_textures(self):
        map_textures = self.map_model.tile_types

        texture_dict = {}
        for texture in map_textures:
            texture_image = pygame.image.load(texture.texture_path)
            texture_dict[texture.tile_type_id] = texture_image
        self.tile_textures = texture_dict

    def update_scroll_pos(self, player_x, player_y, player_width, player_height):
        self.true_scroll[0] += (player_x - self.true_scroll[0] - 150 + int(player_width / 2))/20
        self.true_scroll[1] += (player_y - self.true_scroll[1] - 100 + int(player_height / 2))/20
        scroll = self.true_scroll.copy()
        self.scroll[0] = int(scroll[0])
        self.scroll[1] = int(scroll[1])

