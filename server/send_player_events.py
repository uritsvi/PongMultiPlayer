import pickle

from common.common import SEP
from common.game_events import GameEventEntityCreated, GameEventEntityDestroyed, GameEventEntityUpdated


class SendPlayerEvents:
    def __init__(self, players_tunnels):
        self.players_tunnels = players_tunnels
        self.events = []

    def send_player_entity_created(self, entity):
        print("Creating GameEventEntityCreated for entity:", entity.id)
        self.events.append(GameEventEntityCreated(entity))

    def send_player_entity_destroyed(self, entity):
        print("Creating GameEventEntityDestroyed for entity:", entity.id)
        self.events.append(GameEventEntityDestroyed(entity))

    def send_player_entity_updated(self, entity):
        print("Creating GameEventEntityUpdated for entity:", entity.id)
        self.events.append(GameEventEntityUpdated(entity))

    def finish_frame(self):
        out = b""
        for event in self.events:
            event = pickle.dumps(event)
            out += event + SEP.encode()
        for player_tunnel in self.players_tunnels:
            player_tunnel.get_send_tunnel().push_data(out)

        self.events.clear()