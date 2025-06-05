import socket
import threading
import traceback

from common.common import SEP, MATCH_MAKER_CREATE_ROOM, MATCH_MAKER_JOIN_ROOM, ERROR, SUCCESS, MATCH_MAKER_PORT
from common.networking import Networking
from sessions import Sessions


class ConnectionManager:
    def __init__(self):
        self.__sessions = Sessions()

    def handle_req(self, conn: Networking):
        try:
            req = conn.receive()
            if req is None:
                print("Connection closed by client")
                return

            session_id = None
            req_params = req.decode().split(SEP)  # Assuming the request is a string, decode it
            if req_params[0] == MATCH_MAKER_CREATE_ROOM:
                session_id = self.__sessions.create(conn)
                conn.send(session_id.encode())
            elif req_params[0] == MATCH_MAKER_JOIN_ROOM:
                session_id = req_params[1]
                if not self.__sessions.connect_to_existing(session_id, conn):
                    raise Exception("Room not found or full")

            assert session_id is not None, "Session ID should not be None"
            ready = self.__sessions.get_session(session_id).run_if_ready()
            if ready:
                self.__sessions.remove_from_connect_session(session_id)

            print("Client connected to session:", session_id)

        except Exception as e:
            print(f"Error receiving data: {traceback.format_exc()}")
            conn.send(ERROR.encode())

    def run(self):
        listen_socket = socket.socket()
        listen_socket.bind(("0.0.0.0", MATCH_MAKER_PORT))
        listen_socket.listen(20)

        while True:
            print("Waiting for connection...")
            try:
                client_socket, addr = listen_socket.accept()
                print("accepted")
                threading.Thread(target=self.handle_req, args=(Networking(client_socket),)).start()
            except Exception as e:
                print(f"Error accepting connection: {traceback.format_exc()}")
                continue