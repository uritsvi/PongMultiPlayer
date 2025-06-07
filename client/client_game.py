import pickle
import time

from common.common import SERVER_ADDRESS, EVENTS_LIST_MSG, SEP
from common.networking import Networking
from common.player_tunnels import PlayerTunnels
from common.scence_builders.pong_builder import build_pong_scene
from window import Window


class Game:
    def __init__(self, send_port, recv_port):
        self.send_port = send_port
        self.recv_port = recv_port

        self.player_tunnels: PlayerTunnels = None

        self.window = Window()
        self.current_scene = build_pong_scene()


    def connect_tunnels(self):
        send_conn = Networking(Networking.create_sock(SERVER_ADDRESS, int(self.send_port)))
        recv_conn = Networking(Networking.create_sock(SERVER_ADDRESS, int(self.recv_port)))

        self.player_tunnels = PlayerTunnels(
            send_conn,
            recv_conn,
            server=False
        )
        self.player_tunnels.start_tunnels()

    def send_events(self, events):
        out = f"{EVENTS_LIST_MSG}{SEP}".encode()
        for event in events:
            out += pickle.dumps(event) + SEP.encode()
            print("New evevnt")

        if len(events) > 0:
            self.player_tunnels.get_send_tunnel().push_data(out)


    def run(self):
        print("Game started")
        self.window.create()
        self.connect_tunnels()

        while self.window.is_running():
            events = self.window.poll_events()
            self.send_events(events)

            self.window.render()

            print("aaaaaaaaa")
            time.sleep(0.5)

        self.window.close()
        print("Game ended")