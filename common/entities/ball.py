import pygame.color

from common.entity import Entity
from common.vec2 import Vec2


class Ball(Entity):
    SPEED = 0.01
    WIDTH = 0.075/2
    HEIGHT = 0.1/2

    def __init__(self, paddle_1, paddle_2):
        super().__init__()
        self.direction = Vec2(-0.5, -1)  # Initial direction of the ball
        self.paddle_1 = paddle_1
        self.paddle_2 = paddle_2

    def ball_in_screen_y(self, pos):
        if pos.y - self.HEIGHT <= -1 or pos.y + self.HEIGHT >= 1:
            return False
        return True

    def ball_outside_screen_x(self, pos):
        if pos.x + self.WIDTH <= -1 or pos.x - self.WIDTH >= 1:
            return True
        return False

    def intersect_left_paddle(self, pos, paddle):
        if (paddle.position.x - paddle.WIDTH <= pos.x - self.WIDTH <= paddle.position.x + paddle.WIDTH and
                paddle.position.y - paddle.HEIGHT <= pos.y <= paddle.position.y + paddle.HEIGHT):
            return True
        return False

    def intersect_right_paddle(self, pos, paddle):
        if (paddle.position.x - paddle.WIDTH <= pos.x + self.WIDTH <= paddle.position.x + paddle.WIDTH and
                paddle.position.y - paddle.HEIGHT <= pos.y <= paddle.position.y + paddle.HEIGHT):
            return True
        return False

    def update(self, inputs, current_scene):
        next_pos = self.position + self.direction * self.SPEED
        if self.ball_in_screen_y(next_pos):
            if self.ball_outside_screen_x(next_pos):
                current_scene.destroy_entity(self)
                current_scene.add_entity(Ball(self.paddle_1, self.paddle_2))  # Reset the ball
                return False

            if self.intersect_left_paddle(next_pos, self.paddle_1) or self.intersect_right_paddle(next_pos, self.paddle_2):
                self.direction.x *= -1

            self.position = next_pos
        else:
            self.direction.y *= -1  # Reverse the vertical direction if it goes out of bounds
            self.update(inputs, current_scene) # Retry the update with the new direction
        return True

    def render(self, window):
        window.draw_rect(self.position.x, self.position.y, self.WIDTH, self.HEIGHT, pygame.color.Color("white"))