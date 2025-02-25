import os
import pandas as pd

def join_df(path,res_path,sort_by='ts'):
    files = os.listdir(path)
    # symbol = files[0].split('_')[0]
    for i,file in enumerate(files):
        print(i,'/',len(files))
        path_file = os.path.join(path,file)
        if i == 0:
            df_main = pd.read_csv(path_file)
        else:
            df_work = pd.read_csv(path_file)
            df_main = pd.concat([df_main,df_work])
    main_file = os.path.join(res_path)
    df_main = df_main.sort_values(sort_by,ascending=True)
    # df_main['size_volume'] = round(df_main['price'] * df_main['size'],2)
    df_main = df_main.drop('Unnamed: 0',axis=1)
    df_main = df_main.reset_index(drop=True)
    df_main.to_csv(main_file)