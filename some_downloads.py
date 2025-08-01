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
start_date = str(today - timedelta(days=45))
# start_date = '2025-02-01'
fut = True
# fut = False
from request_functions.download_moex import save_df
tickers = ['NGN5','BRQ5','MMU5','RMU5','GZU5','IMOEXF','EDU5','SRU5',]
# tickers = ['IMOEXF']
# tickers = ['CNYRUBF']
# tickers = ['SRU5','CRU5','CNYRUBF','EDU5']
# tickers = ['UWGN','QIWI','APTK','KZOSP']
# from Traders.TestingTrader.tickers_groups import tickersMoexStock2
# tickers = [x[0] for x in tickersMoexStock2]
print(tickers)# # tickers = ['SBER','ROSN','GAZP',"MTLR","VTBR","NLMK"]
folder_save = 'DataForTests\DataFromMoexForStepTests'
for ticker in tickers:
    print(ticker)
    if fut:
        board = "RFUD"
        market = "forts"
        engine= "futures"
        save_df(ticker,1,start_date,board=board,market=market,engine=engine,folder_save=folder_save)
    else:
        board = "TQBR"
        save_df(ticker,1,start_date)





