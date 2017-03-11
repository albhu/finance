from operator import itemgetter
from io import StringIO
import pandas as pd
import numpy as np

class OrderBook:

    def __init__(self, symbol):
        self.symbol = symbol
        self.bid = []
        self.offer = []

    def add(self, order):
        if order.side == 'B':
            self.bid.append(order)
        elif order.side == 'S':
            self.offer.append(order)
        else:
            print('Error: Order is not a buy or sell')

    def cancel(self, order):
        if order.side == 'B':
            self.bid = [e for e in self.bid \
                if e.get('orderid', '') != order.orderid or \
                e.get.exchange != order.exchange]
        elif order.side == 'S':
            self.offer = [e for e in self.offer \
                if e.get('orderid', '') != order.orderid or \
                e.get('exchange') != order.exchange]
        else:
            print('error not a buy or sell')

    def modify(self, order):
        self.cancel(order)
        self.add(order)

    def sort_book(self, order, **kwargs):
        order = sorted(order, key=itemgetter('price', 'exchange'), **kwargs)
        try:
            order = order[0]
        except:
            order = order
        return order

    def format_book(self):
        try:
            df_bid = self.sort_book(self.bid, reverse=True)
            df_bid = pd.DataFrame(df_bid, index=[0])
            df_bid = df_bid.drop('order', axis=1)
        except Exception as e:
            pass

        try:
            df_offer = self.sort_book(self.offer, reverse=False)
            df_offer = pd.DataFrame(df_offer, index=[0])
            df_offer = df_offer.drop('order', axis=1)    
        except Exception as e:
            pass
        df_orderbook = pd.concat([df_bid, df_offer], axis=1)
        return df_bid, df_offer

    def display_book(self, k=None, output=False):
        pd.set_option('display.width', 1000)
        pd.set_option('display.max_columns', 1000)
        bid, offer = self.format_book()
        if output is True:
            print(bid)
            print(offer)
        return bid, offer

    def __str__(self):
        fileStr = StringIO()
        fileStr.write("------ Bids -------\n")
        if self.bid != None and len(self.bid) > 0:
            for x in self.bid:
                fileStr.write('\n')
                for k, v in x.items():
                    fileStr.write('%s | ' % v)
        fileStr.write("\n------ Asks -------\n")
        if self.offer != None and len(self.offer) > 0:
            for y in self.offer:
                for k, v in y.items():
                    fileStr.write('%s' % v)
        fileStr.write("\n")
        return fileStr.getvalue()
