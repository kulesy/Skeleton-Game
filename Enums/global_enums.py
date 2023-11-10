from enum import Enum

class DirectionEnum(Enum):
    NONE = 0
    UP = 1
    RIGHT = 2
    LEFT = 3
    DOWN = 4

class CollisionEnum(Enum):
    NONE = 0
    TOP = 1
    RIGHT = 2
    LEFT = 3
    BOTTOM = 4

class PlatformEnum(Enum):
    TOP = 1
    RIGHT = 2
    LEFT = 3
    BOTTOM = 4

class ActionEnum(Enum):
    IDLE = 0
    MOVING = 1
    JUMPING = 2

class ArmStateEnum(Enum):
    ATTACHED = 0
    DETACHED = 1
    STUCK = 2

class AxisEnum(Enum):
    X = 0
    Y = 1