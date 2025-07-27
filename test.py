symbol = '1000PEPEUSDT'
from request_functions.download_bybit import save_df

save_df(symbol,'1',n_parts=2)

# print(candles[-1])
# print(len(candles))