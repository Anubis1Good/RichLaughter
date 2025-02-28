from Bots.TestBot1 import TestBot1
from strategies.work_strategies.PTA import PTA2_DDCde,PTA2_KOLOBOK,PTA2_ZAYAC,PTA8_LOBSTER,PTA8_LOBBY,PTA2_BDVCr,PTA8_FOBBY,PTA2_UDC,PTA9_CRAB,PTA2_DDCrWork,PTA9_RAB,PTA8_OBBY,PTA8_OBBY_VOR,PTA8_OBBY_PF,PTA8_OBBY_FREE,PTA8_OBBY_FREEr,PTA2_BDDCm,PTA8_OOBBY_FREE,PTA8_OOBBY,PTA8_OOBBY_FREEr,PTA2_ALKASH
from strategies.work_strategies.STA_ml import STAML1_XGBR2
from strategies.work_strategies.STA_ca import STA1_LITE
from strategies.work_strategies.LTA import LTA_LAKSA,LTA_LAKSAe
from strategies.work_strategies.OGTA import OGTA3_Rails
from time import sleep

bots = []
wss = [
    (STAML1_XGBR2,(60,5)),
    (STAML1_XGBR2,(5,5)),
    (PTA8_OBBY,(5,0.5)),
    (PTA8_OBBY_VOR,(5,0.5)),
    (PTA8_LOBSTER,(4,0.5)),
    (PTA8_OBBY_PF,(5,0.5)),
    (PTA8_FOBBY,(5,0.5)),
    (PTA8_OBBY_FREEr,(4,0.5)),
    (PTA8_OBBY_FREE,(4,0.5)),
    (PTA8_LOBBY,(4,0.5)),
    (PTA2_BDVCr,(2,)),
    (PTA2_BDDCm,(5,)),
    (PTA2_UDC,(3,5)),
    (PTA2_ZAYAC,(3,2)),
    (PTA2_KOLOBOK,(3,2)),
    (PTA8_OOBBY_FREE,(5,0.5)),
    (LTA_LAKSAe,(40,3)),
    (LTA_LAKSA,(10,5)),
    (PTA9_RAB,(5,2,10,0.5)),
    (PTA8_OOBBY,(55,0.5)),
    (PTA8_OOBBY_FREEr,(20,1)),
    (PTA2_DDCde,(5,)),
    (OGTA3_Rails,(20,)),
    (STA1_LITE,(5,1,0.5,15)),
    (PTA2_ALKASH,(40,)),
    (PTA9_CRAB,(10,0.5,5,0.5)),
    (PTA2_DDCrWork,(5,)),

]
print(len(wss))
for WS,conf in wss:
    strategy = WS("DOGEUSDT","5m","usdt-futures",1,*conf)
    bot = TestBot1("DOGEUSDT",strategy,conf)
    bots.append(bot)


while True:
    # print(strategy())
    for bot in bots:
        bot.run()
        sleep(0.1)