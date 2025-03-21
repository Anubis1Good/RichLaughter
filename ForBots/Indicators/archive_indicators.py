import pandas as pd
import numpy as np

def get_vodka_channel(row,df:pd.DataFrame,period=20):
    if row.name < period:
        return np.array([-1,-1,-1])
    df_short = df.iloc[row.name-period:row.name+1]
    max_hb = df_short['high'].median()
    min_hb = df_short['low'].median()
    avarage = (min_hb + max_hb)/2

    return np.array([max_hb,min_hb,avarage])

def add_vodka_channel_old(df:pd.DataFrame,period=20):
    '''add top_mean, bottom_mean, avarege_mean'''
    points = df.apply(lambda row: get_vodka_channel(row,df,period),axis=1)
    points = np.stack(points.values)
    df['top_mean'] = pd.Series(points[:,0])
    df['bottom_mean'] = pd.Series(points[:,1])
    df['avarege_mean'] = pd.Series(points[:,2])
    return df

def get_donchan_channel(row,df:pd.DataFrame,period=20):
    if row.name < period:
        return np.array([-1,-1,-1])
    df_short = df.iloc[row.name-period:row.name+1]
    max_hb = df_short['high'].max()
    min_hb = df_short['low'].min()
    avarage = (min_hb + max_hb)/2

    return np.array([max_hb,min_hb,avarage])

def add_donchan_channel_old(df:pd.DataFrame,period=20):
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
    # if 'shape' in dir(middle_max):
    #     print(row['max_hb'])
    #     print(prev['max_hb'])
    return np.array([middle_max,middle_min])

def add_donchan_middle(df:pd.DataFrame):
    """add 'middle_max','middle_min'"""
    points = df.apply(lambda row: get_donchan_middle(row,df),axis=1)
    # for p in points:
    #     print(p.shape,p)
    points = np.stack(points.values)
    df['middle_max'] = pd.Series(points[:,0])
    df['middle_min'] = pd.Series(points[:,1])
    return df


def get_donchan_prev(row,df:pd.DataFrame,top='max_hb',bottom='min_hb'):
    prev_max,prev_min = -1,-1
    if row.name > 1:
        prev = df.loc[row.name-1]
        prev_min = prev[bottom]
        prev_max = prev[top]
    return np.array([prev_max,prev_min])

def add_donchan_prev(df:pd.DataFrame,top='max_hb',bottom='min_hb'):
    """add 'prev_max','prev_min'"""
    points = df.apply(lambda row: get_donchan_prev(row,df,top,bottom),axis=1)
    points = np.stack(points.values)
    df['prev_max'] = pd.Series(points[:,0])
    df['prev_min'] = pd.Series(points[:,1])
    return df

def add_vangerchik_old(df:pd.DataFrame):
    """add max_vg, min_vg"""
    df['max_vg'] = df.apply(lambda row: row['max_hb'] - (row['max_hb']-row['min_hb'])/10,axis=1)
    df['min_vg'] = df.apply(lambda row: row['min_hb'] + (row['max_hb']-row['min_hb'])/10,axis=1)
    return df

def get_sma(row,df:pd.DataFrame,period=20,kind='middle'):
    if row.name < period:
        return -1
    df_short = df.iloc[row.name-period:row.name+1]
    return df_short[kind].mean()

def add_sma_old(df:pd.DataFrame,period=20,kind='close'):
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

def add_bollinger_old(df:pd.DataFrame,period=20,kind='close',multiplier=2):
    '''add bbu, bbd, sma'''
    points = df.apply(lambda row: get_bollinger(row,df,period,kind,multiplier),axis=1)
    points = np.stack(points.values)
    df['bbu'] = pd.Series(points[:,0])
    df['bbd'] = pd.Series(points[:,1])
    df['sma'] = pd.Series(points[:,2])
    return df