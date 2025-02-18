import os
import pandas as pd

def get_minute_eq(row):
    timer = row['variant'].split('_')[-1]
    if 'm' in timer:
        mult = int(timer.replace('m',''))
    elif 'H' in timer:
        mult = int(timer.replace('H',''))*60
    return row['total_average_fee_percent']/mult


folder_name = 'TestResults'
data_folder = 'data'
folders = os.listdir(folder_name)
df_main = pd.DataFrame(columns=['name','total_per','total_min_fee_percent','total_max_fee_percent','total_average_fee_percent','count','variant'])
for folder in folders:
    print(folder)
    full_path_folder = os.path.join(folder_name,folder)
    if os.path.isdir(full_path_folder):
        variants = os.listdir(full_path_folder)
        for variant in variants:
            path_bot = os.path.join(full_path_folder,variant,data_folder,folder + '.xlsx')
            df_work = pd.read_excel(path_bot,'total')
            df_work = df_work.sort_values(by='total_average_fee_percent',axis=0,ascending=False)
            df_work = df_work.head(3)
            df_work = df_work.reindex(columns = ['name','total_per','total_min_fee_percent','total_max_fee_percent','total_average_fee_percent','count'])
            df_work['variant'] = variant
            df_main = pd.concat([df_main,df_work],axis=0)
df_main['minute_eq'] = df_main.apply(get_minute_eq,axis=1)
df_main = df_main.sort_values(by='minute_eq',axis=0,ascending=False)
df_main = df_main.reset_index(drop=True)
path_df_main = os.path.join(folder_name,'Total.xlsx')
with pd.ExcelWriter(path_df_main) as writer:  
    df_main.to_excel(writer,sheet_name='total') 

