from time import time
import ccxt
from utils.settings import settings


class BitgetTrader:
    def __init__(self):
        self._exchange = self.create_exchange()
        print(self._exchange)
    def create_exchange(self):
        return ccxt.bitget({'apiKey':settings.apikey_bitget,'secret':settings.apisec_bitget,'password':settings.apiphrase_bitget,"options":{'defaultType':'swap','adjustForTimeDifferecnce':True}})

    def fetch_symbols(self):
        symbols = None
        # string = '_UMCBL'
        try:
            data = self._exchange.fetch_markets()
            # symbols = [pair['id'] for pair in data if string in pair['id']]
            symbols = [pair['id'] for pair in data]
        except:
            print('error')
        return symbols
    
    def fetch_firts_orders(self,symbol):
        bbid,bask = None,None
        try:
            ob = self._exchange.fetch_order_book(symbol)
            bbid = ob['bids'][0]
            bask = ob['asks'][0]
        except Exception as e:
            print(e)
        return bbid,bask
    
    def open_orders(self):
        orders = None
        try:
            orders = self._exchange.fetch_open_orders()
        except:
            print('error')
        return orders
    
    def limit_order(self,side,price,size,symbol,sl=None,target=None):
        '''
        side: buy / sell
        '''
        order = None
        order_id = str(time() * 1000000)
        params = {'newClientOrderId':"{}_limit_{}".format(order_id,side),"timeInForceValue":"normal",'hedged':True}
        if sl is not None:
            params['presetStopLossPrice'] = sl
        if target is not None:
            params["presetTakeProfitPrice"] = target
        try:
            order = self._exchange.create_order(
                symbol=symbol,
                type='limit',
                side=side,
                amount=size,
                price=price,
                params=params
            )
        except Exception as e:
            print(e)
        return order

    
    def cancel_order(self, symbol, orderId):
        order = None
        try:
            order = self._exchange.cancel_order(symbol=symbol,id=orderId)
        except Exception as e:
            print(e)
        return order
    
    def balance(self):
        balance = None
        try:
            balance = self._exchange.fetch_balance()
        except:
            print('error')
        return balance['total']['USDT'],balance['free']['USDT'], balance['used']['USDT']