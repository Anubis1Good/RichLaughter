from Traders.TestingTrader.TestingTrader1 import TestingTrader1
from Traders.TestingTrader.tickers_groups import tickersMoexFut
from Traders.TestingTrader.wss_maps import skynetTestMap

exchange = 'MOEX'
spec = 'FUT'
db_path = f'dbs/Skynet_{exchange}_{spec}.db'

tt1 = TestingTrader1(exchange,spec,db_path,tickersMoexFut,skynetTestMap)

tt1.run()