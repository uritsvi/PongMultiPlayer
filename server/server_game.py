import socket
from typing import List

from common.fps import Fps
from common.networking import Networking
from common.player_tunnels import PlayerTunnels
from recv_player_events import RecvPlayerEvents
from pong_builder import build_pong_scene
from send_player_events import SendPlayerEvents


class Game:
    def __init__(self, number_of_players):
        self.players_tunnels: List[PlayerTunnels] = []
        self.number_of_players = number_of_players

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

        send_player_events = SendPlayerEvents(self.players_tunnels)
        recv_player_events = RecvPlayerEvents(self.players_tunnels, self.number_of_players)

        self.current_scene = build_pong_scene(send_player_events)
        fps = Fps()

        while True:
            fps.start_frame()

            inputs = recv_player_events.get_player_events()
            self.current_scene.update(inputs)

            fps.end_frame()

