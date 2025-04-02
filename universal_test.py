from time import sleep
import sys
from Traders.TestingTrader.TestingTrader1 import TestingTrader1
from Traders.TestingTrader.tickers_groups import tickersBitgetFut,tickersMoexFut,tickersMoexStock
from Traders.TestingTrader.wss_maps import bitgetFutMap,moexFutMap,moexStockMap

args = sys.argv[1:]
exchange = args[0]
spec =  args[1]
mode = args[2]
if exchange == 'MOEX':
    if spec == 'FUT':
        tickers = tickersMoexFut
        wss_map = moexFutMap
    else:
        tickers = tickersMoexStock
        wss_map = moexStockMap
elif exchange == 'Bitget':
    tickers = tickersBitgetFut
    wss_map = bitgetFutMap
else:
    sys.exit(0)

db_path = f'dbs/test_{exchange}_{spec}.db'

tt1 = TestingTrader1(exchange,spec,db_path,tickers,wss_map)

if mode == 'run':
    sys.stdout.write(f"{db_path} starting...\n")
    sys.stdout.flush()
    tt1.run()
elif mode == 'close':
    sys.stdout.write(f"{db_path} closing...\n")
    sys.stdout.flush()
    tt1.close_all_pos()
sys.exit(1)