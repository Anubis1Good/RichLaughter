from Traders.BitgetTrader import BitgetTrader
from Bots.RL1 import RL1
from strategies.work_strategies.PTA import PTA2_BDDC
from time import sleep

trader = BitgetTrader()
strategy = PTA2_BDDC(10,"DOGEUSDT","1m")
bot = RL1("DOGEUSDT",trader,strategy,25,5)


while True:
    # print(strategy())
    bot.run()
    sleep(10)