from common.tunnel import Tunnel

class PlayerTunnels:
    def __init__(self, send_conn, recv_conn):
        self.__send_tunnel = Tunnel(send_conn, sending=True)
        self.__recv_tunnel = Tunnel(recv_conn, sending=False)

    def wait_for_connection(self):
        self.__send_tunnel.wait_for_connection()
        self.__recv_tunnel.wait_for_connection()

    def get_send_tunnel(self):
        return self.__send_tunnel

    def get_recv_tunnel(self):
        return self.__recv_tunnel
