from Traders.BitgetTrader import BitgetTrader
from Bots.RL1 import RL1
from strategies.work_strategies.MTA_KING import MTA_KING as WS
from time import sleep

trader = BitgetTrader()
# strategy = WS("DOGEUSDT","5m",period=4,multiplier=0.5)
strategy = WS("DOGEUSDT","30m",period=300,pick_file='uKING_30m_Bitget_FUT')
bot = RL1("DOGEUSDT",trader,strategy,30,1)
# trader.need_reset = False

while True:
    # print(strategy())
    bot.run()
    sleep(5)