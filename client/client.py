import os

import connect_screen
from client_game import Game

class Client:
    def run(self):
        send_port, recv_port = connect_screen.ConnectScreen().run()
        Game(send_port, recv_port).run()

