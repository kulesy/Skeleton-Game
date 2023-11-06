import pygame
from enums.global_enums import ActionEnum, ArmStateEnum

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

friction = 0.2
terminal_velocity = 3

map = Map(16, display)

jump_height = 50
player_image = pygame.image.load('assets/animations/player/idle/0.png')

font = Font("assets/fonts/large_font.png", (255,255,255))

spawn_points = [[12,4]]
player = Player(map)
cursor = Cursor(WINDOW_SIZE, screen_zoom)
controls = Controls()

while True:
    display.fill((0,0,0))
    map.update_scroll_pos(player.entity.x, player.entity.y, player.entity.width, player.entity.height)

    map.render()
    
    controls.handle_controls_events(pygame.event.get())

    mouse_angle = cursor.get_mouse_angle_rad(map.scroll, (player.entity.x + player.arm_offset[0], player.entity.y + player.arm_offset[1]))

    player.arm_left.update_arm_state(mouse_angle)
    player.arm_right.update_arm_state(mouse_angle)

    player.handle_charging_throw(controls.is_charging_throw, mouse_angle, player.arm_left)
    if (player.arm_left.arm_state != ArmStateEnum.ATTACHED):
        player.handle_charging_throw(controls.is_charging_throw, mouse_angle, player.arm_right)
        
    if (controls.is_respawning):
        current_spawn_point = spawn_points[0]
        for spawn_point in spawn_points:
            if (player.entity.y <= spawn_point[1] * 16):
                current_spawn_point = spawn_point
        player.reset_player()
        controls.is_respawning = False

    if (player.entity.y > 1000):
        player.reset_player()

    if (controls.is_moving_left): 
        player.movable.velocity[0] = -2
    elif (controls.is_moving_right): 
        player.movable.velocity[0] = 2

    if ((controls.is_moving_left or controls.is_moving_right) and 
        player.air_timer == 0):
        player.sprite.set_action(ActionEnum.MOVING)
    elif (player.air_timer == 0):
        player.sprite.set_action(ActionEnum.IDLE)

    if (controls.is_jumping):
        player.sprite.set_action(ActionEnum.JUMPING)
        player.jump()
        controls.is_jumping = False

    player.move(mouse_angle)
    player.arm_left.move_arm()
    player.arm_right.move_arm()
    player.handle_render()

    if (pygame.time.get_ticks() < 3000):
        font.render("Press R to restart", display, (150 - (font.width("Press R to restart")/2) , 40))

    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0,0))
    pygame.display.update()
    clock.tick(60)