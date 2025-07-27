import ccxt
from time import time,sleep
from utils.settings import settings

class BybitTrader1:
    def __init__(self,defaultType='swap',crutch_sleep=0.5):
        self._exchange = self.create_exchange(defaultType)
        self.need_reset = True
        self.crutch_sleep = crutch_sleep
        self.last_sync = 0
        print(self._exchange)
    def create_exchange(self,defaultType):
        return ccxt.bybit({
            'apiKey':settings.apikey_bybit,
            'secret':settings.apisec_bybit,
            'enableRateLimit': True,
            "options":{
                'defaultType':defaultType,
                'adjustForTimeDifference': True,
                'recvWindow': 15000,
                }
            })
    def sync_time(self):
        """Синхронизация времени с сервером Bybit"""
        try:
            server_time = self._exchange.fetch_time()
            local_time = int(time() * 1000)
            time_diff = server_time - local_time
            self.crutch_sleep = (time_diff / 1000)
            self.last_sync = local_time
            print(f"Время синхронизировано. Разница: {time_diff} мс")
            return True
        except Exception as e:
            print(f"Ошибка синхронизации времени: {e}")
            return False
        
    def check_connect(self):
        try:
            balance = self._exchange.fetch_balance()
            print("Подключение успешно! Баланс:", balance['USDT']['free'])
        except Exception as e:
            print("Ошибка подключения:", e)
    
    def fetch_symbols(self):
        symbols = None
        try:
            data = self._exchange.fetch_markets()
            symbols = [pair['id'] for pair in data if pair['swap']]  # Только фьючерсы
        except Exception as e:
            print(f'Error fetching symbols: {e}')
        return symbols

    def fetch_first_orders(self, symbol, index=0):
        bbid, bask = None, None
        try:
            ob = self._exchange.fetch_order_book(symbol)
            bbid = ob['bids'][index][0] if len(ob['bids']) > index else None
            bask = ob['asks'][index][0] if len(ob['asks']) > index else None
        except Exception as e:
            print(f'Error fetching order book: {e}')
        return bbid, bask

    def fetch_condition_orders(self, symbol, price):
        bbid, bask = None, None
        try:
            ob = self._exchange.fetch_order_book(symbol)
            bbid = next((bid[0] for bid in ob['bids'] if bid[0] <= price), None)
            bask = next((ask[0] for ask in ob['asks'] if ask[0] >= price), None)
        except Exception as e:
            print(f'Error fetching conditional orders: {e}')
        return bbid, bask

    def open_orders(self, symbol=None):
        orders = None
        try:
            orders = self._exchange.fetch_open_orders(symbol) if symbol else self._exchange.fetch_open_orders()
        except Exception as e:
            print(f'Error fetching open orders: {e}')
        return orders

    def limit_order(self, side, price, size, symbol, sl=None, tp=None):
        order = None
        params = {}
        if sl:
            params['stopLoss'] = str(sl)  # Bybit использует строки для цен
        if tp:
            params['takeProfit'] = str(tp)
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
            print(f'Error creating order: {e}')
        return order

    def cancel_order(self, symbol, order_id):
        try:
            return self._exchange.cancel_order(id=order_id, symbol=symbol)
        except Exception as e:
            print(f'Error canceling order: {e}')
            return None

    def clear_orders(self, symbol):
        try:
            orders = self._exchange.fetch_open_orders(symbol)
            for order in orders:
                self.cancel_order(symbol, order['id'])
        except Exception as e:
            print(f'Error clearing orders: {e}')

    def balance(self):
        try:
            balance = self._exchange.fetch_balance({'type': 'swap'})  # Для фьючерсов
            usdt = balance['total'].get('USDT', {})
            return usdt.get('total', 0), usdt.get('free', 0), usdt.get('used', 0)
        except Exception as e:
            print(f'Error fetching balance: {e}')
            return None, None, None

    def check_position(self, symbol):
        """Проверка позиции с обработкой ошибок времени"""
        try:
            # Синхронизируем время каждые 5 минут
            if (time() * 1000 - self.last_sync) > 300000:
                self.sync_time()

            positions = self._exchange.fetch_positions(
                symbols=[symbol],
                params={'recvWindow': 15000}  # Явно указываем увеличенное окно
            )
            
            if positions and len(positions) > 0:
                pos = positions[0]
                
                # side = 'long' if pos['side'] == 'buy' else 'short' if pos['side'] == 'sell' else None
                side = pos['side']
                return side, abs(float(pos['contracts']))
            return None, None
            
        except ccxt.NetworkError as e:
            print(f"Сетевая ошибка: {e}")
            sleep(1)
            return self.check_position(symbol)
        except Exception as e:
            print(f"Ошибка проверки позиции: {e}")
            return None, None

    def safe_request(self, method, *args, **kwargs):
        """Безопасный запрос с повторными попытками"""
        for _ in range(3):
            try:
                return getattr(self.exchange, method)(*args, **kwargs)
            except ccxt.ExchangeError as e:
                print(f"Ошибка биржи: {e}")
                self.sync_time()
                sleep(1)
            except Exception as e:
                print(f"Неожиданная ошибка: {e}")
                raise
        raise ConnectionError("Не удалось выполнить запрос после 3 попыток")
    
    def open_long(self,symbol,amount,step):
        bbid,bask = self.fetch_first_orders(symbol,step)
        side, am = self.check_position(symbol)
        if side == 'short':
            self.clear_orders(symbol)
            sleep(self.crutch_sleep)
            size = int(am) + int(amount)
            self.limit_order('buy',bbid,size,symbol)
        elif side != 'long':
            self.clear_orders(symbol)
            sleep(self.crutch_sleep)
            self.limit_order('buy',bbid,amount,symbol)

    def open_short(self,symbol,amount,step):
        bbid,bask = self.fetch_first_orders(symbol,step)
        side, am = self.check_position(symbol)
        if side == 'long':
            self.clear_orders(symbol)
            sleep(self.crutch_sleep)
            size = int(am) + int(amount)
            self.limit_order('sell',bask,size,symbol)
        elif side != 'short':
            self.clear_orders(symbol)
            sleep(self.crutch_sleep)
            self.limit_order('sell',bask,amount,symbol)


    def close_long(self,symbol,step):
        side, amount = self.check_position(symbol)
        bbid,bask = self.fetch_first_orders(symbol,step)
        if side == 'long':
            self.clear_orders(symbol)
            sleep(self.crutch_sleep)
            self.limit_order('sell',bask,amount,symbol)
        else:
            if self.need_reset:
                self.clear_orders(symbol)

    def close_short(self,symbol,step):
        side, amount = self.check_position(symbol)
        bbid,bask = self.fetch_first_orders(symbol,step)
        if side == 'short':
            self.clear_orders(symbol)
            sleep(self.crutch_sleep)
            self.limit_order('buy',bbid,amount,symbol)
        else:
            if self.need_reset:
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
            if self.need_reset:
                self.clear_orders(symbol)

    # price_work
    def open_long_pw(self,symbol,amount,price):
        bbid,bask = self.fetch_condition_orders(symbol,price)
        side, am = self.check_position(symbol)
        print(bbid)
        if side == 'short':
            self.clear_orders(symbol)
            sleep(self.crutch_sleep)
            size = int(am) + int(amount)
            self.limit_order('buy',bbid,size,symbol)
        elif side != 'long':
            self.clear_orders(symbol)
            sleep(self.crutch_sleep)
            self.limit_order('buy',bbid,amount,symbol)

    def open_short_pw(self,symbol,amount,price):
        bbid,bask = self.fetch_condition_orders(symbol,price)
        side, am = self.check_position(symbol)
        if side == 'long':
            self.clear_orders(symbol)
            sleep(self.crutch_sleep)
            size = int(am) + int(amount)
            self.limit_order('sell',bask,size,symbol)
        elif side != 'short':
            self.clear_orders(symbol)
            sleep(self.crutch_sleep)
            self.limit_order('sell',bask,amount,symbol)

    def close_long_pw(self,symbol,price):
        side, amount = self.check_position(symbol)
        bbid,bask = self.fetch_condition_orders(symbol,price)
        if side == 'long':
            self.clear_orders(symbol)
            sleep(self.crutch_sleep)
            self.limit_order('sell',bask,amount,symbol)
        else:
            if self.need_reset:
                self.clear_orders(symbol)

    def close_short_pw(self,symbol,price):
        side, amount = self.check_position(symbol)
        bbid,bask = self.fetch_condition_orders(symbol,price)
        if side == 'short':
            self.clear_orders(symbol)
            sleep(self.crutch_sleep)
            self.limit_order('buy',bbid,amount,symbol)
        else:
            if self.need_reset:
                self.clear_orders(symbol)
    
    def none_action(self,symbol):
        if self.need_reset:
            self.clear_orders(symbol)


