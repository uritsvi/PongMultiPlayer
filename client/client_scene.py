from common.base_scene import BaseScene
from common.common import SEP
from common.pickle_base64 import pickle_loads_base64


class ClientScene:
    def __init__(self, player_tunnel):
        self.player_tunnel = player_tunnel
        self.base_scene = BaseScene()

    def handle_server_events(self):
        events = self.player_tunnel.get_recv_tunnel().pull_data()
        while self.player_tunnel.get_recv_tunnel().have_new_data():
            events += self.player_tunnel.get_recv_tunnel().pull_data()

        if events is None:
            return

        events = events.split(SEP.encode())[:-1]
        for event in events:
            event = pickle_loads_base64(event)
            event.apply_to_client(self.base_scene)



    def update_game(self, window):
        self.handle_server_events()
        for entity in self.base_scene.get_entities():
            entity.render(window)