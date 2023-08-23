import pygame
from objects.physics_constants import PhysicsConstants

from scripts.text import Font

from objects.controls import Controls
from objects.cursor import Cursor
from objects.map import Map
from objects.player import Player 
clock = pygame.time.Clock()

pygame.init()

pygame.display.set_caption('Skeleton Arm')

WINDOW_SIZE = (600, 400)

screen_zoom = 2

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface((WINDOW_SIZE[0] / screen_zoom, WINDOW_SIZE[1] / screen_zoom))

physics_constants = PhysicsConstants()
friction = 0.2
terminal_velocity = 3

map = Map(16)

jump_height = 50
player_image = pygame.image.load('assets/animations/player/idle/0.png')

font = Font("assets/fonts/large_font.png", (255,255,255))

spawn_points = [[12,4]]
player = Player(spawn_points[0], map)
cursor = Cursor(WINDOW_SIZE, screen_zoom)
controls = Controls()

while True:
    display.fill((0,0,0))
    map.update_scroll_pos(player.x, player.y, player.width, player.height)

    map.render(display)
    
    controls.handle_controls_events(pygame.event.get())

    mouse_angle = cursor.get_mouse_angle_rad(map.scroll, (player.arm.x, player.arm.y))

    player.update_arm_state(mouse_angle)

    player.handle_charging_throw(display, map.scroll, controls.is_charging_throw, mouse_angle)
        
    if (controls.is_respawning):
        current_spawn_point = spawn_points[0]
        for spawn_point in spawn_points:
            if (player.y <= spawn_point[1] * 16):
                current_spawn_point = spawn_point
        player = Player(current_spawn_point, map)
        controls.is_respawning = False

    if (player.y > 100):
        player = Player(spawn_points[0], map)

    ## ARM HITBOX
    arm_rect = player.arm.rect.copy()
    arm_rect.x = player.arm.rect.x - map.scroll[0]
    arm_rect.y = player.arm.rect.y - map.scroll[1]
    pygame.draw.rect(display, (255, 0, 0) , arm_rect)

    if (controls.is_moving_left): 
        player.velocity[0] = -2
    elif (controls.is_moving_right): 
        player.velocity[0] = 2

    if (controls.is_jumping):
        player.jump()
        controls.is_jumping = False

    player.move(map.tile_rects)
    player.move_arm(map.tile_rects, mouse_angle)
    player.render(display, map.scroll)

    if (pygame.time.get_ticks() < 3000):
        font.render("Press R to restart", display, (150 - (font.width("Press R to restart")/2) , 40))

    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0,0))
    pygame.display.update()
    clock.tick(60)