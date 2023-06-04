import pygame

from Objects.Player import Player

class Map:
    def __init__(self, map_json, tile_size):
        self.map_json = map_json
        self.tile_size = tile_size
        self.tile_textures = None
        self.scroll = [0,0]
        self.tile_rects = []
        self.true_scroll = [0,0]
        self.get_tile_textures()

    def render(self, display):
        self.tile_rects = []
        self.get_tile_textures()
        map_tiles = self.map_json["tiles"]

        for tile in map_tiles.values():
            display.blit(self.tile_textures[tile["texture"]], 
                         (tile["position"][0] * self.tile_size - self.scroll[0],
                         tile["position"][1] * self.tile_size - self.scroll[1]))
            self.tile_rects.append(pygame.Rect((tile["position"][0] * self.tile_size,
                                      tile["position"][1] * self.tile_size), 
                                      (16, 16)))

    def get_tile_textures(self):
        map_textures = self.map_json["textures"]

        texture_dict = {}
        for texture in map_textures:
            texture_image = pygame.image.load(texture["path"])
            texture_dict[texture["value"]] = texture_image
        self.tile_textures = texture_dict

    def update_scroll_pos(self, player: Player):
        self.true_scroll[0] += (player.entity.x - self.true_scroll[0] - 150 + int(player.entity.size_x / 2))/20
        self.true_scroll[1] += (player.entity.y - self.true_scroll[1] - 100 + int(player.entity.size_y / 2))/20
        scroll = self.true_scroll.copy()
        self.scroll[0] = int(scroll[0])
        self.scroll[1] = int(scroll[1])

