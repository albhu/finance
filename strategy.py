import socket
import json
import pandas as pd
import numpy as np
import json
from ordermanager import OrderManager
from collections import OrderedDict
from pnlmanager import Trade, TradeManager, Fill

class Strategy(OrderManager):
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.market_orders = OrderedDict()
"""
Organize strategies here
- should return T/F
"""

class Vanilla(Strategy):
    def __init__(self):
        self.name = 'Vanilla' + '\n'
        self.description = '*********************' + '\n' +\
                           '*********************' + '\n' +\
                           '*********************' + '\n' +\
        'Take means of price for Symbol for different news signals. Buy when the top of the orderbook is lower than the mean. Sell when the top of the orderbook is higher than the mean.' + '\n' + \
                           '*********************' + '\n' +\
                           '*********************' + '\n' +\
                           '*********************' + '\n'
        super().__init__(self.name, self.description)

    def execute(self, bid=None, offer=None):
        """
        Take means of prices for Symbol for different news
        - Buy when the top of the orderbook is lower than the mean
        - Sell when the top of orderbook is higher than the mean
        """

        guide = pd.read_csv('strategy_guides/vanilla.csv')
        try:
            symbol = np.asscalar(bid['symbol'].values)
            side = np.asscalar(bid['side'].values)
            news = np.asscalar(bid['news'].astype(int).values)
        except:
            pass
        try:
            o_symbol = np.asscalar(offer['symbol'].values)
            o_side = np.asscalar(offer['side'].values)
            o_news = np.asscalar(offer['news'].astype(int).values)
        except:
            pass

        if not bid.empty:
            guide_price = np.asscalar(guide[(guide.symbol == symbol) \
                    & (guide.side == side) \
                    & (guide.news == news)]['price'].values)
            bid_price = np.asscalar(bid['price'].astype(float).values)
            if bid_price >= guide_price:
                bid = self.df_dict(bid)
                self.submit_order(bid)
            return True
        else:
            return False

        if not offer.empty:
            guide_price_o = np.asscalar(guide[(guide.symbol == o_symbol) \
                    & (guide.side == o_side) \
                    & (guide.news == o_news)]['price'].values)
            offer_price = np.asscalar(offer['price'].astype(float).values)
            if offer_price <= guide_price:
                offer = self.df_dict(offer)
                self.submit_order(offer)
            return True
        else:
            return False
        
class Strawberry(Strategy):
    def __init__(self):
        self.name = 'Strawberry:' + '\n'
        self.description = '*********************' + '\n' +\
                           '*********************' + '\n' +\
                           '*********************' + '\n' +\
                'The Strawberry strategy uses results from OLS on the news indicators to determine whether the presence of news influences bid/offer prices. Make decisions based off the guide created from the coefficients of the regression' + '\n' +\
                '*********************' + '\n' +\
                '*********************' + '\n' +\
                '*********************' + '\n'
        super().__init__(self.name, self.description)

    def execute(self, bid=None, offer=None):
        """
        Use results from historical OLS regression on News
        """

        guide = pd.read_csv('strategy_guides/strawberry.csv')
        try:
            symbol = np.asscalar(bid['symbol'].values)
            side = np.asscalar(bid['side'].values)
            news = np.asscalar(bid['news'].astype(int).values)
        except:
            pass
        try:
            o_symbol = np.asscalar(offer['symbol'].values)
            o_side = np.asscalar(offer['side'].values)
            o_news = np.asscalar(offer['news'].astype(int).values)
        except:
            pass

        try:
            if not bid.empty:
                decision = np.asscalar(guide[(guide.symbol == symbol) \
                        & (guide.side == side) \
                        & (guide.news == news)]['is_buy'].values)
                if decision == 'Buy':
                    bid = self.df_dict(bid)
                    self.submit_order(bid)
                print(a)
                return True
            else:
                return False
        except:
            pass

        try:
            if not offer.empty:
                decision_o = np.asscalar(guide[(guide.symbol == symbol_o) \
                        & (guide.side == side_o) \
                        & (guide.news == news_o)]['is_buy'].values)
                if decision_o == 'Sell':
                    offer = self.df_dict(offer)
                    self.submit_order(offer)
                return True
            else:
                return False
        except:
            pass
