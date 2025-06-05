import os
import socket
import threading
import logging
import queue

import common.common as common
from common.networking import Networking


class Tunnel:
    def __init__(self, conn: Networking, sending, networking=None):
        self.__conn = conn

        self.__sending = sending
        self.__thread = None

        self.__queue = queue.Queue()

        if networking is not None:
            self.__init_tunnel(networking)

    def __init_tunnel(self, networking):
        self.__thread = threading.Thread(
            target=self.__thread_worker,
            args=(networking, )
        ).start()

    def connect(self):
        self.__init_tunnel(self.__conn)

    def __make_user_id(self):

        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)

        user_id = f"{local_ip}_{os.getpid()}"
        return user_id

    def __sending_thread(self, networking: Networking):
        logging.info("Started sending tunnel started")
        networking.send(b"{self.__make_user_id()}{common.SEP}{common.SEND_TUNNEL_TYPE}")

    def __receiving_thread(self, networking: Networking):
        logging.info("Started receiving tunnel started")
        networking.send(b"{self.__make_user_id()}{common.SEP}{common.RECEIVE_TUNNEL_TYPE}")

    def __thread_worker(self, networking: Networking):
        if self.__sending:
          self.__sending_thread(networking)
          return
        self.__receiving_thread(networking)

    def push_data(self, data):
        assert self.__sending
        self.__queue.put_nowait(data)

    def pull_data(self):
        assert not self.__sending, "Tunnel type is sender"
        return self.__queue.get_nowait()

    def have_new_data(self):
        return not self.__queue.empty()

    def is_sending(self):
        return self.__sending

    def wait_for_connection(self):
        self.__conn.wait_for_connection()
