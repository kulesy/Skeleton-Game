import json

class PhysicsConstants():
    def __init__(self):
        with open('physics_constants.json', 'r') as f:
            physics_json = json.load(f)
            self.gravity = physics_json["gravity"]
            self.friction = physics_json["friction"]
            self.terminal_velocity = physics_json["terminalVelocity"]