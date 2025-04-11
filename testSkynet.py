from Traders.TestingTrader.TestingTrader1 import TestingTrader1
from Traders.TestingTrader.tickers_groups import tickersMoexFut
from strategies.work_strategies.MTA_KING import MTA_KING

wssMoexSkynet1 = (
    (MTA_KING,(100,'KING_1_MOEX_FUT')),
)

wssMoexSkynet5 = (
    (MTA_KING,(100,'KING_5_MOEX_FUT')),
)

skynetTestMap = {
    1:wssMoexSkynet1,
    5:wssMoexSkynet5
}

exchange = 'MOEX'
spec = 'FUT'
db_path = f'dbs/king_king{exchange}_{spec}.db'

tt1 = TestingTrader1(exchange,spec,db_path,tickersMoexFut,skynetTestMap)

tt1.run()