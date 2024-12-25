import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
from Loader.QuikLoader import quik_loader
from utils.draw_utils import draw_lite_chart,draw_chart_channel
from ForBots.Indicators.classic_indicators import add_donchan_channel
raw_file = 'DataForTests\DataFromQuik\SPBFUT.MMU4_T1.txt'
# raw_file = 'DataForTests\DataFromQuik\SPBFUT.CRU4_T1.txt'

df = quik_loader(raw_file)
# df = df.iloc[0:200]
# df.info()
df = add_donchan_channel(df,15)

trades = {
    'pos':0,
    'open_price':0,
    'total':0,
    'count':0
}
longs = []
shorts = []
closes = []

equity = []

def get_action_PTA2_DDC(row):
    if row['high'] == row['max_hb']:
        if trades['pos'] == 0:
            trades['pos'] = -1
            shorts.append((row.name,row['high']))
            trades['open_price'] = row['high']
        elif trades['pos'] == 1:
            trades['pos'] = -1
            shorts.append((row.name,row['high']))
            trades['total'] += row['high'] - trades['open_price']
            closes.append((row.name,row['high']))
            trades['open_price'] = row['high']
            trades['count'] += 1
    elif row['low'] == row['min_hb']:
        if trades['pos'] == 0:
            trades['pos'] = 1
            longs.append((row.name,row['low']))
            trades['open_price'] = row['low']
        elif trades['pos'] == -1:
            trades['pos'] = 1
            longs.append((row.name,row['low']))
            trades['total'] += trades['open_price'] - row['low']
            closes.append((row.name,row['low']))
            trades['count'] += 1
            trades['open_price'] = row['low']
    else:
        if row['low'] <= row['avarege']:
            if trades['pos'] == -1:
                trades['pos'] = 0
                trades['total'] += row['low'] - trades['open_price']
                closes.append((row.name,row['low']))
                trades['count'] += 1
        if row['high'] >= row['avarege']:
            if trades['pos'] == 1:
                trades['pos'] = 0
                trades['total'] += trades['open_price'] - row['high']
                closes.append((row.name,row['high']))
                trades['count'] += 1
    equity.append(trades['total'])

# print(df[df['x'] == 41])
df.apply(get_action_PTA2_DDC,axis=1)
print(trades)

longs = np.array(longs)
shorts = np.array(shorts)
closes = np.array(closes)
equity = np.array(equity)

# draw_lite_chart(df)
# draw_chart_channel(df)
# plt.scatter(longs[:,0],longs[:,1],marker='^')
# plt.scatter(shorts[:,0],shorts[:,1],marker='v')
# plt.scatter(closes[:,0],closes[:,1],marker='x')
plt.plot(equity)
plt.show()