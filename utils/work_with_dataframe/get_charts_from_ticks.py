import pandas as pd
import os
from time import time
cur_minute = 0
df_chart = pd.DataFrame(columns=['ms','open','high','low','close','vol_coin','volume','direction','middle','x'])
x = 0
def get_chart(row,multiplier=1):
    global cur_minute,x
    cm = row['ts']//(1000*60*multiplier)
    if cm != cur_minute:
        cur_minute = cm
        df_chart.loc[x] = pd.Series({
            'ms':row['ts'],
            'open':row['price'],
            'high':row['price'],
            'low':row['price'],
            'close':row['price'],
            'vol_coin':row['size'],
            'volume':row['size_volume'],
            'direction':1,
            'middle':row['price'],
            'x':x
        })
        x += 1
    else:
        prev = df_chart.iloc[-1]
        if prev['high'] < row['price']:
            prev['high'] = row['price']
        if prev['low'] > row['price']:
            prev['low'] = row['price']
        prev['close'] = row['price']
        prev['vol_coin'] += row['size']
        prev['volume'] += row['size_volume']
        if prev['open'] <= prev['close']:
            prev['direction'] = 1
        else:
            prev['direction'] = -1
        prev['middle'] = (prev['high'] + prev['low'])/2


def get_chart_from_ticks(path_ticks:str,multiplier:int=1):
    stock_name= path_ticks.split('\\')[-1].split('_')[0]
    df = pd.read_csv(path_ticks)
    df = df.apply(lambda row: get_chart(row,multiplier),axis=1)
    df_chart.to_csv(f'DataForTests\DataFromTicksBitget\{stock_name}_{multiplier}m_from_ticks.csv')


# Cumulative bars
cur_minute_cum = 0
df_chart_cum = pd.DataFrame(columns=['ms','open','high','low','close','vol_coin','volume','direction','middle','x'])
x_cum = 0
count_candels = 0
def get_chart_cum(row,multiplier=1,df_size=0,stock_name='0',output_folder='.'):
    global cur_minute_cum,x_cum,count_candels,df_chart_cum
    cm = row['ts']//(1000*60*multiplier)
    if cm != cur_minute_cum:
        if count_candels == 30//multiplier:
            df_chart_cum.to_csv(f'{output_folder}\{stock_name}_{multiplier}m_from_ticks_{time()}.csv')
            count_candels = 0
            df_chart_cum = pd.DataFrame(columns=['ms','open','high','low','close','vol_coin','volume','direction','middle','x'])
            print(x_cum,'/',df_size)
        cur_minute_cum = cm
        df_chart_cum.loc[x_cum] = pd.Series({
            'ms':row['ts'],
            'open':row['price'],
            'high':row['price'],
            'low':row['price'],
            'close':row['price'],
            'vol_coin':row['size'],
            'volume':row['size_volume'],
            'direction':1,
            'middle':row['price'],
            'x':x_cum
        })
        count_candels += 1
    else:
        prev = df_chart_cum.iloc[-1]
        high = max(row['price'],prev['high'])
        low = min(row['price'],prev['low'])
        direction = 1 if prev['open'] <= row['price'] else -1
        df_chart_cum.loc[x_cum] = pd.Series({
            'ms':row['ts'],
            'open':prev['open'],
            'high':high,
            'low':low,
            'close':row['price'],
            'vol_coin':prev['vol_coin']+row['size'],
            'volume':prev['volume']+row['size_volume'],
            'direction':direction,
            'middle':(high + low)/2,
            'x':x_cum
        })
    x_cum += 1


def get_chart_from_ticks_cum(path_ticks:str,multiplier:int=1):
    stock_name= path_ticks.split('\\')[-1].split('_')[0]
    df = pd.read_csv(path_ticks)
    df_size = len(df.index)
    sep_name = 'sep'+str(multiplier)
    output_folder = f'DataForTests\DataFromTicksBitgetCum\{sep_name}'
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    df = df.apply(lambda row: get_chart_cum(row,multiplier,df_size,stock_name,output_folder),axis=1)
    df_chart_cum.to_csv(f'{output_folder}\{stock_name}_{multiplier}m_from_ticks_{time()}.csv')


