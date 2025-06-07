from common.entity import Entity
from common.vec2 import Vec2


class Ball(Entity):
    SPEED = 0.1

    def __init__(self):
        super().__init__()
        self.direction = Vec2(-1, -1)  # Initial direction of the ball

    def update(self, inputs):
        self.position += self.direction * self.SPEED

    def render(self, window):
        print("Render Ball", self.position)