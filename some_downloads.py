from time import time
from request_functions.download_bitget import save_df,download_bitget_ticks

end = int(time())*1000
week = 60*60*24*7*1000 - 1000
start = end-week
download_bitget_ticks(symbol="DOGEUSDT",start=start,end=end)
# save_df(symbol="DOGEUSDT",n_parts=50,granularity='1m')
# start_date = '2025-02-01'
# fut = True
# # fut = False
# from request_functions.download_moex import save_df
# if fut:
#     board = "RFUD"
#     ticker = 'MMH5'
#     market = "forts"
#     engine= "futures"
#     save_df(ticker,1,start_date,board=board,market=market,engine=engine)
# else:
#     board = "TQBR"
#     ticker = 'SNGSP'
#     save_df(ticker,1,start_date)





