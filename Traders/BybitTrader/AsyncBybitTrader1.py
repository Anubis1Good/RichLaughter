import asyncio
import ccxt.async_support as ccxt
from time import time
from utils.settings import settings

class AsyncBybitTrader1:
    def __init__(self, defaultType='swap'):
        self._exchange = None
        self.defaultType = defaultType
        self.need_reset = True
        self.position_checks = {}  # Для отслеживания статуса позиций

    async def initialize(self):
        """Асинхронная инициализация"""
        self._exchange = await self.create_exchange()
        print(f"Exchange initialized: {self._exchange}")

    async def create_exchange(self):
        """Создание асинхронного подключения"""
        return ccxt.bybit({
            'apiKey': settings.apikey_bybit,
            'secret': settings.apisec_bybit,
            'enableRateLimit': True,
            'options': {
                'defaultType': self.defaultType,
                'adjustForTimeDifference': True,
            }
        })

    async def check_connect(self):
        """Проверка подключения"""
        try:
            balance = await self._exchange.fetch_balance()
            print("Connection successful! Balance:", balance['USDT']['free'])
            return True
        except Exception as e:
            print("Connection error:", e)
            return False

    async def fetch_symbols(self):
        """Получение списка символов"""
        try:
            data = await self._exchange.fetch_markets()
            return [pair['id'] for pair in data if pair['swap']]
        except Exception as e:
            print(f'Error fetching symbols: {e}')
            return None

    async def fetch_first_orders(self, symbol, index=0):
        """Получение первых ордеров в стакане"""
        try:
            ob = await self._exchange.fetch_order_book(symbol)
            return (
                ob['bids'][index][0] if len(ob['bids']) > index else None,
                ob['asks'][index][0] if len(ob['asks']) > index else None
            )
        except Exception as e:
            print(f'Error fetching order book: {e}')
            return None, None

    async def fetch_condition_orders(self, symbol, price):
        """Поиск ордеров по условию цены"""
        try:
            ob = await self._exchange.fetch_order_book(symbol)
            return (
                next((bid[0] for bid in ob['bids'] if bid[0] <= price), None),
                next((ask[0] for ask in ob['asks'] if ask[0] >= price), None)
            )
        except Exception as e:
            print(f'Error fetching conditional orders: {e}')
            return None, None

    async def open_orders(self, symbol=None):
        """Получение открытых ордеров"""
        try:
            return await self._exchange.fetch_open_orders(symbol) if symbol else await self._exchange.fetch_open_orders()
        except Exception as e:
            print(f'Error fetching open orders: {e}')
            return None

    async def limit_order(self, side, price, size, symbol, sl=None, tp=None):
        """Размещение лимитного ордера"""
        params = {}
        if sl:
            params['stopLoss'] = str(sl)
        if tp:
            params['takeProfit'] = str(tp)
        
        try:
            return await self._exchange.create_order(
                symbol=symbol,
                type='limit',
                side=side,
                amount=size,
                price=price,
                params=params
            )
        except Exception as e:
            print(f'Error creating order: {e}')
            return None

    async def cancel_order(self, symbol, order_id):
        """Отмена ордера"""
        try:
            return await self._exchange.cancel_order(id=order_id, symbol=symbol)
        except Exception as e:
            print(f'Error canceling order: {e}')
            return None

    async def clear_orders(self, symbol):
        """Очистка всех ордеров"""
        try:
            orders = await self._exchange.fetch_open_orders(symbol)
            for order in orders:
                await self.cancel_order(symbol, order['id'])
        except Exception as e:
            print(f'Error clearing orders: {e}')

    async def balance(self):
        """Получение баланса"""
        try:
            balance = await self._exchange.fetch_balance({'type': 'swap'})
            usdt = balance['total'].get('USDT', {})
            return usdt.get('total', 0), usdt.get('free', 0), usdt.get('used', 0)
        except Exception as e:
            print(f'Error fetching balance: {e}')
            return None, None, None

    async def check_position(self, symbol):
        """Проверка текущей позиции"""
        try:
            positions = await self._exchange.fetch_positions([symbol])
            if positions:
                pos = positions[0]
                side = 'long' if pos['side'] == 'buy' else 'short' if pos['side'] == 'sell' else None
                return side, abs(float(pos['contracts']))
            return None, None
        except Exception as e:
            print(f'Error checking position: {e}')
            return None, None

    async def wait_for_position_update(self, symbol, target_side=None, timeout=10):
        """Ожидание обновления позиции"""
        start_time = time()
        while time() - start_time < timeout:
            current_side, current_size = await self.check_position(symbol)
            
            if target_side is None and current_size == 0:
                return True  # Позиция закрыта
            elif current_side == target_side:
                return True  # Позиция соответствует цели
            
            await asyncio.sleep(0.1)
        
        raise TimeoutError(f"Position didn't update in {timeout} seconds")

    async def open_long(self, symbol, amount, step):
        """Открытие лонг позиции с проверкой текущей позиции"""
        bbid, bask = await self.fetch_first_orders(symbol, step)
        side, am = await self.check_position(symbol)
        
        if side == 'short':
            await self.clear_orders(symbol)
            await self.wait_for_position_update(symbol, None)
            await self.limit_order('buy', bbid, amount + abs(am), symbol)
        elif side != 'long':
            await self.clear_orders(symbol)
            await self.limit_order('buy', bbid, amount, symbol)

    async def open_short(self, symbol, amount, step):
        """Открытие шорт позиции с проверкой текущей позиции"""
        bbid, bask = await self.fetch_first_orders(symbol, step)
        side, am = await self.check_position(symbol)
        
        if side == 'long':
            await self.clear_orders(symbol)
            await self.wait_for_position_update(symbol, None)
            await self.limit_order('sell', bask, amount + abs(am), symbol)
        elif side != 'short':
            await self.clear_orders(symbol)
            await self.limit_order('sell', bask, amount, symbol)

    async def close_long(self, symbol, step):
        """Закрытие лонг позиции"""
        side, amount = await self.check_position(symbol)
        if side == 'long':
            await self.clear_orders(symbol)
            _, bask = await self.fetch_first_orders(symbol, step)
            await self.limit_order('sell', bask, amount, symbol)
        elif self.need_reset:
            await self.clear_orders(symbol)

    async def close_short(self, symbol, step):
        """Закрытие шорт позиции"""
        side, amount = await self.check_position(symbol)
        if side == 'short':
            await self.clear_orders(symbol)
            bbid, _ = await self.fetch_first_orders(symbol, step)
            await self.limit_order('buy', bbid, amount, symbol)
        elif self.need_reset:
            await self.clear_orders(symbol)

    async def close_all(self, symbol, step):
        """Закрытие всех позиций"""
        side, amount = await self.check_position(symbol)
        if side == 'short':
            await self.close_short(symbol, step)
        elif side == 'long':
            await self.close_long(symbol, step)
        elif self.need_reset:
            await self.clear_orders(symbol)

    # Асинхронные версии методов price_work
    async def open_long_pw(self, symbol, amount, price):
        bbid, bask = await self.fetch_condition_orders(symbol, price)
        side, am = await self.check_position(symbol)
        
        if side == 'short':
            await self.clear_orders(symbol)
            await self.wait_for_position_update(symbol, None)
            await self.limit_order('buy', bbid, amount + abs(am), symbol)
        elif side != 'long':
            await self.clear_orders(symbol)
            await self.limit_order('buy', bbid, amount, symbol)

    async def open_short_pw(self, symbol, amount, price):
        bbid, bask = await self.fetch_condition_orders(symbol, price)
        side, am = await self.check_position(symbol)
        
        if side == 'long':
            await self.clear_orders(symbol)
            await self.wait_for_position_update(symbol, None)
            await self.limit_order('sell', bask, amount + abs(am), symbol)
        elif side != 'short':
            await self.clear_orders(symbol)
            await self.limit_order('sell', bask, amount, symbol)

    async def close_long_pw(self, symbol, price):
        side, amount = await self.check_position(symbol)
        if side == 'long':
            await self.clear_orders(symbol)
            _, bask = await self.fetch_condition_orders(symbol, price)
            await self.limit_order('sell', bask, amount, symbol)
        elif self.need_reset:
            await self.clear_orders(symbol)

    async def close_short_pw(self, symbol, price):
        side, amount = await self.check_position(symbol)
        if side == 'short':
            await self.clear_orders(symbol)
            bbid, _ = await self.fetch_condition_orders(symbol, price)
            await self.limit_order('buy', bbid, amount, symbol)
        elif self.need_reset:
            await self.clear_orders(symbol)

    async def none_action(self, symbol):
        if self.need_reset:
            await self.clear_orders(symbol)

    async def close(self):
        """Корректное закрытие соединения"""
        if self._exchange:
            await self._exchange.close()