import shutil
from time import time
import pandas as pd
from Optimiztion.Optimizator1 import generate_combinations
from Bots.TestBot1 import TestBot1offline
from Loader.BitgetLoader import bitget_loader
from strategies.work_strategies.PTA import PTA2_BDDC,PTA2_BDDCde,PTA2_BDDCr,PTA2_DDCde,PTA2_VOLCHARA,PTA2_LISICA,PTA8_LOBSTER,PTA2_BDVCr,PTA2_UDC,PTA2_AUDC,PTA9_CRAB,PTA2_DDCrWork,PTA8_DOBBY,PTA8_OBBY,PTA8_OBBY_PF,PTA8_DOBBY_FREE,PTA8_DOBBY_FREEr,PTA4_WDDCde,PTA4_WDDCr,PTA2_DDCrVG,PTA2_DVCr,PTA2_KOLOBOK,PTA2_ZAYAC,PTA8_FOBBY,PTA8_LOBBY,PTA8_OBBY_FREE,PTA8_OBBY_FREEr,PTA8_OBBY_VOR,PTA9_RAB
from strategies.work_strategies.STA_ml import STAML1_XGBR2,STAML1_XGBR3_User,STAML1_XGBR4,STAML1_XGBR5,STAML1_XGBR6,STAML1_XGBR7,STAML1_XGBR8,STAML1_ARIMAS1,STAML1_PROPHET1
from strategies.work_strategies.STA_ca import STA1_LITE
from strategies.work_strategies.LTA import LTA_APHOBO,LTA_APHOGA,LTA_BORSCH,LTA_MISO
from time import sleep
# raw_file = 'DataForTests\oldBitget\DOGEUSDT_1m_1741087742_big.csv'

shutil.rmtree("logsOffTest")

multiplier = 1
raw_file = 'DataForTests\TicksBidgetUnion\DOGEUSDT_union.csv'
df = pd.read_csv(raw_file)
len_df = len(df.index)
bots = []
wss = []
params1 = [
    [3,4] + list(range(5,66,5)),
    (10,20,30,40)
]
group = (
    (PTA4_WDDCde,params1),
)
for ws,params in group:
    configs = generate_combinations(params)
    for conf in configs:
        wss.append((ws,conf))

# wss = [
#     (STAML1_XGBR2,(60,5)),
#     (STAML1_XGBR2,(5,5)),
#     (STAML1_ARIMAS1,(20,(1, 1, 1),50)),
#     (STAML1_PROPHET1,(20,)),
#     (LTA_PHOBO,(10,3)),
#     (LTA_PHOGA,(10,3)),
#     (LTA_BORSCH,(20,14)),
#     (LTA_MISO,(52,9,26,52,14,12,26,9)),
# ]
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

# df_chart = pd.DataFrame(columns=['ms','open','high','low','close','vol_coin','volume','direction','middle','x','cm'])
candels = []
cur_candel = {
    'ms',
    'open',
    'high',
    'low',
    'close',
    'vol_coin',
    'volume',
    'direction',
    'middle',
    'cm'
}

# price,size,side,ts,size_volume
def change_candles(row):
    cm = row['ts']//(1000*60*multiplier)
    try:
        is_cm = cm == candels[-1]['cm']
    except:
        is_cm = False
    if candels and is_cm:
        last_candel = candels.pop()
        cur_candel = {
            'ms':row['ts'],
            'open':last_candel['open'],
            'high':row['price'] if row['price'] > last_candel['high'] else last_candel['high'],
            'low':row['price'] if row['price'] < last_candel['low'] else last_candel['low'],
            'close':row['price'],
            'vol_coin':row['size'] + last_candel['vol_coin'],
            'volume':row['size_volume'] + last_candel['volume'],
            'direction':1 if last_candel['open'] < row['price'] else -1,
            'middle':row['price'],
            'cm':cm
        }
        cur_candel['middle'] = (cur_candel['low'] + cur_candel['high'])/2
    else:
        cur_candel = {
            'ms':row['ts'],
            'open':row['price'],
            'high':row['price'],
            'low':row['price'],
            'close':row['price'],
            'vol_coin':row['size'],
            'volume':row['size_volume'],
            'direction':1,
            'middle':row['price'],
            'cm':cm
        }
    candels.append(cur_candel)
    if len(candels) > max_period:
        candels.pop(0)

def simulation_chart(row):
    start = time()
    change_candles(row)
    df_work = pd.DataFrame(candels)
    df_work['x'] = df_work.index
    len_df_work = len(df_work.index)
    if len_df_work == max_period:
        for bot in bots:
            bot.run(df_work)
    remains = len_df - row.name
    end = time() - start
    remains_sec = remains * end
    hour = int(remains_sec // 3600)
    minutes = int((remains_sec % 3600) // 60)
    sec = int((remains_sec % 3600) % 60)
    remains_time = f'{hour}:{minutes}:{sec}'
    print(row.name,'/',len_df,'len_df_work:',len_df_work,'len_wss:',len(wss),'remains_time:',remains_time)

df.apply(simulation_chart,axis=1)
# cm = row['ts']//(1000*60*multiplier)

# for i in tqdm(range(len(df.index))):

