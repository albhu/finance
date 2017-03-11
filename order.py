class Order(dict):
    """
    Dictionary Object storing the representation of an Order
    """
    def __init__(self, order):
        """
        @symbol eg, GOOGL
        @orderid eg, 3245
        @action eg, A
        @exchange eg, 3
        @quantity eg, 148000
        @news eg, 0
        @side eg, S
        @description eg, Alphabet Class A
        @price eg, 815.34
        """
        self.order = order
        self.symbol = None
        self.orderid = None
        self.action = None
        self.exchange = None
        self.quantity = None
        self.news = None
        self.side = None
        self.description = None
        self.price = None
        self.parse_dict()
        #self.time_in = None

    def parse_dict(self):
        """
        parse stream and assign parameters
        """
        self.symbol = self.order['Symbol']
        self.orderid = self.order['OrderID']
        self.action = self.order['Action']
        self.exchange = self.order['Exchange']
        self.quantity = self.order['Quantity']
        self.news = self.order['News']
        self.side = self.order['Side']
        self.description = self.order['Description']
        self.price = self.order['Price']

    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError("No such attribute: " + name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("No such attribute: " + name)
