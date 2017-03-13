from order import Order
from orderbook import OrderBook
from client import FinanceClient
from ordermanager import OrderManager
from strategy import Vanilla, Strawberry
import sys

# local server for finance data
host_ip, server_port = "localhost", 9995

def main():
    """
    Turn on the FinanceServer
    - fetch data from the FinanceServer
    - parse out each order as an Order object
    - add these Orders to the OrderBook using the values in Action
    - for each added order, decide to trade indicated by signal
    """
    strategy_choice = sys.argv[1]
    books = {}
    client = FinanceClient(host_ip, server_port)
    ordermanager = OrderManager()

    if strategy_choice == 'Vanilla':
        strategy = Vanilla()
    elif strategy_choice == 'Strawberry':
        strategy = Strawberry()
    else:
        print('strategies available: Vanilla or Strawberry')

    print(strategy.name, strategy.description)

    for line in client.fetch():
        try:
            order = Order(line)
            book = books.get(order.symbol)
            if book is None:
                book = books[order.symbol] = OrderBook(order.symbol)
            if order.action == 'A':
                book.add(order)
            elif order.action == 'M':
                book.modify(order)
            bid, offer = book.display_book(output=True)
            ordermanager.signal(bid, offer, strategy.execute)

        except Exception as e:
            print(e)
            pass

if __name__ == '__main__':
    main()
