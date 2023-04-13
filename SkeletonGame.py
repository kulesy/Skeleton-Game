import pygame, sys
import scripts.engine as e
from perlin_noise import PerlinNoise
import json
import math
from enum import Enum

clock = pygame.time.Clock()

from pygame.locals import *
pygame.init()

pygame.display.set_caption('Test Game')

WINDOW_SIZE = (600, 400)

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface((300, 200))

moving_right = False
moving_left = False
charging_throw = False

map = {}

with open('map.json', 'r') as file:
    map = json.load(file)[0]


jump_height = 50

player_image = pygame.image.load('animations/player/idle/idle-1.png')
player_arm_image = pygame.image.load('animations/arm/idle/idle-1.png').convert()
player_arm_image.set_colorkey((0,0,0))
player_y_velocity = 0
player_arm_gravity = 0
air_timer = 0
true_scroll = [-150, -100]

noise_generator = PerlinNoise()

def load_map(tile_rects, scroll):
    texture = pygame.image.load(map["texture_path"])
    cells = map["cells"]
    for cell in cells:
        display.blit(texture, (cell[1] * 16 - scroll[0], cell[2] * 16 - scroll[1]))
        tile_rects.append(pygame.Rect((cell[1] * 16, cell[2] * 16), (16, 16)))


e.load_animations("animations/")

class Collision(Enum):
    TOP = 1
    RIGHT = 2
    LEFT = 3
    BOTTOM = 4
    NONE = 5

class Player:
    def __init__(self, entity):
        self.velocity = [0, 0]
        self.entity = entity
        self.arm = e.entity(entity.x + 3, entity.y + 15, 4, 4, "arm")
        self.arm_flip = False
        self.arm_angle = 0
        self.arm_velocity = [0, 0]
        self.is_arm_detached = False
        self.is_arm_stuck = False
        self.charge = 0
        self.charge_timer = 100
    
    def reset_arm(self):
        self.arm = e.entity(self.entity.x + 3, self.entity.y + 15, 4, 4, "arm")
        self.arm_flip = False
        self.arm_angle = 0
        self.arm_velocity = [0, 0]
        self.is_arm_detached = False
        self.is_arm_stuck = False
        self.charge = 0
    
    def move_arm(self, tiles):
        player.arm.x -= player.arm_velocity[0]
        player.arm.obj.rect.x = round(player.arm.x)
        block_collisions = e.collision_test(self.arm.obj.rect, tiles)
        for block in block_collisions:
            if (self.arm_velocity[0] < 0):
                self.arm.x = block.left - 8
                self.arm.y = block.top + 8
                self.arm.obj.rect.x = self.arm.x - self.arm.size_x / 2
                self.arm.obj.rect.y = self.arm.y
                return Collision.RIGHT
            elif (self.arm_velocity[0] > 0):
                self.arm.x = block.right + 8
                self.arm.y = block.top + 8
                self.arm.obj.rect.x = self.arm.x - self.arm.size_x / 2
                self.arm.obj.rect.y = self.arm.y
                return Collision.LEFT
            
        player.arm.y += player.arm_velocity[1]
        player.arm.obj.rect.y = round(player.arm.y)
        block_collisions = e.collision_test(self.arm.obj.rect, tiles)
        for block in block_collisions:
            if (self.arm_velocity[1] < 0):
                self.arm.y = block.bottom + self.arm.size_x / 2
                self.arm.x = block.left + 8
                self.arm.obj.rect.x = self.arm.x
                self.arm.obj.rect.y = self.arm.y
                return Collision.TOP
            elif (self.arm_velocity[1] > 0):
                self.arm.y = block.top - self.arm.size_x / 2
                self.arm.x = block.left + 8
                self.arm.obj.rect.x = self.arm.x
                self.arm.obj.rect.y = self.arm.y
                return Collision.BOTTOM
        
        return Collision.NONE
    

player_entity = e.entity(0, 0 - (player_image.get_height()/2), player_image.get_width(), player_image.get_height(), "player")
player = Player(player_entity)

while True:
    display.fill((0,0,0))
    true_scroll[0] += (player.entity.x - true_scroll[0] - 150 + int(player.entity.size_x / 2))/20
    true_scroll[1] += (player.entity.y - true_scroll[1] - 100 + int(player.entity.size_y / 2))/20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])
    tile_rects = []

    mx, my = ((pygame.mouse.get_pos()[0] - 150 + scroll[0]),(pygame.mouse.get_pos()[1] - 100 + scroll[1]))

    load_map(tile_rects, scroll)

    mouse_arm_diff_y = my-player.arm.y
    mouse_arm_diff_x = mx-player.arm.x
    mouse_angle = math.atan2((mouse_arm_diff_y),(mouse_arm_diff_x)) - (math.pi/2)
    
    if (math.degrees(mouse_angle) < 0 and math.degrees(mouse_angle) > -180):
        player.entity.flip = False
    else:
        player.entity.flip = True

    player.velocity = [0,0]
    if (moving_right):
        player.velocity[0] = 2
        player.entity.set_flip(False)
        player.entity.set_action("run")
        player.entity.flip = False
    if (moving_left):
        player.velocity[0] = -2
        player.entity.set_flip(True)
        player.entity.set_action("run")
        player.entity.flip = True
    if (moving_left == False and moving_right == False):
        player.entity.set_action("idle")

    player.velocity[1] += player_y_velocity
    player_y_velocity += 0.2
    if (player_y_velocity > 3):
        player_y_velocity = 3

    if (player.is_arm_detached == False and player.is_arm_stuck == False):
        player.arm_angle = math.degrees(mouse_angle)
        if (player.arm_flip):
            player.arm_angle += player.charge
        if (player.arm_flip == False):
            player.arm_angle -= player.charge
            player.arm_angle = -player.arm_angle
    elif (player.is_arm_detached):
        player.arm_angle -= 20
    else:
        player.arm_velocity = [0, 0]
        
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_UP:
                if air_timer < 6:
                    player_y_velocity = -5
            if event.key == K_r:
                player.reset_arm()
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False
        if event.type == MOUSEBUTTONDOWN:
            if player.charge_timer > 100:
                player.charge_timer = 0
                charging_throw = True
        if event.type == MOUSEBUTTONUP:
            charging_throw = False
            player.arm_velocity[0] = math.sin(mouse_angle) * 4
            player.arm_velocity[1] = math.cos(mouse_angle) * 4

    player.charge_timer += 1

    if (charging_throw):
        if (player.charge != 100):
            player.charge += 5
    else:
        if (player.charge <= 0):
            player.charge = 0
        else:
            player.charge -= 25
            if (player.charge == 0):
                player.is_arm_detached = True

    player_pos_before = [player.entity.x, player.entity.y].copy()
    player_collisions = player.entity.move(player.velocity, tile_rects)
    if (player.is_arm_detached == False and player.is_arm_stuck == False):
        player_pos_dif = (player.entity.x - player_pos_before[0], player.entity.y - player_pos_before[1])
        player.arm.x += player_pos_dif[0]
        player.arm.y += player_pos_dif[1]
        player.arm.obj.rect.x += player_pos_dif[0]
        player.arm.obj.rect.y = player.arm.y
        if (player.arm_flip != player.entity.flip):
            player.arm_flip = player.entity.flip
            if (player.entity.flip == True):
                player.arm.x += 9
                player.arm.obj.rect.x = player.arm.x - player.arm.size_x
            elif (player.entity.flip == False):
                player.arm.x -= 9
                player.arm.obj.rect.x = player.arm.x

    elif (player.is_arm_detached and player.is_arm_stuck == False):
        arm_tiles_collision = player.move_arm(tile_rects)
        player.arm_velocity[1] += player_arm_gravity
        player_arm_gravity += 0.005
        if (player_arm_gravity > 0.1):
            player_arm_gravity = 0.1

        if (arm_tiles_collision != Collision.NONE):
            player.is_arm_detached = False
            player.is_arm_stuck = True

            if (player.arm_velocity[0] > 0):
                player.arm_flip = True
            if (player.arm_velocity[0] < 0):
                player.arm_flip = False

            if (arm_tiles_collision == Collision.LEFT or arm_tiles_collision == Collision.RIGHT): 
                player.arm_angle = 90
            elif (arm_tiles_collision == Collision.TOP): 
                player.arm_angle = 180
            elif (arm_tiles_collision == Collision.BOTTOM): 
                player.arm_angle = 0
                
            player.arm_velocity[0] = 0
            player.arm_velocity[1] = 0
            player_arm_gravity = 0
    else:
        player_arm_collision = player.entity.obj.rect.colliderect(player.arm.obj.rect)
        if (player_arm_collision):
            player_y_velocity = -6
            player.reset_arm()

    if player_collisions['bottom']:
        air_timer = 0
    else:
        air_timer += 1

    if player.entity.y > 100:
        player_entity = e.entity(0, 0 - (player_image.get_height()/2), player_image.get_width(), player_image.get_height(), "player")
        player = Player(player_entity)
    
    player.entity.change_frame(1)
    player.entity.display(display, scroll)
    player_arm_image_copy = pygame.transform.rotate(player_arm_image, player.arm_angle)
    player_arm_image_loc = [round(player.arm.x) - int(player_arm_image_copy.get_width() / 2), player.arm.y - int(player_arm_image_copy.get_height() / 2)]
    display.blit(pygame.transform.flip(player_arm_image_copy, player.arm_flip, False), (player_arm_image_loc[0]- scroll[0], player_arm_image_loc[1] - scroll[1]))

    ## ARM HITBOX
    # arm_rect = player.arm.obj.rect.copy()
    # arm_rect.x = player.arm.obj.rect.x - scroll[0]
    # arm_rect.y = player.arm.obj.rect.y - scroll[1]
    # pygame.draw.rect(display, (255, 0, 0) , arm_rect)

    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0,0))
    pygame.display.update()
    clock.tick(60)