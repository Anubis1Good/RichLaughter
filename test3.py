from pprint import pprint
from Traders.TestingTrader.TestingTrader1 import TestingTrader1
from Traders.TestingTrader.tickers_groups import tickersBitgetFut,tickersMoexFut
from Traders.TestingTrader.wss_maps import bitgetFutMap,moexFutMap


# tt1 = TestingTrader1('Bitget','FUT','dbs/test_bitget.db',tickersBitgetFut,bitgetFutMap)
# pprint(tt1.map_bots)
tt1 = TestingTrader1('MOEX','FUT','dbs/test_moex_fut.db',tickersMoexFut,moexFutMap)
# pprint(tt1.map_bots)
# tt1.run()
