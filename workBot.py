from Traders.BitgetTrader import BitgetTrader
from Bots.RL1 import RL1
from strategies.work_strategies.STA_ml import STAML1_XGBR2 as WS
from time import sleep

trader = BitgetTrader()
# strategy = WS("DOGEUSDT","5m",period=4,multiplier=0.5)
strategy = WS("DOGEUSDT","1m",period=60,future_steps=5)
bot = RL1("DOGEUSDT",trader,strategy,30,1)
# trader.need_reset = False

while True:
    # print(strategy())
    bot.run()
    sleep(5)