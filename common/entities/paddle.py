from copy import deepcopy

import pygame.color

from common.entity import Entity
from common.input import KEY_UP_TYPE, KEY_DOWN_TYPE
from common.vec2 import Vec2


class Paddle(Entity):
    UP_KEY= "w"
    DOWN_KEY = "s"

    WIDTH = 0.05
    HEIGHT = 0.2
    SPEED = 0.05

    def __init__(self, input_index):
        super().__init__()
        if input_index == 0:
            self.position = Vec2(-0.9, 0)
        elif input_index == 1:
            self.position = Vec2(0.9, 0)
        else:
            raise ValueError("Invalid input index for Paddle. Must be 0 or 1.")

        self.up = False
        self.down = False

        self.input_index = input_index

    def update_input(self, my_input):
        for current_input in my_input:
            if current_input.get_type() == KEY_UP_TYPE and current_input.get_key() == self.UP_KEY:
                self.up = False
            elif current_input.get_type() == KEY_DOWN_TYPE and current_input.get_key() == self.UP_KEY:
                self.up = True
            elif current_input.get_type() == KEY_UP_TYPE and current_input.get_key() == self.DOWN_KEY:
                self.down = False
            elif current_input.get_type() == KEY_DOWN_TYPE and current_input.get_key() == self.DOWN_KEY:
                self.down = True

    def position_in_screen(self, position):
        return -1 <= position.y - self.HEIGHT and position.y + self.HEIGHT <= 1

    def update(self, inputs, current_scene):
        print(inputs)
        my_input = inputs[self.input_index]
        if my_input is not None:
            self.update_input(my_input)

        next_pos = deepcopy(self.position)
        if self.up:
            print("Moving paddle up")
            next_pos.y += self.SPEED
        if self.down:
            print("Moving paddle down")
            next_pos.y -= self.SPEED
        if self.position_in_screen(next_pos):
            self.position = next_pos

        return True


    def render(self, window):
        window.draw_rect(self.position.x, self.position.y, self.WIDTH, self.HEIGHT, pygame.color.Color("white"))