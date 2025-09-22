from Traders.BybitTrader.BybitTrader1 import BybitTrader1
from Bots.RL1 import RL1
from strategies.work_strategies.MTA_KING import MTA_KING as WS
from time import sleep

trader = BybitTrader1()
# strategy = WS("DOGEUSDT","5m",period=4,multiplier=0.5)
strategy = WS("WIFUSDT","30m",period=300,pick_file='KING_30m_Bitget_FUT')
bot = RL1("WIFUSDT",trader,strategy,6,1)
# trader.need_reset = False

while True:
    # print(strategy())
    bot.run()
    sleep(5)