import pygame, math

class Cursor:
    def __init__(self, window_size, screen_zoom):
        self.display_size: tuple[int, int] = ((window_size[0] / screen_zoom, window_size[1] / screen_zoom))
        self.mouse_pos: tuple[int, int] = (0,0)

    def get_mouse_angle_rad(self, scroll, target_pos) -> float:
        self.mouse_pos = ((pygame.mouse.get_pos()[0] - 150 + scroll[0]),(pygame.mouse.get_pos()[1] - 100 + scroll[1]))
        diff_x = self.mouse_pos[0] - target_pos[0]
        diff_y = self.mouse_pos[1] - target_pos[1]
        mouse_angle = math.atan2((diff_y),(diff_x))

        return mouse_angle