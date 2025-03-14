from Traders.BitgetTrader import BitgetTrader
from Bots.RL1 import RL1
from strategies.work_strategies.PTA import PTA4_WDDCr as WS
from time import sleep

trader = BitgetTrader()
# strategy = WS("DOGEUSDT","5m",period=4,multiplier=0.5)
strategy = WS("DOGEUSDT","5m",period=10,threshold=30)
bot = RL1("DOGEUSDT",trader,strategy,35,1)
# trader.need_reset = False

while True:
    # print(strategy())
    bot.run()
    sleep(5)