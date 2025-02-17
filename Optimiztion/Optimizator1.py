import os
import itertools
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
from collections import defaultdict
from Loader.BitgetLoader import bitget_loader
from strategies.test_strategies.check import check_strategy
def generate_combinations(ps):
    # Используем itertools.product для генерации всех возможных комбинаций
    combinations = list(itertools.product(*ps))
    return combinations

class Optimizator1:
    def __init__(self,ws,ts,params,min_fee=0.0004,max_fee=0.0012):
        self.ws = ws
        self.ts = ts
        self.configs = generate_combinations(params)
        self.min_fee = min_fee
        self.max_fee = max_fee
        self.average_fee = (max_fee+min_fee)/2
        self.name_bot = str(type(ws())).split('.')[-1][:-2]
    
    def run(self,raw_file:str):
        data_folder,images_folder = self.create_folders(raw_file)
        data = defaultdict(list)
        for conf in tqdm(self.configs):
            df = bitget_loader(raw_file)
            bot = self.ws('BTCUSDT',"1m","usdt-futures",1,*conf)
            df = bot.get_test_df(df)
            trades,longs,shorts,closes,equity = check_strategy(df,self.ts,bot)
            if trades['count'] != 0:
                total_without_fee = (trades['total']/trades['open_price'])*100
                min_fee = trades['count']*trades['open_price']*self.min_fee
                max_fee = trades['count']*trades['open_price']*self.max_fee
                average_fee = trades['count']*trades['open_price']*self.average_fee
                total_min_fee = trades['total'] - min_fee
                total_max_fee = trades['total'] - max_fee
                total_average_fee = trades['total'] - average_fee
                name_file = self.name_bot +"_"+ "_".join(list(map(str,conf)))
                # percent_min_fee = (min_fee/trades['open_price'])*100
                # percent_max_fee = (max_fee/trades['open_price'])*100
                # percent_average_fee = (average_fee/trades['open_price'])*100
                total_min_fee_percent = (total_min_fee/trades['open_price'])*100
                total_max_fee_percent = (total_max_fee/trades['open_price'])*100
                total_average_fee_percent = (total_average_fee/trades['open_price'])*100
                data['name'].append(name_file)
                data['total'].append(trades['total'])
                data['total_min_fee'].append(total_min_fee)
                data['total_max_fee'].append(total_max_fee)
                data['total_average_fee'].append(total_average_fee)
                data['total_per'].append(total_without_fee)
                data['total_min_fee_percent'].append(total_min_fee_percent)
                data['total_max_fee_percent'].append(total_max_fee_percent)
                data['total_average_fee_percent'].append(total_average_fee_percent)
                data['count'].append(trades['count'])
                for i,el in enumerate(conf):
                    data['param'+str(i)].append(el)
                full_name_img = os.path.join(images_folder,name_file +'.png')
                plt.plot(equity,color='blue')
                plt.savefig(full_name_img)
                plt.close()
        full_name_doc = os.path.join(data_folder,self.name_bot +'.xlsx')
        df = pd.DataFrame(data)
        with pd.ExcelWriter(full_name_doc) as writer:  
            df.to_excel(writer,sheet_name='total')         

    def create_folders(self,raw_file):
        sep = '\\' if '\\' in raw_file else '/'
        variant_name = raw_file.split(sep)[-1]
        variant_name = variant_name.split('_')
        variant_name = variant_name[0]+'_'+variant_name[1]
        folder_name = os.path.join("TestResults",self.name_bot)
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)
        folder_variant = os.path.join(folder_name,variant_name)
        if not os.path.exists(folder_variant):
            os.mkdir(folder_variant)
        data_folder = os.path.join(folder_variant,'data')
        if not os.path.exists(data_folder):
            os.mkdir(data_folder)
        images_folder = os.path.join(folder_variant,'images')
        if not os.path.exists(images_folder):
            os.mkdir(images_folder)
        return data_folder,images_folder