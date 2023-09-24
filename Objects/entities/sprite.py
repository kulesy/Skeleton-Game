import json

from pygame import Surface
import pygame

from models.animation_action import AnimationAction


class Sprite(object):
    def __init__(self, type):
        self.current_frame = self.get_current_frame()
        self.type = type
        self.animation_actions = self.get_animation_actions(type)
        self.action_id = 0
        self.current_frame_index = 0
        self.frame_hold__count = 0
        self.is_flipped = False

    def get_current_frame(self):
        animation_action: AnimationAction = self.animation_actions[self.action.name.lower()]
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
        
        current_frame_flipped = pygame.transform.flip(current_frame, self.is_flipped, False)
        return current_frame_flipped

    def get_animation_actions(self, type: str) -> dict[str, AnimationAction]:
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
    
    def set_action(self, action):
        if (self.action == action):
            return
        
        self.action = action
        self.current_frame_index = 0
        self.frame_hold__count = 0