from Bots.TestBot1 import TestBot1
from strategies.work_strategies.PTA import PTA8_LOBSTER as WS
from time import sleep


# strategy = WS("DOGEUSDT","1m",period=2)
strategy = WS("DOGEUSDT","3m",period=4,multiplier=0.5)
bot = TestBot1("DOGEUSDT",strategy)


while True:
    # print(strategy())
    bot.run()
    sleep(1)