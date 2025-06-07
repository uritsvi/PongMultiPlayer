import os
import socket
import threading
import logging
import queue

import common.common as common
from common.networking import Networking


class Tunnel:
    def __init__(self, conn: Networking, sending):
        self.conn = conn

        self.sending = sending
        self.thread = None

        self.queue = queue.Queue()

    def start_tunnel(self):
        self.thread = threading.Thread(
            target=self.thread_worker,
            args=(self.conn, )
        ).start()

    def make_user_id(self):

        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)

        user_id = f"{local_ip}_{os.getpid()}"
        return user_id

    def sending_thread(self, networking: Networking):
        print("Start sending thread", networking.sock.getsockname())

        while True:
            data = self.queue.get()
            print("new data in tunnel")
            networking.send(data)
            logging.debug(f"Sent data from tunnel")

    def receiving_thread(self, networking: Networking):
        print("Start receiving thread", networking.sock.getsockname())

        while True:
            data = networking.receive()
            print("reacived")
            if data is None:
                logging.warning(f"Tunnel received None, closing tunnel")
                break
            logging.debug(f"Received data in tunnel ")
            self.queue.put(data)

    def thread_worker(self, networking: Networking):
        if self.sending:
          self.sending_thread(networking)
          return
        self.receiving_thread(networking)

    def push_data(self, data):
        assert self.sending

        print("pushing data to tunnel", self.conn.sock.getsockname())
        self.queue.put(data)

    def pull_data(self):
        assert not self.sending, "Tunnel type is sender"
        return self.queue.get_nowait()

    def have_new_data(self):
        return not self.queue.empty()

    def is_sending(self):
        return self.sending

    def wait_for_connection(self):
        print(self.sending, self.conn.sock.getsockname())

        self.conn = self.conn.wait_for_connection()
