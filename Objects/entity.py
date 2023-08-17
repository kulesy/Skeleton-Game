import json

from pygame import Surface
import pygame
from enums.global_enums import ActionEnum, DirectionEnum
from objects.models.animation_action import AnimationAction
from objects.physics_obj import PhysicsObj

class Entity(PhysicsObj):
    def __init__(self, x, y, width, height, img, type, isAnimated): # x, y, size_x, size_y, type
        super().__init__(x, y, width, height, img)
        self.animation_actions = self.get_animation_actions(type, isAnimated)
        self.flip = False
        self.action = ActionEnum.IDLE
        self.current_frame = 0
        self.frame_hold__count = 0

    def render(self, display: Surface, scroll: list[int]):
        animation_action: AnimationAction = self.animation_actions[self.action.name.lower()]
        frame = animation_action.frames[self.current_frame]
        if (self.frame_hold__count >= animation_action.frameHold - 1):
            self.frame_hold__count = 0
            if (self.current_frame >= animation_action.numberOfFrames - 1):
                if (animation_action.isLoop):
                    self.current_frame = 0
            else:
                self.current_frame += 1
        else:
            self.frame_hold__count += 1

        display.blit(pygame.transform.flip(frame, self.flip, False), (self.x - scroll[0], self.y - scroll[1]))
        
    def update_direction(self):
        if (self.velocity[0] > 0):
            self.direction = DirectionEnum.RIGHT
            self.flip = False
            self.set_action(ActionEnum.MOVING)
        elif (self.velocity[0] < 0):
            self.direction = DirectionEnum.LEFT
            self.flip = True
            self.set_action(ActionEnum.MOVING)
        elif (self.velocity[0] == 0):
            self.direction = DirectionEnum.NONE    
            self.set_action(ActionEnum.IDLE)
    
    def set_action(self, action):
        if (self.action == action):
            return
        
        self.action = action
        self.current_frame = 0
        self.frame_hold__count = 0


    def get_animation_actions(self, type: str, isAnimated: bool) -> dict[str, AnimationAction]:
        if (isAnimated == False):
            return {}

        animations_path = f'assets/animations/{type}'
        animationActions: dict[str, AnimationAction] = {}

        with open(f'{animations_path}/animation_action_settings.json', 'r') as f:
            animation = json.load(f)
            for action in animation:
                frames: list[Surface] = []
                for frameNumber in range(animation[action]["numberOfFrames"]):
                    frame = pygame.image.load(f"{animations_path}/{action}/{frameNumber}.png").convert()
                    frame.set_colorkey((0,0,0))
                    frames.append(frame)
                
                animationActions[action] = AnimationAction(frames,
                                                           animation[action]["numberOfFrames"],
                                                           animation[action]["frameHold"],
                                                           animation[action]["isLoop"])
        
        return animationActions