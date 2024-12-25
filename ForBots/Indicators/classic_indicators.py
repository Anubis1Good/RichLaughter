import pandas as pd
import numpy as np

def get_donchan_channel(row,df:pd.DataFrame,period=20,delay=0):
    x = int(row['x'])
    df_short = df.iloc[x-period:x+1]
    max_hb = df_short['high'].max()
    min_hb = df_short['low'].min()
    avarage = (min_hb + max_hb)//2

    return np.array([max_hb,min_hb,avarage])

def add_donchan_channel(df:pd.DataFrame,period=20,delay=0):
    df_slice  = df.iloc[period:]
    points = df_slice.apply(lambda row: get_donchan_channel(row,df,period,delay),axis=1)
    points = np.stack(points.values)
    df_slice = df_slice.reset_index()
    df_slice = df_slice.drop('index',axis=1)
    df_slice['max_hb'] = pd.Series(points[:,0])
    df_slice['min_hb'] = pd.Series(points[:,1])
    df_slice['avarege'] = pd.Series(points[:,2])
    return df_slice