from time import time,sleep
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
    
    def fetch_firts_orders(self,symbol,index=0):
        '''bbid,bask'''
        bbid,bask = None,None
        try:
            ob = self._exchange.fetch_order_book(symbol)
            bbid = ob['bids'][index][0]
            bask = ob['asks'][index][0]
        except Exception as e:
            print(e)
        return bbid,bask
    
    def fetch_condition_orders(self,symbol,price):
        bbid,bask = None,None
        try:
            ob = self._exchange.fetch_order_book(symbol)
            for bid in ob['bids']:
                if bid[0] <= price:
                    bbid  =bid[0]
                    break
            for ask in ob['asks']:
                if ask[0] >= price:
                    bask  = ask[0]
                    break
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
        # self._exchange.set_position_mode(False, symbol)
        # self._exchange.set_margin_mode( 'isolated', symbol)
        order = None
        order_id = str(time() * 1000000)
        # hold_side = "short" if side == 'sell' else "long"
        # params = {'newClientOrderId':"{}_limit_{}".format(order_id,side),"timeInForceValue":"normal",'hedged':True}
        # params = {'newClientOrderId':"{}_limit_{}".format(order_id,side),"timeInForceValue":"normal",'oneWayMode':True, 'holdSide':hold_side}
        params = {'newClientOrderId':"{}_limit_{}".format(order_id,side),"timeInForceValue":"normal",'oneWayMode':True}
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
    
    def clear_orders(self,symbol):
        orders = None
        try:
            orders = self._exchange.fetch_open_orders(symbol)
            if len(orders) > 0:
                for order in orders:
                    self.cancel_order(symbol,order['info']['orderId'])
        except Exception as e:
            print(e)
    
    def balance(self):
        balance = None
        try:
            balance = self._exchange.fetch_balance()
        except:
            print('error')
        return balance['total']['USDT'],balance['free']['USDT'], balance['used']['USDT']
    
    def check_position(self,symbol):
        '''side, amount'''
        side, amount = None, None
        try:
            pos = self._exchange.fetch_position(symbol)
            amount = pos['info']['total']
            side = pos['side']
        except:
            pass
        return side, amount

    def open_long(self,symbol,amount,step):
        bbid,bask = self.fetch_firts_orders(symbol,step)
        side, am = self.check_position(symbol)
        if side != 'long':
            self.clear_orders(symbol)
            sleep(0.5) # TODO
            self.limit_order('buy',bbid,amount,symbol)
        # if side == 'short':
        #     self.clear_orders(symbol)
        #     sleep(0.5) # TODO
        #     self.limit_order('buy',bbid,amount,symbol)

    def open_short(self,symbol,amount,step):
        bbid,bask = self.fetch_firts_orders(symbol,step)
        side, am = self.check_position(symbol)
        if side != 'short':
            self.clear_orders(symbol)
            sleep(0.5) # TODO
            self.limit_order('sell',bask,amount,symbol)
        # if side == 'long':
        #     self.clear_orders(symbol)
        #     sleep(0.5) # TODO
        #     self.limit_order('sell',bask,amount,symbol)


    def close_long(self,symbol,step):
        side, amount = self.check_position(symbol)
        if side == 'long':
            self.open_short(symbol,amount,step)
        else:
            self.clear_orders(symbol)

    def close_short(self,symbol,step):
        side, amount = self.check_position(symbol)
        if side == 'short':
            self.open_long(symbol,amount,step)
        else:
            self.clear_orders(symbol)

    def close_all(self,symbol,step):
        side, amount = self.check_position(symbol)
        if side == 'short':
            self.clear_orders(symbol)
            self.open_long(symbol,amount,step)
        elif side == 'short':
            self.clear_orders(symbol)
            self.open_long(symbol,amount,step)
        else:
            self.clear_orders(symbol)

    # middle_price
    def open_long_m(self,symbol,amount,price):
        bbid,bask = self.fetch_condition_orders(symbol,price)
        side, am = self.check_position(symbol)
        if side != 'long':
            self.clear_orders(symbol)
            sleep(0.5) # TODO
            self.limit_order('buy',bbid,amount,symbol)

    def open_short_m(self,symbol,amount,price):
        bbid,bask = self.fetch_condition_orders(symbol,price)
        side, am = self.check_position(symbol)
        if side != 'short':
            self.clear_orders(symbol)
            sleep(0.5) # TODO
            self.limit_order('sell',bask,amount,symbol)

    def close_long_m(self,symbol,price):
        side, amount = self.check_position(symbol)
        if side == 'long':
            self.open_short_m(symbol,amount,price)
        else:
            self.clear_orders(symbol)

    def close_short_m(self,symbol,price):
        side, amount = self.check_position(symbol)
        if side == 'short':
            self.open_long_m(symbol,amount,price)
        else:
            self.clear_orders(symbol)
    
    def none_action(self,symbol):
        self.clear_orders(symbol)