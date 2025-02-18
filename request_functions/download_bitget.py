import os
import pandas as pd
from time import time, sleep
from request_functions.get_bitget import get_history_candles,get_candles
import matplotlib.pyplot as plt
from tqdm import tqdm

def get_multiplier(granularity:str):
    multiplier = None
    if 'm' in granularity:
        multiplier = int(granularity.replace('m',''))
        return multiplier
    elif 'H' in granularity:
        multiplier = int(granularity.replace('H',''))*60
    elif 'D' in granularity:
        multiplier = int(granularity.replace('H',''))*60*24
    return multiplier

def download_bitget(symbol="BTCUSDT",granularity="1m",productType="usdt-futures",n_parts=10,limit="200"):
    step = 200
    t = int(time())*1000
    r = range(1,n_parts+1)
    multiplier = get_multiplier(granularity)
    for i in reversed(r):
        startTime = t - step*60*1000*i*multiplier
        endTime = t - step*60*1000*(i-1)*multiplier
        if i == r[-1]:
            res = get_history_candles(symbol=symbol,granularity=granularity,productType=productType, startTime=startTime,endTime=endTime,limit=limit)
        else:
            res += get_history_candles(symbol=symbol,granularity=granularity,productType=productType, startTime=startTime,endTime=endTime,limit=limit)
        # sleep(0.1)
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
    df = df.reset_index()
    df['x'] = df.index
    df = df.drop(['index'],axis=1)
    return df

def get_df(symbol="BTCUSDT",granularity="1m",productType="usdt-futures",limit="200"):
    """K-line particle size
    - 1m(1 minute)
    - 3m(3 minutes)
    - 5m(5 minutes)
    - 15m(15 minutes)
    - 30m(30 minutes)
    - 1H( 1 hour)
    - 4H(4 hours)
    - 6H(6 hours)
    - 12H(12 hours)
    - 1D(1 day)
    - 3D ( 3 days)
    - 1W (1 week)
    - 1M (monthly line)
    - 6Hutc (UTC 6 hour line)
    - 12Hutc (UTC 12 hour line)
    - 1Dutc (UTC 1-day line)
    - 3Dutc (UTC 3-day line)
    - 1Wutc (UTC weekly line)
    - 1Mutc (UTC monthly line)
    """
    df = get_candles(symbol,granularity,productType,limit)
    df = create_df(df)
    return df

def save_df(symbol="BTCUSDT",granularity="1m",productType="usdt-futures",n_parts=10):
    """K-line particle size
    - 1m(1 minute)
    - 3m(3 minutes)
    - 5m(5 minutes)
    - 15m(15 minutes)
    - 30m(30 minutes)
    - 1H( 1 hour)
    - 4H(4 hours)
    - 6H(6 hours)
    - 12H(12 hours)
    - 1D(1 day)
    - 3D ( 3 days)
    - 1W (1 week)
    - 1M (monthly line)
    - 6Hutc (UTC 6 hour line)
    - 12Hutc (UTC 12 hour line)
    - 1Dutc (UTC 1-day line)
    - 3Dutc (UTC 3-day line)
    - 1Wutc (UTC weekly line)
    - 1Mutc (UTC monthly line)
    """
    df = download_bitget(symbol,granularity,productType,n_parts)
    df = create_df(df)
    path = os.path.join('DataForTests/DataFromBitget',symbol+"_"+granularity+'_'+str(time()).split(".")[0]+'.csv')
    df.to_csv(path)

