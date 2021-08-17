import json

from bin._binance_ import Z_Binance

binance = Z_Binance()


class Schedule:

    def __init__(self):
        with open('usr/orders.json') as jn:
            self.j = dict(json.load(jn))
        jn.close()

    def save_order(self, order):
        self.j[order.id] = order.d
        with open('usr/orders.json', 'w') as jn:
            json.dump(self.j, jn)
        jn.close()

    def delete_order(self, id):
        del self.j[id]
        with open('usr/orders.json', 'w') as jn:
            json.dump(self.j, jn)
        jn.close()

    def reader(self):
        with open('usr/orders.json', 'r') as jn:
            json.read()
        jn.close()


all_orders = Schedule()


class Order(Schedule):

    def __init__(self, id, symbol, z_type, take_profit, quantity, side=None, execution_priority=None, timeInForce=None):
        super().__init__()
        self.id = id
        self.d = {}
        self.symbol, self.d["symbol"] = symbol, symbol
        self.type, self.d["type"] = z_type, z_type
        self.side, self.d["side"] = side, side
        self.take_profit, self.d["take_profit"] = take_profit, take_profit
        self.execution_priority, self.d["execution_priority"] = execution_priority, execution_priority
        self.quantity, self.d["quantity"] = quantity, quantity
        self.timeInForce, self.d["timeInForce"] = timeInForce, timeInForce
        Schedule.save_order(all_orders, order=self)

    def edit_order(self, id=False, symbol=False, type=False, side=False, take_profit=False, execution_priority=False,
                   quantity=False, timeInForce=False):
        for x in [id, symbol, type, side, take_profit, execution_priority, quantity, timeInForce]:
            if x:
                self.x, self.d[x] = x
        if self.quantity == 0:
            Schedule.delete_order(self)
        else:
            Schedule.save_order(self)
