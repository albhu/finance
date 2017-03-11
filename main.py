from order import Order
from orderbook import OrderBook
from client import FinanceClient
from ordermanager import OrderManager
from strategy import Vanilla, Strawberry
import time
import socket
import json

# local server for finance data
host_ip, server_port = "localhost", 9995

def main():
    """
    Turn on the FinanceServer
    - fetch data from the FinanceServer
    - parse out each order as an Order object
    - add these Orders to the OrderBook using the values in Action
    - for each added order, decide to trade indicated by submit_order
    """
    books = {}
    client = FinanceClient(host_ip, server_port)
    ordermanager = OrderManager(host_ip, server_port)
    strategy = Strawberry()
    print(strategy.name + ':' , strategy.description)
    for line in client.fetch():
        try:
            order = Order(line)
            book = books.get(order.symbol)
            if book is None:
                book = books[order.symbol] = OrderBook(order.symbol)
            book.add(order)
            bid, offer = book.display_book()
            print('-----------------')
            if not bid.empty:
                print(bid)
            if not offer.empty:
                print(offer)
            print('-----------------')
            if ordermanager.signal(bid, offer, strategy.execute):
                print('order sent')
        except Exception as e:
            print(e)
            pass

if __name__ == '__main__':
    main()
