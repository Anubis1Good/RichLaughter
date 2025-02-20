import pandas as pd
import numpy as np

def add_slice_df(df:pd.DataFrame,period=20):
    df_slice  = df.iloc[period+1:]
    df_slice = df_slice.reset_index(drop=True)
    return df_slice

def add_enter_price(df:pd.DataFrame,func):
    """add 'long_price','short_price','close_long_price','close_short_price'"""
    points = df.apply(lambda row: func(row),axis=1)
    points = np.stack(points.values)
    df['long_price'] = pd.Series(points[:,0])
    df['short_price'] = pd.Series(points[:,1])
    df['close_long_price'] = pd.Series(points[:,2])
    df['close_short_price'] = pd.Series(points[:,3])
    return df

def get_donchan_channel(row,df:pd.DataFrame,period=20):
    if row.name < period:
        return np.array([-1,-1,-1])
    df_short = df.iloc[row.name-period:row.name+1]
    max_hb = df_short['high'].max()
    min_hb = df_short['low'].min()
    avarage = (min_hb + max_hb)/2

    return np.array([max_hb,min_hb,avarage])

def add_donchan_channel(df:pd.DataFrame,period=20):
    '''add max_hb, min_hb, avarege'''
    points = df.apply(lambda row: get_donchan_channel(row,df,period),axis=1)
    points = np.stack(points.values)
    df['max_hb'] = pd.Series(points[:,0])
    df['min_hb'] = pd.Series(points[:,1])
    df['avarege'] = pd.Series(points[:,2])
    return df

def get_donchan_middle(row,df:pd.DataFrame):
    middle_max,middle_min = -1,-1
    if row.name > 1:
        prev = df.loc[row.name-1]
        middle_min = (row['min_hb'] + prev['min_hb'])/2
        middle_max = (row['max_hb'] + prev['max_hb'])/2
    return np.array([middle_max,middle_min])

def add_donchan_middle(df:pd.DataFrame):
    """add 'middle_max','middle_min'"""
    points = df.apply(lambda row: get_donchan_middle(row,df),axis=1)
    points = np.stack(points.values)
    df['middle_max'] = pd.Series(points[:,0])
    df['middle_min'] = pd.Series(points[:,1])
    return df
def get_donchan_prev(row,df:pd.DataFrame):
    prev_max,prev_min = -1,-1
    if row.name > 1:
        prev = df.loc[row.name-1]
        prev_min = prev['min_hb']
        prev_max = prev['max_hb']
    return np.array([prev_max,prev_min])

def add_donchan_prev(df:pd.DataFrame):
    """add 'prev_max','prev_min'"""
    points = df.apply(lambda row: get_donchan_prev(row,df),axis=1)
    points = np.stack(points.values)
    df['prev_max'] = pd.Series(points[:,0])
    df['prev_min'] = pd.Series(points[:,1])
    return df

def add_vangerchik(df:pd.DataFrame):
    """add max_vg, min_hb"""
    df['max_vg'] = df.apply(lambda row: row['max_hb'] - (row['max_hb']-row['min_hb'])/10,axis=1)
    df['min_vg'] = df.apply(lambda row: row['min_hb'] + (row['max_hb']-row['min_hb'])/10,axis=1)
    return df

def get_sma(row,df:pd.DataFrame,period=20,kind='middle'):
    if row.name < period:
        return -1
    df_short = df.iloc[row.name-period:row.name+1]
    return df_short[kind].mean()

def add_sma(df:pd.DataFrame,period=20,kind='middle'):
    '''add sma'''
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
    '''add bbu, bbd, sma'''
    points = df.apply(lambda row: get_bollinger(row,df,period,kind,multiplier),axis=1)
    points = np.stack(points.values)
    df['bbu'] = pd.Series(points[:,0])
    df['bbd'] = pd.Series(points[:,1])
    df['sma'] = pd.Series(points[:,2])
    return df

def add_over_bb(df:pd.DataFrame):
    '''add over_bbu and over_bbd'''
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
    """add bbu_attached, bbd_attached, attached_change"""
    points = df.apply(lambda row: get_attached_bb(row,df),axis=1)
    points = np.stack(points.values)
    df['bbu_attached'] = pd.Series(points[:,0])
    df['bbd_attached'] = pd.Series(points[:,1])
    df['attached_change'] = df.apply(lambda row: get_change_attached_bb(row,df),axis=1)
    return df

def add_big_volume(df:pd.DataFrame,period=20,multiplier=1):
    """add sma_volume, is_big """
    df['sma_volume'] = df.apply(lambda row: get_sma(row,df,period,'volume'),axis=1)
    df['is_big'] = df.apply(lambda row: row['volume']*multiplier > row['sma_volume'],axis=1)
    return df

def add_dynamics_ma(df:pd.DataFrame,period=20,kind='sma'):
    """add dynamics_ma"""
    diff = df[kind].diff()
    df[kind+'_slope'] = diff * (1/diff.mean())
    df['dynamics_ma'] = np.degrees(np.arctan(df[kind+'_slope']))
    df['dynamics_ma'] = df['dynamics_ma'].rolling(period).mean()
    df = df.drop(kind+'_slope',axis=1)
    return df

