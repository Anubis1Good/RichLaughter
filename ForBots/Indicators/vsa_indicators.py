import pandas as pd
import numpy as np

def get_rails(row,df:pd.DataFrame):
    if row.name < 1:
        return 0
    prev = df.loc[row.name-1]
    if prev['is_big'] or row['is_big']:
        if prev['direction'] == 1:
            if row['low'] <= prev['low']:
                return -1
        if prev['direction'] == -1:
            if row['high'] >= prev['high']:
                return 1
    return 0

def get_cancel_rails(row,df:pd.DataFrame):
    if row.name < 1:
        return 0
    prev = df.loc[row.name-1]
    if row['rails'] == 1:
        return 
    
stop_long,stop_short = -1,-1
def get_stop_price(row):
    global stop_long,stop_short
    if row.name > 1:
        if row['rails'] == 1:
            stop_long = row['low']
        if row['rails'] == -1:
            stop_short = row['high']
    return np.array([stop_long,stop_short])

def add_stop_price(df:pd.DataFrame):
    """add stop_long,stop_short"""
    points = df.apply(get_stop_price,axis=1)
    points = np.stack(points.values)
    df['stop_long'] = pd.Series(points[:,0])
    df['stop_short'] = pd.Series(points[:,1])
    return df

def add_rails(df:pd.DataFrame):
    """add 'rails', 'stop_long', 'stop_short'"""
    df['rails'] = df.apply(lambda row: get_rails(row,df),axis=1)
    df = add_stop_price(df)
    return df

fl,fs,ps = 0,0,0
def get_period_slice(row):
    global fl,fs, ps
    if not fl:
        if row['rails'] == 1:
            fl = row.name
    if not fs:
        if row['rails'] == -1:
            fs = row.name
    ps = max(fl,fs)

def add_rails_slice(df:pd.DataFrame):
    df.apply(get_period_slice,axis=1)
    df_slice  = df.iloc[ps:]
    df_slice = df_slice.reset_index(drop=True)
    return df_slice

def add_allowance_rails(df:pd.DataFrame):
    """add 'allowance', 'sc'"""
    df['sc'] = df.apply(lambda row: max(row['spred_channel_long'],row['spred_channel_short']),axis=1)
    df['allowance'] = df['sc'] < df['delta_2v']
    return df

def add_spred(df:pd.DataFrame):
    'add "spred"'
    df['spred'] = df['high'] - df['low']
    return df

def get_ogta2_info(row,df:pd.DataFrame):
    info = 0
    if row.name > 1:
        prev = df.loc[row.name-1]
        if prev['spred'] > prev['mean_spred']:
            if prev['low'] > row['low']:
                info -= 1
            if prev['high'] < row['high']:
                info += 1
    return info
    
def add_OGTA2_rails_info(df:pd.DataFrame):
    'add "info"'
    df['info'] = df.apply(lambda row: get_ogta2_info(row,df),axis=1)
    return df