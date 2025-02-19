import os
from time import time
import requests
import apimoex
import pandas as pd

def download_moex(ticker,interval,start,end=None,board: str = "TQBR",market:str="shares", engine:str = "stock"):
    with requests.Session() as session:
        data = apimoex.get_board_candles(session, ticker,interval,start,end,board=board,market=market,engine=engine)
        df = pd.DataFrame(data)

        return df
    
def create_df(df:pd.DataFrame):
    df = df.rename(columns={'value':"vol_coin",'begin':'ms'})
    df['direction'] = df.apply(lambda row: 1 if row['open'] < row['close'] else -1, axis=1)
    df['middle'] = df.apply(lambda row: (row['high']+row['low'])/2,axis=1)
    df = df.reset_index()
    df['x'] = df.index
    df = df.drop(['index'],axis=1)
    return df

def save_df(ticker,interval,start,end=None,board: str = "TQBR",market:str="shares", engine:str = "stock"):
    """K-line particle size
        1 - 1 минута
        10 - 10 минут
        60 - 1 час
        24 - 1 день
        7 - 1 неделя
        31 - 1 месяц
        4 - 1 квартал
    """
    df = download_moex(ticker,interval,start,end,board,market,engine)
    df = create_df(df)
    path = os.path.join('DataForTests/DataFromMOEX',ticker+"_"+str(interval)+'_'+str(time()).split(".")[0]+'.csv')
    df.to_csv(path)