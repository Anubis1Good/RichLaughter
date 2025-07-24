from time import sleep
import sys
from Bots.TestBot3 import backup_sqlite_db
from Traders.TestingTrader.TestingTrader1 import TestingTrader1
from Traders.TestingTrader.tickers_groups import tickersBitgetFut,tickersMoexFut,tickersMoexStock,tickersMoexFut2
from Traders.TestingTrader.wss_maps import bitgetFutMap,moexFutMap,moexStockMap,bitgetMTAFutMap,moexMTAFutMap,moexMTAStockMap,moexFutMap2

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
elif exchange == 'MOEXM':
    if spec == 'FUT':
        tickers = tickersMoexFut
        wss_map = moexMTAFutMap
    else:
        tickers = tickersMoexStock
        wss_map = moexMTAStockMap
elif exchange == 'MOEX2':
    if spec == 'FUT':
        tickers = tickersMoexFut2
        wss_map = moexFutMap2
    # else:
    #     tickers = tickersMoexStock
    #     wss_map = moexMTAStockMap
elif exchange == 'Bitget':
    tickers = tickersBitgetFut
    wss_map = bitgetFutMap
elif exchange == 'BitgetM':
    tickers = tickersBitgetFut
    wss_map = bitgetMTAFutMap
else:
    sys.exit(0)

db_path = f'dbs/test_{exchange}_{spec}.db'

tt1 = TestingTrader1(exchange,spec,db_path,tickers,wss_map)

if mode == 'run':
    backup_sqlite_db(db_path)
    sys.stdout.write(f"{db_path} starting...\n")
    sys.stdout.flush()
    tt1.run()
elif mode == 'close':
    sys.stdout.write(f"{db_path} closing...\n")
    sys.stdout.flush()
    tt1.close_all_pos()
sys.exit(1)