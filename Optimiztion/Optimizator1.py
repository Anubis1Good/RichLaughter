import os
import itertools
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
from multiprocessing import Pool, cpu_count
from collections import defaultdict
from Loader.BitgetLoader import bitget_loader
from strategies.test_strategies.check import check_strategy

import psutil
phys_cores = psutil.cpu_count(logical=False) 

def generate_combinations(ps):
    # Используем itertools.product для генерации всех возможных комбинаций
    combinations = list(itertools.product(*ps))
    return combinations

class Optimizator1:
    def __init__(self,ws,ts,params,min_fee=0.0004,max_fee=0.0012,need_plot=False):
        self.ws = ws
        self.ts = ts
        self.configs = generate_combinations(params)
        self.min_fee = min_fee
        self.max_fee = max_fee
        self.average_fee = (max_fee+min_fee)/2
        self.name_bot = str(type(ws())).split('.')[-1][:-2]
        self.need_plot = need_plot
    
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
                if self.need_plot:
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

# TODO мультипроцессорный оптимизатор
class Optimizator2(Optimizator1):
    def process_config(self,args):
        conf, self_ref, raw_file = args
        self = self_ref  # получаем ссылку на экземпляр класса
        
        df = bitget_loader(raw_file)
        bot = self.ws('BTCUSDT', "1m", "usdt-futures", 1, *conf)
        df = bot.get_test_df(df)
        trades, longs, shorts, closes, equity = check_strategy(df, self.ts, bot)
        
        result = None
        if trades['count'] != 0:
            total_without_fee = (trades['total']/trades['open_price'])*100
            min_fee = trades['count']*trades['open_price']*self.min_fee
            max_fee = trades['count']*trades['open_price']*self.max_fee
            average_fee = trades['count']*trades['open_price']*self.average_fee
            
            result = {
                'name': self.name_bot + "_" + "_".join(list(map(str, conf))),
                'total': trades['total'],
                'total_min_fee': trades['total'] - min_fee,
                'total_max_fee': trades['total'] - max_fee,
                'total_average_fee': trades['total'] - average_fee,
                'total_per': total_without_fee,
                'total_min_fee_percent': (trades['total'] - min_fee)/trades['open_price']*100,
                'total_max_fee_percent': (trades['total'] - max_fee)/trades['open_price']*100,
                'total_average_fee_percent': (trades['total'] - average_fee)/trades['open_price']*100,
                'count': trades['count'],
                'conf': conf,
                'equity': equity
            }
        return result

    def run(self, raw_file):
        data_folder, images_folder = self.create_folders(raw_file)
        data = defaultdict(list)
        
        # Подготовка аргументов для каждого процесса
        args = [(conf, self, raw_file) for conf in self.configs]
        
        # Используем количество ядер, но можно задать меньше для экономии памяти
        num_processes = min(max(1, phys_cores - 2), len(self.configs))
        print('Use',num_processes,'cores')
        with Pool(processes=num_processes) as pool:
            # Используем imap_unordered для более быстрого выполнения (порядок не важен)
            results = list(tqdm(pool.imap_unordered(self.process_config, args), total=len(self.configs)))
        
        # Обработка результатов
        for result in results:
            if result:
                name_file = result['name']
                data['name'].append(name_file)
                data['total'].append(result['total'])
                data['total_min_fee'].append(result['total_min_fee'])
                data['total_max_fee'].append(result['total_max_fee'])
                data['total_average_fee'].append(result['total_average_fee'])
                data['total_per'].append(result['total_per'])
                data['total_min_fee_percent'].append(result['total_min_fee_percent'])
                data['total_max_fee_percent'].append(result['total_max_fee_percent'])
                data['total_average_fee_percent'].append(result['total_average_fee_percent'])
                data['count'].append(result['count'])
                
                for i, el in enumerate(result['conf']):
                    data[f'param{i}'].append(el)
                
                # Сохранение графика
                if self.need_plot:
                    full_name_img = os.path.join(images_folder, name_file + '.png')
                    plt.plot(result['equity'], color='blue')
                    plt.savefig(full_name_img)
                    plt.close()
        
        # Сохранение результатов в Excel
        full_name_doc = os.path.join(data_folder, self.name_bot + '.xlsx')
        df = pd.DataFrame(data)
        df = df.sort_values('total_min_fee_percent',axis=0,ascending=False).reset_index(drop=True)
        df = df.drop(['total_min_fee','total_max_fee','total_average_fee'],axis=1)
        with pd.ExcelWriter(full_name_doc, engine='xlsxwriter') as writer:  
            df.to_excel(writer, sheet_name='total')
            worksheet = writer.sheets['total']
            for i, col in enumerate(df.columns,start=1):
                width = max(df[col].apply(lambda x: len(str(x))).max(), len(col))
                worksheet.set_column(i, i, width)
            # Создаем список для хранения результатов
            influence_results = []

            # Анализируем влияние каждого параметра
            for i in range(len(result['conf'])):  # param0-param6
                param_name = f'param{i}'
                grouped = df.groupby(param_name)['total_min_fee_percent'].agg(['mean','median']).reset_index()
                grouped.columns = ['param_value', 'mean_tmfp','median_tmfp']
                grouped['parameter'] = param_name
                influence_results.append(grouped)

            # Объединяем все результаты в один датафрейм
            influence_df = pd.concat(influence_results, ignore_index=True)

            # Сортируем для наглядности
            influence_df = influence_df.sort_values(['parameter', 'mean_tmfp'], 
                                                ascending=[True, False])
            influence_df.to_excel(writer, sheet_name='params')
            worksheet = writer.sheets['params']
            workbook = writer.book
            for i, col in enumerate(influence_df.columns,start=1):
                width = max(influence_df[col].apply(lambda x: len(str(x))).max(), len(col))
                worksheet.set_column(i, i, width)
                worksheet.conditional_format(1, i, len(influence_df), i, {
                    'type': 'cell',
                    'criteria': 'less than',
                    'value': 0,
                    'format': workbook.add_format({'bg_color': '#FFC7CE', 'font_color': '#9C0006'})
                })
                worksheet.conditional_format(1, i, len(influence_df), i, {
                        'type': '3_color_scale',
                        'min_color': '#DA9694',
                        'mid_color': '#FFFFFF',
                        'max_color': '#00B0F0'
                    })