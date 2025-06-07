from common.entity import Entity
from common.vec2 import Vec2


class Ball(Entity):
    def __init__(self):
        super().__init__()

    def update(self, inputs):
        self.x += 1
        self.y += 1

    def render(self, window):
        print("Render Ball", self.x, self.y)