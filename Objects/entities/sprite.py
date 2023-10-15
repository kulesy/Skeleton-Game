import json

from pygame import Surface
import pygame
from enums.global_enums import ActionEnum

from models.animation_action import AnimationAction
from objects.entities.entity import Entity


class Sprite(object):
    def __init__(self, entity, type):
        self.entity: Entity = entity
        self.type = type
        self.action_state = ActionEnum.IDLE
        self.current_frame_index = 0
        self.frame_hold__count = 0
        self.animation_actions = self.get_animation_actions(type)
        self.current_frame = self.get_current_frame()
        entity.width = self.current_frame.get_width()
        entity.height = self.current_frame.get_height()

    def get_current_frame(self):
        animation_action: AnimationAction = self.animation_actions[self.action_state]
        current_frame = animation_action.frames[self.current_frame_index]
        if (self.frame_hold__count >= animation_action.frameHold - 1):
            self.frame_hold__count = 0
            if (self.current_frame_index >= animation_action.numberOfFrames - 1):
                if (animation_action.isLoop):
                    self.current_frame_index = 0
            else:
                self.current_frame_index += 1
        else:
            self.frame_hold__count += 1
        
        current_frame_flipped = pygame.transform.flip(current_frame, self.entity.is_flipped, False)
        return current_frame_flipped

    def get_animation_actions(self, type: str) -> dict[ActionEnum, AnimationAction]:
        animations_path = f'assets/animations/{type}'
        animationActions: dict[ActionEnum, AnimationAction] = {}

        with open(f'{animations_path}/animation_action_settings.json', 'r') as f:
            animation = json.load(f)
            for action in animation:
                frames: list[Surface] = []
                for frameNumber in range(animation[action]["numberOfFrames"]):
                    frame = pygame.image.load(f"{animations_path}/{action}/{frameNumber}.png").convert()
                    frame.set_colorkey((0,0,0))
                    frames.append(frame)
                
                animationActions[ActionEnum(animation[action]["state"])] = AnimationAction(frames,
                                                           animation[action]["numberOfFrames"],
                                                           animation[action]["frameHold"],
                                                           animation[action]["isLoop"])
        
        return animationActions
    
    def set_action(self, action_state):
        if (self.action_state == action_state):
            return
        
        self.action_state = action_state
        self.current_frame_index = 0
        self.frame_hold__count = 0