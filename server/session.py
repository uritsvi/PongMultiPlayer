import threading

from common.common import MATCH_MAKER_GAME_START, SEP
from server_game import Game

from common.networking import Networking


class Session:
    NUMBER_OF_PLAYERS = 2

    def __init__(self):
        self.__clients = []

    def run(self):
        print("Run session")

        game = Game(self.NUMBER_OF_PLAYERS)
        ports = game.allocate_ports()
        for port_pair, client in zip(ports, self.__clients):
            print(f"Assigning port {port_pair[0]} to client {client}")
            client.send(
                f"{MATCH_MAKER_GAME_START}"
                f"{SEP}"
                f"{port_pair[0]}"
                f"{SEP}"
                f"{port_pair[1]}"
                f"".encode()
            )
        game.run()


    def is_ready(self) -> bool:
        """Check if the session is ready to run."""
        return len(self.__clients) == self.NUMBER_OF_PLAYERS

    def run_if_ready(self) -> bool:
        """Run the session if it is ready, return True if it was run, False otherwise."""
        if not self.is_ready():
            return False

        threading.Thread(target=self.run).start()
        return True

    def add_client(self, networking: Networking):
        print("Adding client")

        self.__clients.append(networking)
        return self.is_ready()

