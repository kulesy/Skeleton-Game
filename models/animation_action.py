from pygame import Surface

class AnimationAction():
    def __init__(self, frames: list[Surface], numberOfFrames: int, frameHold: int, isLoop: bool):
        self.frames: list[Surface] = frames
        self.numberOfFrames : int = numberOfFrames
        self.frameHold : int = frameHold
        self.isLoop : bool = isLoop