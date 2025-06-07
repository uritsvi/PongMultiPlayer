from common.tunnel import Tunnel

class PlayerTunnels:
    def __init__(self, client_send_conn, client_recv_conn, server=True):
        if server:
            self.send_tunnel = Tunnel(client_recv_conn, sending=True)
            self.recv_tunnel = Tunnel(client_send_conn, sending=False)
        else:
            self.send_tunnel = Tunnel(client_send_conn, sending=True)
            self.recv_tunnel = Tunnel(client_recv_conn, sending=False)

    def wait_for_connection(self):
        self.recv_tunnel.wait_for_connection()
        self.send_tunnel.wait_for_connection()


    def get_send_tunnel(self):
        return self.send_tunnel

    def get_recv_tunnel(self):
        return self.recv_tunnel

    def start_tunnels(self):
        self.send_tunnel.start_tunnel()
        self.recv_tunnel.start_tunnel()