import socket
import ast
import json
from orderbook import OrderBook

host_ip, server_port = "localhost", 9995

class FinanceClient:
    """
    TCP Client to connect to Finance server
    Fetch method is a generator to iterate stream
    """
    def __init__(self, host_ip, server_port):
        self.host_ip = host_ip
        self.server_port = server_port

    def connect(self):
        self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_client.connect((host_ip, server_port))
        return self.tcp_client

    @property
    def is_connected(self):
        try:
            return self.connect()
        except:
            return False

    def close(self):
        self.tcp_client.close()

    def fetch(self, recv_buffer=1024):
        if not self.connect():
            self.connect()
        try:
            while True:
                chunk = self.tcp_client.recv(recv_buffer)
                chunk = ast.literal_eval(chunk.decode())
                yield chunk 
        finally:
            print('closing connection')
            self.close()
        return
