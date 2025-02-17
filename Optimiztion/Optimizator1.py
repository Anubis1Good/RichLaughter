import os
import itertools
import pandas as pd
import matplotlib.pyplot as plt
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
    
    def run(self,raw_file):
        folder_name = os.path.join("TestResults",self.name_bot)
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)
        data_folder = os.path.join(folder_name,'data')
        if not os.path.exists(data_folder):
            os.mkdir(data_folder)
        images_folder = os.path.join(folder_name,'images')
        if not os.path.exists(images_folder):
            os.mkdir(images_folder)
        
        for conf in self.configs:
            df = bitget_loader(raw_file)
            bot = self.ws('BTCUSDT',"1m","usdt-futures",1,*conf)
            df = bot.get_test_df(df)
            trades,longs,shorts,closes,equity = check_strategy(df,self.ts,bot)
            total_without_fee = (trades['total']/trades['open_price'])*100
            min_fee = trades['count']*trades['open_price']*self.min_fee
            max_fee = trades['count']*trades['open_price']*self.max_fee
            average_fee = trades['count']*trades['open_price']*self.average_fee
            percent_min_fee = (min_fee/trades['open_price'])*100
            percent_max_fee = (max_fee/trades['open_price'])*100
            percent_average_fee = (average_fee/trades['open_price'])*100

            total_min_fee = trades['total'] - min_fee
            total_min_fee_percent = (total_min_fee/trades['open_price'])*100
            total_max_fee = trades['total'] - max_fee
            total_max_fee_percent = (total_max_fee/trades['open_price'])*100
            total_average_fee = trades['total'] - average_fee
            total_average_fee_percent = (total_average_fee/trades['open_price'])*100

            name_file = self.name_bot + "_".join(list(map(str,conf)))
            # full_name_doc = os.path.join(data_folder,name_file +'.xlsx')
            full_name_img = os.path.join(data_folder,name_file +'.png')
            plt.plot(equity,color='blue')
            plt.savefig(full_name_img)
            plt.close()