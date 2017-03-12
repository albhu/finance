import socket
import json
import pandas as pd
import numpy as np
import json

host_ip, server_port = "localhost", 9995

"""
TO DO:
split this up to an ordermanager?
and a strategy?
"""

class OrderManager:
    """
    Receive top of the book
    Pass through rules to determine whether or not an order should be submitted
    Send order from top of book back to server
    """
    def __init__(self, host_ip, server_port):
        self.host_ip = host_ip
        self.server_port = server_port

    def connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host_ip, server_port))
        return self.client

    @property
    def is_connected(self):
        try:
            return self.connect()
        except:
            return False

    def close(self):
        self.client.close()

    def json_format(self, v):
        return json.dumps(v).encode('utf-8')

    def submit_order(self, quote):
        if not self.connect():
            self.connect()
        try:
            self.client.send(self.json_format(quote))
        except Exception as e:
            print(e)
        return

    def signal(self, bid=None, offer=None, strategy=None):
        if not strategy:
            print('No strategy chosen')

        execution_plan = strategy(bid, offer)
        return execution_plan

    def df_dict(self, df):
        """
        Convert pandas dataframe to dictionary
        """
        d = [dict([(colname, row[i])
                for i,colname in enumerate(df.columns)
            ])
            for row in df.values
        ]
        return d[0]
