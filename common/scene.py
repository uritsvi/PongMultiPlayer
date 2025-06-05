class Scene:
    def __init__(self):
        self.__entities = []

    def add_entity(self, entity):
        self.__entities.append(entity)

    def update(self, inputs):
        for entity in self.__entities:
            entity.update(inputs)

    def render(self, window):
        for entity in self.__entities:
            entity.render(window)