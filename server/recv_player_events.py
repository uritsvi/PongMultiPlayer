from common.common import USER_EVENTS_LIST_MSG, SEP
from common.pickle_base64 import pickle_loads_base64


class RecvPlayerEvents:
    def __init__(self, players_tunnels, number_of_players):
        self.players_tunnels = players_tunnels
        self.number_of_players = number_of_players

    def get_player_events(self):
        inputs = [None] * self.number_of_players
        for i, player_tunnel in enumerate(self.players_tunnels):
            if player_tunnel.get_recv_tunnel().have_new_data():
                data = player_tunnel.get_recv_tunnel().pull_data()
                if data.startswith(USER_EVENTS_LIST_MSG.encode()):
                    events = data.split(SEP.encode())[1:-1]
                    all_input = []
                    for event in events:
                        all_input.append(pickle_loads_base64(event))
                    inputs[i] = all_input

        return inputs

