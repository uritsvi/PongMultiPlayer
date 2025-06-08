import pickle

from common.common import SEP
from common.game_events import GameEventEntityCreated, GameEventEntityDestroyed, GameEventEntityUpdated
from common.pickle_base64 import pickle_dumps_base64


class SendPlayerEvents:
    def __init__(self, players_tunnels):
        self.players_tunnels = players_tunnels
        self.events = []

    def send_player_entity_created(self, entity):
        self.events.append(GameEventEntityCreated(entity))

    def send_player_entity_destroyed(self, entity):
        self.events.append(GameEventEntityDestroyed(entity))

    def send_player_entity_updated(self, entity):
        self.events.append(GameEventEntityUpdated(entity))

    def finish_frame(self):
        out = b""
        for event in self.events:
            event_dmp = pickle_dumps_base64(event)
            out += event_dmp + SEP.encode()

        for player_tunnel in self.players_tunnels:
            player_tunnel.get_send_tunnel().push_data(out)

        self.events.clear()