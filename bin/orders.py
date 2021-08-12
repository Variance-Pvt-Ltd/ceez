import json
from bin._binance_ import Z_Binance
binance=Z_Binance()
class Schedule:
    def __init__(self):
        with open('../usr/orders.json') as jn:
            self.j = dict(json.load(jn))
        jn.close()

    def save_order(self, order):
        self.j[order.id] = order.d
        with open('../usr/orders.json', 'w') as jn:
            json.dump(self.j, jn).encode('utf-8')
        jn.close()

    def delete_order(self, id):


        
        del self.j[id]
        with open('../usr/orders.json', 'w') as jn:
            json.dump(self.j, jn).encode('utf-8')
        jn.close()


class Order(Schedule):
    def __init__(self, z_id, symbol, z_type, side, take_profit, execution_priority, quantity, timeInForce):
        super().__init__()
        if self.execution_priority == 1:
            pass  # ToDo: execute binance
        else:
            self.id = z_id
            self.d = {}
            self.symbol, self.d["symbol"] = symbol
            self.type, self.d["type"] = z_type
            self.side, self.d["side"] = side
            self.take_profit, self.d["take_profit"] = take_profit
            self.execution_priority, self.d["execution_priority"] = execution_priority
            self.quantity, self.d["quantity"] = quantity
            self.timeInForce, self.d["timeInForce"] = timeInForce
            Schedule.save_order(self)

    def edit_order(self, id=False, symbol=False, type=False, side=False, take_profit=False, execution_priority=False,
                   quantity=False, timeInForce=False):
        for x in [id, symbol, type, side, take_profit, execution_priority, quantity, timeInForce]:
            if x:
                self.x, self.d[x] = x
        if self.quantity == 0:
            Schedule.delete_order(self)
        else:
            Schedule.save_order(self)
