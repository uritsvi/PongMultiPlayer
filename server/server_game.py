import pickle
import socket
import time
from typing import List

from common.common import EVENTS_LIST_MSG, SEP
from common.networking import Networking
from common.player_tunnels import PlayerTunnels
from common.scence_builders.pong_builder import build_pong_scene


class Game:
    def __init__(self, number_of_players):
        self.players_tunnels: List[PlayerTunnels] = []
        self.number_of_players = number_of_players
        self.current_scene = build_pong_scene()

    def create_conn(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('', 0))
        port = sock.getsockname()[1]

        return sock, port

    def create_player_tunnels(self):
        send, send_port = self.create_conn()
        recv, recv_port = self.create_conn()

        self.players_tunnels.append(PlayerTunnels(Networking(send), Networking(recv)))

        return send_port, recv_port

    def allocate_ports(self):
        out = []

        for i in range(0, self.number_of_players):
            ports = self.create_player_tunnels()
            out.append(ports)

        return out

    def wait_for_connections(self):
        for player_tunnels in self.players_tunnels:
            player_tunnels.wait_for_connection()
            player_tunnels.start_tunnels()

    def run(self):
        self.wait_for_connections()
        print("All sockets are connected")

        while True:

            inputs = [None] * self.number_of_players
            for i, player_tunnel in enumerate(self.players_tunnels):
                if player_tunnel.get_recv_tunnel().have_new_data():
                    data = player_tunnel.get_recv_tunnel().pull_data()
                    if data.startswith(EVENTS_LIST_MSG.encode()):
                        events = data.split(SEP.encode())[1:-1]
                        all_input = []
                        for event in events:
                            all_input.append(pickle.loads(event))
                        inputs[i] = all_input

            time.sleep(0.5)


            self.current_scene.update(inputs)