import os

import connect_screen
from client_game import Game

class Client:
    def run(self):
        send_port, recv_port = connect_screen.ConnectScreen().run()
        if send_port is None or recv_port is None:
            print("Failed to connect to the server.")
            return

        Game(send_port, recv_port).run()

