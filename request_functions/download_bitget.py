import os
import pandas as pd
from time import time, sleep
from request_functions.get_bitget import get_history_candles
import matplotlib.pyplot as plt
from tqdm import tqdm

def download_bitget(symbol="BTCUSDT",granularity="1m",productType="usdt-futures",n_parts=10):
    step = 200
    t = int(time())*1000
    r = range(1,n_parts+1)
    for i in tqdm(reversed(r)):
        startTime = t - step*60*1000*i
        endTime = t - step*60*1000*(i-1)
        if i == r[-1]:
            res = get_history_candles(symbol=symbol,granularity=granularity,productType=productType, startTime=startTime,endTime=endTime)
        else:
            res += get_history_candles(symbol=symbol,granularity=granularity,productType=productType, startTime=startTime,endTime=endTime)
        sleep(0.5)
    return res

def save_df(symbol="BTCUSDT",granularity="1m",productType="usdt-futures",n_parts=10):
    df = download_bitget(symbol,granularity,productType,n_parts)
    df = pd.DataFrame(df,columns=["ms","open","high","low","close","vol_coin","volume"])
    for c in df.columns:
        if c == 'ms':
            df[c] = df[c].apply(int)
        else:
            df[c] = df[c].apply(float)
    df['direction'] = df.apply(lambda row: 1 if row['open'] < row['close'] else -1, axis=1)
    df = df.reset_index()
    df['x'] = df.index
    df = df.drop(['index'],axis=1)
    path = os.path.join('DataForTests/DataFromBitget',symbol+str(time()).split(".")[0]+'.csv')
    df.to_csv(path)

