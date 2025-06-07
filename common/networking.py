import socket
import struct
import common.common as common

"""Accepts a socket that is already connected or already bound to a port."""
class Networking:
    def __init__(self, sock):
        self.sock = sock

    def __receive_by_size(self):
        size_buff = self.sock.recv(4)
        if len(size_buff) == 0:
            raise Exception("Socket closed unexpectedly")

        size = socket.ntohl(struct.unpack('I', size_buff)[0])
        buffer = self.sock.recv(size)
        while len(buffer) < size:
            current = self.sock.recv(size - len(buffer))
            buffer += current

        return buffer

    def __send_by_size(self, buffer):
        size = len(buffer)
        buffer = struct.pack("I", socket.htonl(size)) + buffer
        self.sock.sendall(buffer)

    def send(self, data):
        self.__send_by_size(data)
        response = self.__receive_by_size().decode()
        if response != common.ACK:
            raise "Ack msg did not recv"

    def receive(self):
        data = self.__receive_by_size()
        self.__send_by_size(common.ACK.encode())
        return data

    def wait_for_connection(self):
        self.sock.listen(1)
        print("Waiting for connection...")
        client_socket, addr = self.sock.accept()
        print(f"Accepted connection from {addr}")
        return Networking(client_socket)

    @classmethod
    def create_sock(cls, ip, port):
        print("create sock", ip, port)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))

        return sock
