import tkinter as tk
import threading
import socket

from client_game import Game
from common import common
from common.common import MATCH_MAKER_CREATE_ROOM, MATCH_MAKER_PORT, SERVER_ADDRESS, SEP, MATCH_MAKER_JOIN_ROOM, \
    MATCH_MAKER_GAME_START
from common.networking import Networking


# Simulated backend functions
def create_room():
    print("Trying to create a room...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_ADDRESS, MATCH_MAKER_PORT))

    conn = Networking(sock)
    conn.send(MATCH_MAKER_CREATE_ROOM.encode())

    session_id = conn.receive().decode().strip()

    print("Connected to match maker server.", session_id)
    return session_id, conn


def connect_to_room(room_id):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_ADDRESS, MATCH_MAKER_PORT))

    conn = Networking(sock)
    conn.send(f"{MATCH_MAKER_JOIN_ROOM}{SEP}{room_id}".encode())

    return conn


class ConnectScreen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Room App")
        self.root.geometry("500x300")
        self.main_screen()
        self.send_port = None
        self.recv_port = None

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def main_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Select an Option", font=("Arial", 14)).pack(pady=20)
        tk.Button(self.root, text="Create Room", command=self.create_room_screen, width=20).pack(pady=5)
        tk.Button(self.root, text="Connect to Room", command=self.connect_room_screen, width=20).pack(pady=5)

    def show_error(self, message):
        self.clear_screen()
        tk.Label(self.root, text="Error:", font=("Arial", 12), fg="red").pack(pady=10)
        tk.Label(self.root, text=message, wraplength=250).pack(pady=5)
        tk.Button(self.root, text="Back to Start", command=self.main_screen).pack(pady=10)

    def get_ports(self, game_started):

        game_started = str(game_started.decode())
        if not game_started.startswith(MATCH_MAKER_GAME_START):
            raise Exception("Game start message not received correctly")

        send_port = game_started.split(SEP)[1]
        recv_port = game_started.split(SEP)[2]

        return send_port, recv_port

    def wait_for_game_start(self, conn):
        game_started = conn.receive()
        self.send_port, self.recv_port = self.get_ports(game_started)
        self.root.after(0, self.root.destroy)

    def create_room_screen(self):
        self.clear_screen()
        label = tk.Label(self.root, text="Creating Room...", font=("Arial", 12))
        label.pack(pady=10)
        spinner = tk.Label(self.root, text="⏳", font=("Arial", 32))
        spinner.pack(pady=10)

        def task():
            try:
                room_id, conn = create_room()
                self.clear_screen()
                tk.Label(self.root, text="Room Created!", font=("Arial", 14)).pack(pady=10)
                tk.Label(self.root, text="Room ID:", font=("Arial", 12)).pack(pady=5)
                room_id_entry = tk.Entry(self.root, font=("Arial", 16), fg="blue", justify="center")
                room_id_entry.insert(0, room_id)
                room_id_entry.config(state="readonly")
                room_id_entry.pack(pady=10)

                self.wait_for_game_start(conn)

            except Exception as e:
                self.show_error(str(e))

        threading.Thread(target=task).start()

    def connect_room_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Enter Room ID", font=("Arial", 12)).pack(pady=10)
        room_id_entry = tk.Entry(self.root)
        room_id_entry.pack(pady=5)

        def submit():
            room_id = room_id_entry.get().strip()
            self.clear_screen()
            label = tk.Label(self.root, text="Connecting...", font=("Arial", 12))
            label.pack(pady=10)
            spinner = tk.Label(self.root, text="🔄", font=("Arial", 32))
            spinner.pack(pady=10)

            def connect_task():
                try:
                    conn = connect_to_room(room_id)
                    self.clear_screen()
                    tk.Label(self.root, text="Connected Successfully!", font=("Arial", 14), fg="green").pack(pady=10)
                    tk.Button(self.root, text="Back to Start", command=self.main_screen).pack(pady=10)

                    self.wait_for_game_start(conn)

                except Exception as e:
                    self.show_error(str(e))

            threading.Thread(target=connect_task).start()

        tk.Button(self.root, text="Connect", command=submit).pack(pady=10)
        tk.Button(self.root, text="Back to Start", command=self.main_screen).pack()

    """Returns the ip and port of the session to connect to."""
    def run(self):
        self.root.mainloop()


        return self.send_port, self.recv_port
