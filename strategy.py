import socket
import json
import pandas as pd
import numpy as np
import json
from ordermanager import OrderManager
from collections import OrderedDict


class Strategy(OrderManager):
    def __init__(self, name, description):
        self.name = name
        self.description = description
        #self.market_orders = OrderedDict()

    def as_scalar(self, result):
        try:
            result = np.asscalar(result.values)
        except:
            pass
        return result
    
"""
STRATEGIES
1) VANILLA
2) STRAWBERRY
3) ???
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
            symbol = self.as_scalar(bid['symbol'])
            side = self.as_scalar(bid['side'])
            news = self.as_scalar(bid['news'].astype(int))
        except:
            pass
        try:
            o_symbol = self.as_scalar(offer['symbol'])
            o_side = self.as_scalar(offer['side'])
            o_news = self.as_scalar(offer['news'].astype(int))

        except Exception as e:
            pass
        
        try:
            if not bid.empty:
                guide_price = self.as_scalar(guide[(guide.symbol == symbol) \
                        & (guide.side == side) \
                        & (guide.news == news)]['price'])
                bid_price = self.as_scalar(bid['price'].astype(float))
                if bid_price >= guide_price:
                    bid = self.df_dict(bid)
                    self.submit_order(bid)
           #     return True
           # else:
           #     return False

        except Exception as e:
            pass
        
        try:
            if not offer.empty:
                guide_price_o = self.as_scalar(guide[(guide.symbol == o_symbol) \
                        & (guide.side == o_side) \
                        & (guide.news == o_news)]['price'])
                offer_price = self.as_scalar(offer['price'].astype(float))
                if offer_price <= guide_price_o:
                    offer = self.df_dict(offer)
                    self.submit_order(offer)
            #    return True
            #else:
            #    return False

        except Exception as e:
            pass

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
            symbol = self.as_scalar(bid['symbol'])
            side = self.as_scalar(bid['side'])
            news = self.as_scalar(bid['news'].astype(int))
        except:
            pass
        try:
            o_symbol = self.as_scalar(offer['symbol'])
            o_side = self.as_scalar(offer['side'])
            o_news = self.as_scalar(offer['news'].astype(int))
        except:
            pass

        try:
            if not bid.empty:
                decision = (guide[(guide.symbol == symbol) \
                        & (guide.side == side) \
                        & (guide.news == news)]['is_buy'])
                decision = self.as_scalar(decision)
                if decision == 'Buy':
                    bid = self.df_dict(bid)
                    self.submit_order(bid)
            #    return True
            #else:
            #    return False
        except:
            pass

        try:
            if not offer.empty:
                decision_o = (guide[(guide.symbol == o_symbol) \
                        & (guide.side == o_side) \
                        & (guide.news == o_news)]['is_buy'])
                decision_o = self.as_scalar(decision_o)
                if decision_o == 'Sell':
                    offer = self.df_dict(offer)
                    self.submit_order(offer)
            #    return True
            #else:
            #    return False
        except Exception as e:
            pass
