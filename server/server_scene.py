from common.base_scene import BaseScene
from send_player_events import SendPlayerEvents


class ServerScene:
    def __init__(self, send_player_events: SendPlayerEvents):
        self.base_scene = BaseScene()
        self.send_player_events = send_player_events

    def add_entity(self, entity):
        self.base_scene.add_entity(entity)
        self.send_player_events.send_player_entity_created(entity)

    def destroy_entity(self, entity):
        self.base_scene.remove_entity(entity.id)
        self.send_player_events.send_player_entity_destroyed(entity)

    def update(self, inputs):
        for entity in self.base_scene.get_entities():
            entity.update(inputs)
            self.send_player_events.send_player_entity_updated(entity)
        self.send_player_events.finish_frame()

    def render(self, window):
        for entity in self.base_scene.get_entities():
            entity.render(window)