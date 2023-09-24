import pygame, sys
from pygame.locals import *

class Controls:
    def __init__(self):
        self.is_charging_throw: bool = False

        self.is_moving_left: bool = False
        self.is_moving_right: bool = False

        self.is_jumping: bool = False

        self.is_respawning: bool = False

        self.is_recalling: bool = False

    
    def handle_controls_events(self, events) -> None:
        for event in events:
            if (event.type == KEYDOWN):
                if (event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()

                if (event.key == K_a):
                    self.is_moving_left = True
                if (event.key == K_d):
                    self.is_moving_right = True
                if (event.key == K_w):
                    self.is_jumping = True
                if (event.key == K_v):
                    self.is_recalling = True
                    
            if (event.type == KEYUP):
                if (event.key == K_a):
                    self.is_moving_left = False
                if (event.key == K_d):
                    self.is_moving_right = False
                if (event.key == K_r):
                    self.is_respawning = True
                if (event.key == K_v):
                    self.is_recalling = False
            if (event.type == QUIT):
                pygame.quit()
                sys.exit()
            
            if (event.type == MOUSEBUTTONDOWN):
                if (event.button) == 1:
                    self.is_charging_throw = True
            if (event.type == MOUSEBUTTONUP):
                if (event.button) == 1:
                    self.is_charging_throw = False

        return