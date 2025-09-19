import os
import pandas as pd
from time import time,sleep
from request_functions.get_bybit import get_bybit_history_candles
from tqdm import tqdm
# import datetime

# TODO
def download_bybit(symbol="BTCUSDT",granularity="1",n_parts=10):
    step = 200
    t = int(time())*1000
    r = range(1,n_parts+1)
    multiplier = int(granularity)
    for i in tqdm(reversed(r)):
        startTime = t - step*60*1000*i*multiplier
        endTime = t - step*60*1000*(i-1)*multiplier
        print(startTime,endTime)
        if i == r[-1]:
            res = get_bybit_history_candles(symbol,granularity,startTime=startTime,endTime=endTime)
        else:
            res += get_bybit_history_candles(symbol,granularity,startTime=startTime,endTime=endTime)
        sleep(0.1)
    return res


def create_df(df):
    df = pd.DataFrame(df,columns=["ms","open","high","low","close","vol_coin","volume"])
    for c in df.columns:
        if c == 'ms':
            df[c] = df[c].apply(int)
        else:
            df[c] = df[c].apply(float)
    df['direction'] = df.apply(lambda row: 1 if row['open'] < row['close'] else -1, axis=1)
    df['middle'] = df.apply(lambda row: (row['high']+row['low'])/2,axis=1)
    df = df.sort_values('ms',axis=0)
    df = df.reset_index()
    df['x'] = df.index
    df = df.drop(['index'],axis=1)
    return df

def save_df(symbol="BTCUSDT",granularity="60",n_parts=10,path_folder='DataForTests/DataFromBybit'):
    """    - symbol: торговая пара (BTCUSDT)
    - interval: таймфрейм:
      - 1,3,5,15,30,60,120,240,360,720 (минуты)
      - D, W, M (день, неделя, месяц)
    """
    df = download_bybit(symbol,granularity,n_parts)
    print(df[-1])
    df = create_df(df)
    df.info()
    print(df.head())
    print(df.tail())
    if not os.path.exists(path_folder):
        os.makedirs(path_folder)
    path = os.path.join(path_folder,symbol+"_"+str(granularity)+'_'+str(time()).split(".")[0]+'.csv')
    df.to_csv(path)