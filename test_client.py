import socket
import ast
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
        tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_client.connect((host_ip, server_port))
        return tcp_client

    def fetch(self, recv_buffer=512, delim='\n'):
        try:
            tcp_client = self.connect()
        except Exception as e:
            print(e)
            print('Can\'t connect bro!')
        while True:
            try:
                chunk = tcp_client.recv(recv_buffer)
                chunk = ast.literal_eval(chunk.decode('utf-8'))
                yield chunk 
            except Exception as e:
                print(e)
                break
        return
