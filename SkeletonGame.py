import pygame
from Objects.Cursor import Cursor
import scripts.engine as e
import scripts.text as Text
import json
import math
from Objects.Controls import * 
from Objects.Map import * 
from Objects.Player import * 
from Enums.Collision import * 

clock = pygame.time.Clock()

from pygame.locals import *
pygame.init()

pygame.display.set_caption('Skeleton Arm')

WINDOW_SIZE = (600, 400)

screen_zoom = 2

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface((WINDOW_SIZE[0] / screen_zoom, WINDOW_SIZE[1] / screen_zoom))

friction = 0.2
gravity = 0.2
terminal_velocity = 3

with open('map.json', 'r') as f:
    map = Map(json.load(f), 16)

jump_height = 50
player_image = pygame.image.load('animations/player/idle/idle-1.png')

font = Text.Font("fonts/large_font.png", (255,255,255))

e.load_animations("animations/")

spawn_points = [[12,4]]
player_entity = e.entity(spawn_points[0][0] * 16, spawn_points[0][1] * 16 - (player_image.get_height()/2), player_image.get_width(), player_image.get_height(), "player")
player = Player(player_entity, friction, gravity, terminal_velocity)
cursor = Cursor(WINDOW_SIZE, screen_zoom)
controls = Controls()

while True:
    display.fill((0,0,0))
    map.render(display)

    map.update_scroll_pos(player)
    
    controls.handle_controls_events(pygame.event.get())

    mouse_angle = cursor.get_mouse_angle_rad(map.scroll, (player.arm.x, player.arm.y))

    arm_display_angle = mouse_angle - (math.pi/2)

    player.update_arm_state(arm_display_angle)

    player.handle_charging_throw(display, map.scroll, controls.is_charging_throw, mouse_angle)
        
    if (controls.is_respawning):
        current_spawn_point = spawn_points[0]
        for spawn_point in spawn_points:
            if (player.entity.y <= spawn_point[1] * 16):
                current_spawn_point = spawn_point
        player_entity = e.entity(current_spawn_point[0] * 16, current_spawn_point[1] * 16 - (player_image.get_height()/2), player_image.get_width(), player_image.get_height(), "player")
        player = Player(player_entity, friction, gravity, terminal_velocity)
        controls.is_respawning = False

    if (player.entity.y > 100):
        player_entity = e.entity(0, 0 - (player_image.get_height()/2), player_image.get_width(), player_image.get_height(), "player")
        player = Player(player_entity, friction, gravity, terminal_velocity)

    ## ARM HITBOX
    # arm_rect = player.arm.obj.rect.copy()
    # arm_rect.x = player.arm.obj.rect.x - map.scroll[0]
    # arm_rect.y = player.arm.obj.rect.y - map.scroll[1]
    # pygame.draw.rect(display, (255, 0, 0) , arm_rect)

    if (controls.is_moving_left): 
        player.velocity[0] = -2
    elif (controls.is_moving_right): 
        player.velocity[0] = 2

    if (controls.is_jumping):
        player.jump()
        controls.is_jumping = False

    player.move(map.tile_rects, mouse_angle)
    player.render(display, map.scroll)

    if (pygame.time.get_ticks() < 3000):
        font.render("Press R to restart", display, (150 - (font.width("Press R to restart")/2) , 40))

    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0,0))
    pygame.display.update()
    clock.tick(60)