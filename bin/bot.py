import json
import _binance_

with open('../bin/requests.json') as r:
    update = json.load(r)
    r.close()
if update["unread"]:
    pass


def eyes(market, principal, take_profit):
    """

    :param market:
    :param principal:
    :param take_profit: supposed to be in percent
    :return:
    """
    if market == principal((take_profit + 100) / 100):
        place_order = _binance_.Z_Binance(symbol,
                                          side=update['side'],
                                          ztimeInForce=update'timeInForce'],
                                          quantity=update['quantity'],
                                          price=update['price']

                                          )
# limit:
        price is being pass
# market:
