from time import time
from datetime import date,timedelta
from request_functions.download_bitget import save_df,download_bitget_ticks
from Loader.ApiMoexLoader import ApiMoexLoader
from datetime import date,timedelta

today = date.today()
start_date = str(today - timedelta(days=30))
# # start_date = '2025-02-01'

# tickers = ('IMOEXF','MMZ5','RMZ5','SRZ5','GAZPF','SBERF','SVZ5','GZZ5',)
# folder_save = 'DataForTests\DataMoexFutP'
# tickers = ('ROSN','LSRG','CBOM','TRMK','NMTP','SELG','RUAL','MTLR','VTBR','GMKN','APTK','KZOSP','UWGN')
tickers = ('MTLR','IVAT','SGZH','EUTR','VTBR','RNFT','DATA','RAGR','SPBE','MAGN','VKCO','ASTR','ALRS','RUAL','IRAO','SMLT','T','ENPG','SBER','HYDR','SBERP','SELG','AQUA','AFLT','SFIN','ROSN')
folder_save = 'DataForTests\DataMoexStockP'
for ticker in tickers:
    # loader = ApiMoexLoader(ticker,'RFUD','forts','futures')
    loader = ApiMoexLoader(ticker)
    loader.save_df(start_date,timeframe=1,sformat='parquet',folder_save=folder_save)

# end = int(time())*1000
# week = 60*60*24*7*1000 - 1000
# start = end-week
# download_bitget_ticks(symbol="DOGEUSDT",start=start,end=end)
# from request_functions.download_bybit import save_df
# tickers_bybit = ('ADAUSDT','ENAUSDT','1000PEPEUSDT','WIFUSDT','XRPUSDT')
# # tickers_bybit = ('ADAUSDT',)

# for ticker in tickers_bybit:
#     save_df(ticker,'5',500)
# tickers_bitget = ('TRXUSDT','DOGEUSDT','XLMUSDT','XTZUSDT','SUSHIUSDT')
# for ticker in tickers_bitget:
#     save_df(ticker,'5m',n_parts=500)
# ts = ('1m','5m','15m','30m','1H')
# for t in ts:
#     print(t,'start')
#     save_df(symbol="DOGEUSDT",n_parts=100,granularity=t)
#     print(t,'done')




# today = date.today()
# start_date = str(today - timedelta(days=60))
# # start_date = '2025-02-01'
# fut = True
# # fut = False
# from request_functions.download_moex import save_df
# tickers = ['NGU5','BRV5','MMU5','RMU5','GZU5','IMOEXF','SRU5','SVU5']
# # tickers = ['IMOEXF']
# # tickers = ['CNYRUBF']
# # tickers = ['SRU5','CRU5','CNYRUBF','EDU5']
# # tickers = ['UWGN','QIWI','APTK','KZOSP','CBOM','TRMK','SELG','GMKN','VTBR','MTLR','NMTP','ROSN','FESH','RUAL','LSRG']
# # from Traders.TestingTrader.tickers_groups import tickersMoexStock2
# # tickers = [x[0] for x in tickersMoexStock2]
# print(tickers)# # tickers = ['SBER','ROSN','GAZP',"MTLR","VTBR","NLMK"]
# folder_save = 'DataForTests\DataFromMoexForStepTests'
# # folder_save = 'DataForTests\DataFromMoexFastStock'
# for ticker in tickers:
#     print(ticker)
#     if fut:
#         board = "RFUD"
#         market = "forts"
#         engine= "futures"
#         save_df(ticker,1,start_date,board=board,market=market,engine=engine,folder_save=folder_save)
#     else:
#         board = "TQBR"
#         save_df(ticker,1,start_date,folder_save=folder_save)





