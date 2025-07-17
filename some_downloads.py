from time import time
from datetime import date,timedelta
from request_functions.download_bitget import save_df,download_bitget_ticks

end = int(time())*1000
week = 60*60*24*7*1000 - 1000
start = end-week
# download_bitget_ticks(symbol="DOGEUSDT",start=start,end=end)
ts = ('1m','5m','15m','30m','1H')
# for t in ts:
#     print(t,'start')
#     save_df(symbol="DOGEUSDT",n_parts=100,granularity=t)
#     print(t,'done')
today = date.today()
start_date = str(today - timedelta(days=30))
# start_date = '2025-02-01'
fut = True
# fut = False
from request_functions.download_moex import save_df
tickers = ['MMU5','IMOEXF','CRU5','RMU5','GZU5']
# tickers = ['MMM5','GZM5','CRM5','RMM5']
# # tickers = ['SBER','ROSN','GAZP',"MTLR","VTBR","NLMK"]
for ticker in tickers:
    print(ticker)
    if fut:
        board = "RFUD"
        market = "forts"
        engine= "futures"
        save_df(ticker,1,start_date,board=board,market=market,engine=engine,folder_save='DataForTests\DataFromMoexForStepTests')
    else:
        board = "TQBR"
        save_df(ticker,1,start_date)





