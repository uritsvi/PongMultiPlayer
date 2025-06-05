from connection_manager import ConnectionManager


class Server:
    def __init__(self):
        self.connection_manager = ConnectionManager()

    def run(self):
        self.connection_manager.run()