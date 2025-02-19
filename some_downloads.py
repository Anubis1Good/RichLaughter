
from request_functions.download_bitget import save_df
from request_functions.download_moex import save_df


# save_df(symbol="DOGEUSDT",n_parts=50,granularity='1m')
start_date = '2025-02-01'
fut = True
# fut = False
if fut:
    board = "RFUD"
    ticker = 'MMH5'
    market = "forts"
    engine= "futures"
    save_df(ticker,1,start_date,board=board,market=market,engine=engine)
else:
    board = "TQBR"
    ticker = 'SNGSP'
    save_df(ticker,1,start_date)





