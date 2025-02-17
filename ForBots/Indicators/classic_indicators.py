import math
import pandas as pd
import numpy as np

def add_slice_df(df:pd.DataFrame,period=20):
    df_slice  = df.iloc[period:]
    df_slice = df_slice.reset_index(drop=True)
    return df_slice

def get_donchan_channel(row,df:pd.DataFrame,period=20):
    if row.name < period:
        return np.array([-1,-1,-1])
    df_short = df.iloc[row.name-period:row.name+1]
    max_hb = df_short['high'].max()
    min_hb = df_short['low'].min()
    avarage = (min_hb + max_hb)/2

    return np.array([max_hb,min_hb,avarage])

def add_donchan_channel(df:pd.DataFrame,period=20):
    points = df.apply(lambda row: get_donchan_channel(row,df,period),axis=1)
    points = np.stack(points.values)
    df['max_hb'] = pd.Series(points[:,0])
    df['min_hb'] = pd.Series(points[:,1])
    df['avarege'] = pd.Series(points[:,2])
    return df

def add_vangerchik(df:pd.DataFrame):
    df['max_vg'] = df.apply(lambda row: row['max_hb'] - (row['max_hb']-row['min_hb'])/10,axis=1)
    df['min_vg'] = df.apply(lambda row: row['min_hb'] + (row['max_hb']-row['min_hb'])/10,axis=1)
    return df

def get_sma(row,df:pd.DataFrame,period=20,kind='middle'):
    if row.name < period:
        return -1
    df_short = df.iloc[row.name-period:row.name+1]
    return df_short[kind].mean()

def add_sma(df:pd.DataFrame,period=20,kind='middle'):
    df['sma'] = df.apply(lambda row: get_sma(row,df,period,kind),axis=1)
    return df

def get_bollinger(row,df:pd.DataFrame,period=20,kind='middle',multiplier=2):
    if row.name < period:
        return np.array([-1,-1,-1])
    df_short = df.iloc[row.name-period:row.name+1]
    std = df_short[kind].std()
    sma = df_short[kind].mean()
    bbu = sma + std*multiplier
    bbd = sma - std*multiplier

    return np.array([bbu,bbd,sma])

def add_bollinger(df:pd.DataFrame,period=20,kind='middle',multiplier=2):
    points = df.apply(lambda row: get_bollinger(row,df,period,kind,multiplier),axis=1)
    points = np.stack(points.values)
    df['bbu'] = pd.Series(points[:,0])
    df['bbd'] = pd.Series(points[:,1])
    df['sma'] = pd.Series(points[:,2])
    return df

def add_over_bb(df:pd.DataFrame):
    df['over_bbu'] = df.apply(lambda row: row['bbu'] < row['low'],axis=1)
    df['over_bbd'] = df.apply(lambda row: row['bbd'] > row['high'],axis=1)
    return df

def get_attached_bb(row,df:pd.DataFrame):
    bbu_attached = False
    bbd_attached = False
    if row.name > 1:
        prev = df.loc[row.name-1]
        if row['high'] > row['bbu'] or prev['high'] > prev['bbu']:
            bbu_attached = True
        if row['low'] < row['bbd'] or prev['low'] < prev['bbd']:
            bbd_attached = True
    return np.array([bbu_attached,bbd_attached])

def get_change_attached_bb(row,df:pd.DataFrame):
    attached_change = False
    if row.name > 1:
        prev = df.iloc[row.name-1]
        if row['bbu_attached'] != prev['bbu_attached']:
            attached_change = True
        if row['bbd_attached'] != prev['bbd_attached']:
            attached_change = True
    return attached_change
def add_attached_bb(df:pd.DataFrame):
    points = df.apply(lambda row: get_attached_bb(row,df),axis=1)
    points = np.stack(points.values)
    df['bbu_attached'] = pd.Series(points[:,0])
    df['bbd_attached'] = pd.Series(points[:,1])
    df['attached_change'] = df.apply(lambda row: get_change_attached_bb(row,df),axis=1)
    return df

def add_big_volume(df:pd.DataFrame,period=20,multiplier=1):
    df['sma_volume'] = df.apply(lambda row: get_sma(row,df,period,'volume'),axis=1)
    df['is_big'] = df.apply(lambda row: row['volume']*multiplier > row['sma_volume'],axis=1)
    return df

def add_dynamics_ma(df:pd.DataFrame,period=20,kind='sma'):
    diff = df[kind].diff()
    df[kind+'_slope'] = diff * (1/diff.mean())
    df['dynamics_ma'] = np.degrees(np.arctan(df[kind+'_slope']))
    df['dynamics_ma'] = df['dynamics_ma'].rolling(period).mean()
    df = df.drop(kind+'_slope',axis=1)
    return df
