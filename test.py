import requests
import hmac
import base64
from time import time, sleep
from request_functions.get_bitget import get_history_candles,get_candles
from request_functions.download_bitget import save_df
import ccxt
from utils.settings import settings
from Traders.BitgetTrader import BitgetTrader
import numpy as np
import matplotlib.pyplot as plt

save_df(symbol="DOGEUSDT",n_parts=50,granularity='1m')
# res = get_candles(limit=1000)
# print(len(res))

# symbol = 'DOGEUSDT'
# bg_trader = BitgetTrader()
# ob = bg_trader._exchange.fetch_order_book(symbol)

# orders = bg_trader.open_orders()
# print(orders)
# print(bg_trader.balance())
# order = bg_trader.limit_order(side='buy',price=0.2,size=50,sl=0.1,symbol='DOGEUSDT',target=0.3)
# order = bg_trader.limit_order('buy',0.2,50,'DOGEUSDT',0.1,0.3)
# order = bg_trader.limit_order('buy',0.2,50,'DOGEUSDT')
# print(order)
# bg_trader.cancel_order(orders[0]['info']['symbol'],orders[0]['info']['orderId'])




