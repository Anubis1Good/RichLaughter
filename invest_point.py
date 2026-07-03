import os
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
from datetime import date,timedelta
from ForBots.Indicators.mult_indicators import add_crysis_counter
from Loader.ApiMoexLoader import ISSMoexLoader
from utils.draw_utils import draw_hb_chart_fast
from pprint import pprint

need_charts = True
need_charts = False
fut = False
# fut = True
today = date.today()
# start_date = str(today - timedelta(days=720))
start_date = {
    60:str(today - timedelta(days=7)),
    24:str(today - timedelta(days=150)),
    7:str(today - timedelta(days=720)),
}
suffix = 'F' if fut else 'S'
folder = 'TestNewResults/InvestPoint' + suffix
imgs_folder = os.path.join(folder,'charts')
if not os.path.exists(folder):
    os.makedirs(folder)
if need_charts:
    if not os.path.exists(imgs_folder):
        os.makedirs(imgs_folder)

if fut:
    board = "RFUD"
    market = "forts"
    engine= "futures"
else:
    board = "TQBR"
    market="shares"
    engine = "stock"

loader = ISSMoexLoader(board,market,engine)
df_total = loader.get_all_tickers()
# df_total.info()
# print(df_total.head())
cc_list = []
for s in tqdm(df_total['SECID']):
    try:
        cc_dict = {}
        cc_dict['SECID'] = s
        for tf in (60,24,7):
            df = loader.get_candels(s,start_date[tf],timeframe=tf)
            df = loader.processing_df_candels(df)
            df = add_crysis_counter(df)
            cc_dict['cc_'+str(tf)] = round(df['crysis_index'].values[-1],2)
            if need_charts:
                name_file = f'{s}_{tf}.png'
                name_file = os.path.join(imgs_folder,name_file)
                draw_hb_chart_fast(df)
                plt.savefig(name_file)
                plt.close()
        cc_list.append(cc_dict)
    except:
        print(s,'some_error')
    # break
cc_df = pd.DataFrame(cc_list)
# cc_df.info()
# print(cc_df.head())

df_total = pd.merge(cc_df,df_total,on='SECID')
df_total = df_total.sort_values('cc_24')
# df_total.info()
# print(df_total.head())
# print(df_total.tail())
with pd.ExcelWriter(os.path.join(folder,'InvestPoint.xlsx'), engine='xlsxwriter') as writer:  
    df_total.to_excel(writer,sheet_name='total')
    workbook = writer.book
    worksheet = writer.sheets['total']
    for i, col in enumerate(df_total.columns,start=1):
        width = max(df_total[col].apply(lambda x: len(str(x))).max(), len(col))
        worksheet.set_column(i, i, width)