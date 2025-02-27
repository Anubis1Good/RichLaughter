from Bots.TestBot1 import TestBot1
from strategies.work_strategies.PTA import PTA2_DDCde,PTA2_KOLOBOK,PTA2_ZAYAC,PTA8_LOBSTER,PTA8_LOBBY,PTA2_BDVCr,PTA8_FOBBY,PTA2_UDC,PTA8_DOBBY_FREEr,PTA9_CRAB,PTA2_DDCrWork,PTA9_RAB

from time import sleep

bots = []
wss = [
    (PTA2_DDCde,(5,)),
    (PTA2_KOLOBOK,(5,)),
    (PTA2_ZAYAC,(3,2)),
    (PTA8_LOBSTER,(4,0.5)),
    (PTA8_LOBBY,(4,0.5)),
    (PTA2_BDVCr,(4,)),
    (PTA8_FOBBY,(3,1.5)),
    (PTA2_UDC,(10,27)),
    (PTA8_DOBBY_FREEr,(5,2.5)),
    (PTA9_CRAB,(10,0.5,5,0.5)),
    (PTA2_DDCrWork,(2,)),
    (PTA9_RAB,(5,2,10,0.5))
]
for WS,conf in wss:
    strategy = WS("DOGEUSDT","5m","usdt-futures",1,*conf)
    # strategy = WS("DOGEUSDT","1m",period=4,multiplier=0.5)
    bot = TestBot1("DOGEUSDT",strategy)
    bots.append(bot)


while True:
    # print(strategy())
    for bot in bots:
        bot.run()
        sleep(0.1)