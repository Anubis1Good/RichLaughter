import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
mult = 1

# raw_folder = 'logsOffTest'
logs_folder = 'logsMT'
raws_folder = os.listdir(logs_folder)
for raw_folder in raws_folder:
    raw_folder_path = os.path.join(logs_folder,raw_folder)
    raw_files = os.listdir(raw_folder_path)
    date = ".".join(reversed(str(datetime.now()).split(' ')[0].replace('-','.').split('.')))
    # result_name = "_".join(raw_files[0].split('_')[1:3])
    result_name = raw_folder + date
    print(raw_folder)
    min_fee: float = 0.0004
    max_fee: float = 0.0012
    if raw_folder == 'bitget':
        min_fee: float = 0.0004
        max_fee: float = 0.0012
    if raw_folder == 'MOEX':
        min_fee = 0.0002
        max_fee = 0.0009
    average_fee = (max_fee + min_fee)/2
    df_main = pd.DataFrame(columns=['name','total_abs','count','mean_price'])
    # df_main = pd.DataFrame(columns=['name','total_abs','total_per','total_min_fee_percent','total_max_fee_percent','total_average_fee_percent','count'])
    res_name_folder = os.path.join('TestDeepTests',date,result_name)
    if not os.path.exists(res_name_folder):
        os.makedirs(res_name_folder)
    path_imgs = os.path.join(res_name_folder,'equity_chart')
    if not os.path.exists(path_imgs):
        os.mkdir(path_imgs)

    for rw in raw_files:
        rw_path = os.path.join(raw_folder_path,rw)
        df = pd.read_json(rw_path)
        df = df.drop(0,axis=0)
        name_bot = rw.replace('.json','')
        if len(df.index) > 1:
            if pd.isnull(df.iloc[-1]['close_time']):
                index = df.iloc[-1].name
                df = df.drop(index,axis=0)
            df_w = pd.DataFrame({
                'name':[name_bot],
                'total_abs':[df.iloc[-1]['total']],
                'count':len(df.index),
                'mean_price':[df['open_price'].mean()]
            })
            df_main = pd.concat([df_main,df_w],axis=0)
            plt.plot(df['total'],color='blue')
            full_name_img = os.path.join(path_imgs,name_bot + '.png')
            plt.savefig(full_name_img)
            plt.close()
    df_main['total_min_fee'] = df_main['total_abs'] - (df_main['mean_price'] * min_fee * df_main['count'] * 2)
    df_main['total_average_fee'] = df_main['total_abs'] - (df_main['mean_price'] * average_fee * df_main['count'] * 2)
    df_main['total_max_fee'] = df_main['total_abs'] - (df_main['mean_price'] * max_fee * df_main['count'] * 2)
    df_main['total_per'] = (df_main['total_abs']/df_main['mean_price']) * 100
    df_main['total_min_fee_percent'] = (df_main['total_min_fee']/df_main['mean_price']) * 100
    df_main['total_average_fee_percent'] = (df_main['total_average_fee']/df_main['mean_price']) * 100
    df_main['total_max_fee_percent'] = (df_main['total_max_fee']/df_main['mean_price']) * 100
    df_main = df_main.sort_values(by='total_average_fee_percent',axis=0,ascending=False)
    df_main = df_main.reset_index(drop=True)
    df_main = df_main.drop(['mean_price','total_min_fee','total_average_fee','total_max_fee'],axis=1)
    file_name = 'Total_' + result_name + '.xlsx'
    path_df_main = os.path.join(res_name_folder,file_name)
    with pd.ExcelWriter(path_df_main, engine='xlsxwriter') as writer:  
        df_main.to_excel(writer,sheet_name='total')
        workbook = writer.book
        worksheet = writer.sheets['total']
        for i, col in enumerate(df_main.columns,start=1):
            width = max(df_main[col].apply(lambda x: len(str(x))).max(), len(col))
            worksheet.set_column(i, i, width)
        for i, col in enumerate(df_main.columns,start=1):
                # Цветовая шкала
            worksheet.conditional_format(1, i, len(df_main), i, {
                'type': 'cell',
                'criteria': 'less than',
                'value': 0,
                'format': workbook.add_format({'bg_color': '#FFC7CE', 'font_color': '#9C0006'})
            })
            worksheet.conditional_format(1, i, len(df_main), i, {
                'type': '3_color_scale',
                'min_color': '#DA9694',
                'mid_color': '#FFFFFF',
                'max_color': '#00B0F0'
            })
        # Форматируем колонку, начиная со второй строки (первая строка - заголовок)
        # writer._save()