from request_functions.download_moex import download_moex,create_df
from datetime import date, timedelta
from utils.work_with_dataframe.convert_timeframe import convert_chart1to5
from ForBots.Indicators.classic_indicators import add_vodka_channel
import pandas as pd
today = date.today()

# Вычитаем один день, чтобы получить вчерашнюю дату
yesterday = str(today - timedelta(days=3))
ticker = 'MMM5'
board = "RFUD"
market = "forts"
engine= "futures"

# ticker = 'GMKN'
# board = "TQBR"
# market: str = "shares"
# engine: str = "stock"
df = download_moex(ticker,1,yesterday,board=board,market=market,engine=engine)
df = create_df(df)
df.info()
# df = convert_chart1to5(df)
# df = add_vodka_channel(df,7)
df.info()
print(df.head())
print(df.tail())
