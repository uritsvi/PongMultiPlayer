import pickle

from client_scene import ClientScene
from common.common import SERVER_ADDRESS, USER_EVENTS_LIST_MSG, SEP
from common.fps import Fps
from common.networking import Networking
from common.player_tunnels import PlayerTunnels
from window import Window


class Game:
    def __init__(self, send_port, recv_port):
        self.send_port = send_port
        self.recv_port = recv_port

        self.player_tunnels: PlayerTunnels = None

        self.window = Window()


    def connect_tunnels(self):
        send_conn = Networking(Networking.create_sock(SERVER_ADDRESS, int(self.send_port)))
        recv_conn = Networking(Networking.create_sock(SERVER_ADDRESS, int(self.recv_port)))

        self.player_tunnels = PlayerTunnels(
            send_conn,
            recv_conn,
            server=False
        )
        self.player_tunnels.start_tunnels()

    def send_events_to_server(self, events):
        out = f"{USER_EVENTS_LIST_MSG}{SEP}".encode()
        for event in events:
            out += pickle.dumps(event) + SEP.encode()

        if len(events) > 0:
            self.player_tunnels.get_send_tunnel().push_data(out)


    def poll_events_from_server(self):
        events = self.player_tunnels.get_recv_tunnel().pull_data()
        return events

    def run(self):
        print("Game started")
        self.window.create()
        self.connect_tunnels()

        scene = ClientScene(self.player_tunnels)
        fps = Fps()

        while self.window.is_running():
            fps.start_frame()

            events = self.window.poll_events()
            self.send_events_to_server(events)

            scene.update_game(self.window)
            self.window.render()

            fps.end_frame()


        self.window.close()
        print("Game ended")