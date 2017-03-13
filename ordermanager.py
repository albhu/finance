import socket
import json
import pandas as pd
import numpy as np
from client import FinanceClient

host_ip, server_port = "localhost", 9995

class OrderManager(FinanceClient):
    """
    Receive top of the book
    Pass through rules to determine whether or not an order should be submitted
    Send order from top of book back to server
    """
    def __init__(self):
        #self.host_ip = host_ip
        #self.server_port = server_port
        super(OrderManager, self).__init__(host_ip, server_port)
    
    def json_format(self, v):
        return json.dumps(v).encode('utf-8')

    def submit_order(self, quote):
        if not FinanceClient.is_connected(self):
            FinanceClient.connect(self)
        try:
            FinanceClient.connect(self).send(self.json_format(quote))
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
        fields = ['symbol', 'quantity', 'side', 'price', 'exchange']
        d = [dict([(colname, row[i])
                for i,colname in enumerate(df.columns)
            ])
            for row in df.values
        ]
        quote = d[0]
        ready_order = {k: quote[k] for k in fields}
        for key, value in ready_order.items():
            if key == 'side' and value == 'B':
                ready_order[key] = 'S'
            elif key == 'side' and value == 'S':
                ready_order[key] = 'B'
        return ready_order
