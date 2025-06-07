from common.entity import Entity


class Ball(Entity):
    def update(self, inputs):
        print("Update ball", inputs)

    def render(self, window):
        print("Render Ball")