import binance.exceptions as x
from binance.client import Client
import os
from env.credentials import test_cred


class Z_Binance:
    def __init__(self):
        api_key = test_cred()[0]
        api_secret = test_cred()[1]

        try:
            self.client = Client(api_key, api_secret)
            #### testing purpose only ####
            self.client.API_URL = 'https://testnet.binance.vision/api'
            #############################
        except ReadTimeout:
            print('Failed connecting Binance')

    def balance(self, account='all'):
        if account == 'all':
            return self.client.get_account()
        elif account == 'future':
            print(self.client.futures_account_balance())
        elif account == 'margin':
            print(self.client.futures_account_balance())
        else:  # balance of specific assets
            print(self.client.get_asset_balance(account))

    def order(self, symbol, side, ztimeInForce, quantity, price,ztype='market'):
        # z_order = {}

        try:
            # nonlocal z_order
            z_order = self.client.create_order(
                symbol=symbol,
                side=side,
                type=ztype,
                timeInForce=ztimeInForce,
                quantity=quantity,
                price=price)

        except x.BinanceAPIException as e:
            print(e)
            # ToDo : implement exception handling
        except x.BinanceOrderException as e:
            print(e)
            # ToDo : implement exception handling
        # notification = z_order
        # finally:
        #     return notification

