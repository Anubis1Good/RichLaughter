from Traders.BitgetTrader import BitgetTrader
from Bots.RL1 import RL1
from strategies.work_strategies.PTA import PTA2_DDCr as WS
from time import sleep

trader = BitgetTrader()
# strategy = WS("DOGEUSDT","5m",period=3,multiplier=0.5)
strategy = WS("DOGEUSDT","5m",period=2)
bot = RL1("DOGEUSDT",trader,strategy,25,1)


while True:
    # print(strategy())
    bot.run()
    sleep(5)