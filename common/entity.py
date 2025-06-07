from abc import abstractmethod

from common.vec2 import Vec2

NEXT_ID = 0


class Entity:

    def __init__(self):
        self.position = Vec2(0, 0)

        global NEXT_ID

        self.id = NEXT_ID
        NEXT_ID += 1

    @abstractmethod
    def update(self, inputs, current_scene):
        raise NotImplementedError("This method should be overridden by subclasses.")

    @abstractmethod
    def render(self, window):
        raise NotImplementedError("This method should be overridden by subclasses.")

