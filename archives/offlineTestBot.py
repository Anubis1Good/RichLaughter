from tqdm import tqdm
from Bots.TestBot1 import TestBot1offline
from Loader.BitgetLoader import bitget_loader
from strategies.work_strategies.PTA import PTA2_BDDC,PTA2_BDDCde,PTA2_BDDCr,PTA2_DDCde,PTA2_VOLCHARA,PTA2_LISICA,PTA8_LOBSTER,PTA2_BDVCr,PTA2_UDC,PTA2_AUDC,PTA9_CRAB,PTA2_DDCrWork,PTA8_DOBBY,PTA8_OBBY,PTA8_OBBY_PF,PTA8_DOBBY_FREE,PTA8_DOBBY_FREEr,PTA4_WDDCde,PTA4_WDDCr,PTA2_DDCrVG,PTA2_DVCr,PTA2_KOLOBOK,PTA2_ZAYAC,PTA8_FOBBY,PTA8_LOBBY,PTA8_OBBY_FREE,PTA8_OBBY_FREEr,PTA8_OBBY_VOR,PTA9_RAB
from strategies.work_strategies.STA_ml import STAML1_XGBR2,STAML1_XGBR3_User,STAML1_XGBR4,STAML1_XGBR5,STAML1_XGBR6,STAML1_XGBR7,STAML1_XGBR8,STAML1_ARIMAS1,STAML1_PROPHET1,STAML1_AXGBR2,STAML1_SARIMAS1
from strategies.work_strategies.STA_ca import STA1_LITE
from strategies.work_strategies.LTA import LTA_PHOBO,LTA_PHOGA,LTA_BORSCH,LTA_MISO
from time import sleep
# raw_file = 'DataForTests\oldBitget\DOGEUSDT_1m_1741087742_big.csv'
raw_file = 'DataForTests\DataFromBitget\DOGEUSDT_1m_1739873922.csv'
df = bitget_loader(raw_file)
bots = []
wss = [
    (STAML1_XGBR2,(60,5)),
    (STAML1_XGBR2,(5,5)),
    (STAML1_AXGBR2,(60,5)),
    (STAML1_SARIMAS1,(20,)),
    (STAML1_PROPHET1,(20,)),
    # (LTA_PHOBO,(10,3)),
    # (LTA_PHOGA,(10,3)),
    # (LTA_BORSCH,(20,14)),
    # (LTA_MISO,(52,9,26,52,14,12,26,9)),
]
# wss = [
#     (STAML1_LR1,(60,5)),
# ]
print(len(wss))
for WS,conf in wss:
    strategy = WS("DOGEUSDT","5m","usdt-futures",1,*conf)
    bot = TestBot1offline("DOGEUSDT",strategy,conf)
    bots.append(bot)
periods = [i[1][0] for i in wss]
max_period = max(periods)*2

for i in tqdm(range(max_period,len(df.index))):
    df_work = df.iloc[i-max_period:i]
    for bot in bots:
        bot.run(df_work)
