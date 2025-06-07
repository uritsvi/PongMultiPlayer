import pygame.color

from common.entity import Entity
from common.vec2 import Vec2


class Ball(Entity):
    SPEED = 0.005
    WIDTH = 0.075/2
    HEIGHT = 0.1/2

    def __init__(self):
        super().__init__()
        self.direction = Vec2(-0.5, -1)  # Initial direction of the ball

    def ball_in_screen_y(self, pos):
        if pos.y - self.HEIGHT <= -1 or pos.y + self.HEIGHT >= 1:
            return False
        return True

    def ball_outside_screen_x(self, pos):
        if pos.x + self.WIDTH <= -1 or pos.x - self.WIDTH >= 1:
            return True
        return False

    def update(self, inputs, current_scene):
        next_pos = self.position + self.direction * self.SPEED
        if self.ball_in_screen_y(next_pos):
            if self.ball_outside_screen_x(next_pos):
                current_scene.destroy_entity(self)
                current_scene.add_entity(Ball())
                return False

            self.position = next_pos
        else:
            self.direction.y *= -1  # Reverse the vertical direction if it goes out of bounds
            self.update(inputs, current_scene) # Retry the update with the new direction
        return True

    def render(self, window):
        window.draw_rect(self.position.x, self.position.y, self.WIDTH, self.HEIGHT, pygame.color.Color("white"))