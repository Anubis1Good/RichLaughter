from utils.draw_utils import draw_hb_chart,draw_hbwv_chart
import traceback
import pandas as pd
import matplotlib.pyplot as plt
from strategies.work_strategies.PTA import PTA2_DDCr as WS
import json
# df = pd.read_csv('DataForTests\DataFromTicksBitgetCum\sep1\DOGEUSDT_1m_from_ticks_1740483973.4131718.csv')

# df.apply(draw_hbwv_chart,axis=1)
# plt.show()


df_fast = pd.read_csv('DataForTests\DataFromTicksBitget\DOGEUSDT_15m_from_ticks.csv')
df_slow = pd.read_csv('DataForTests\DataFromTicksBitgetCum\DOGEUSDT_15m_cum.csv')
df_fast = df_fast.drop(['Unnamed: 0'],axis=1)
df_slow = df_slow.drop(['Unnamed: 0','Unnamed: 0.1'],axis=1)
cur_minute = 0
df_slow_slice = None
slice_index = 0
ret = True

def get_moment_df(row:pd.Series,slice_fast:pd.DataFrame,multiplier:int=1):
    global cur_minute,df_slow_slice,slice_index,ret
    
    cm = row['ms']//(1000*60*multiplier)
    if cm != cur_minute:
        cur_minute = cm
        # df_slow['cm'] = df_slow['ms']//(1000*60*multiplier)
        df_slow_slice = df_slow[df_slow['ms']//(1000*60*multiplier) == cur_minute]
        slice_index = 0
    last_bar = df_slow_slice.iloc[slice_index:slice_index+1]
    slice_index += 1
    slice_fast = pd.concat([slice_fast.iloc[:-1],last_bar])
    slice_fast = slice_fast.reset_index(drop=True)
    if len(df_slow_slice.index) <= slice_index:
        print('false--------------------->')
        ret = False
    return slice_fast

period = 2
# ws = WS(period=period,multiplier=0.5,period_slow=5,slope=0.5)
ws = WS(period=period)
j = 0
len_df = len(df_fast.index)

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
# 'long_price','short_price','close_long_price','close_short_price'
bid = (0,0)
def trade_prev(row):
    global bid
    cur_price = row['close']
    if bid[0] > 0:
        if cur_price < bid[1]:
            if trades['pos'] == -1:
                trades['total'] += trades['open_price'] - bid[1]
                closes.append((row['ms'],bid[1])) 
            trades['pos'] += bid[0]
            if trades['pos'] == 1:
                longs.append((row['ms'],bid[1]))
                trades['open_price'] = bid[1]
                trades['count'] += 1
    elif bid[0] < 0:
        if cur_price > bid[1]:
            if trades['pos'] == 1:
                trades['total'] += bid[1] - trades['open_price'] 
                closes.append((row['ms'],bid[1])) 
            trades['pos'] += bid[0]
            if trades['pos'] == -1:
                shorts.append((row['ms'],bid[1]))
                trades['open_price'] = bid[1]   
                trades['count'] += 1
    
def trade_next(action,row):
    global bid
    clp = row['close_long_price']
    csp = row['close_short_price']
    lp = row['long_price']
    sp = row['short_price']
    if action:
        if 'close_long' in action:
            if trades['pos'] == 1:
                bid = (-1,clp)
            else:
                bid = (0,0)
        elif 'close_short' in action:
            if trades['pos'] == -1:
                bid = (1,csp)
            else:
                bid = (0,0)
        elif 'long' in action:
            if trades['pos'] == 1:
                bid = (0,0)
            elif trades['pos'] == -1:
                bid = (2,lp)
            else:
                bid = (1,lp)
        elif 'short' in action:
            if trades['pos'] == 1:
                bid = (-2,sp)
            elif trades['pos'] == -1:
                bid = (0,0)
            else:
                bid = (-1,sp)
    else:
        bid = (0,0)

try:
    for i in range(period*2,len_df):
        slice_fast = df_fast.iloc[i-period*2:i]
        print(cur_minute)
        while ret:
            slice_fast = get_moment_df(df_slow.iloc[j],slice_fast)
            # print(slice_fast.tail())
            slice_fast_copy = slice_fast.copy()
            slice_fast_copy = ws.preprocessing(slice_fast_copy)
            # print(slice_fast_copy.tail())
            action = ws(slice_fast_copy.iloc[-1])
            trade_prev(slice_fast_copy.iloc[-1])
            trade_next(action,slice_fast_copy.iloc[-1])
            print(i,'/',len_df)
            print(trades)
            j += 1
        ret = True
        equity.append(trades['total'])
except Exception as e:
    traceback.print_exception(e)
    slice_fast_copy.info()
last_row = df_fast.iloc[-1]
if trades['pos'] != 0:
    if trades['pos'] == 1:
        trades['total'] += last_row['close'] - trades['open_price'] 
    elif trades['pos'] == -1:
        trades['total'] += trades['open_price'] - last_row['close']
    trades['pos'] = 0
    closes.append((last_row['ms'],last_row['close'])) 
    equity.append(trades['total'])
print(trades)
plt.plot(equity,color='blue')
plt.savefig('test.png')
plt.close()
with open('test.json','w') as f:
    json.dump([trades,longs,shorts,closes,equity],f)