import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import psutil
from time import time 
from tqdm import tqdm
from multiprocessing import Pool
from functools import partial
from strategies.test_strategies.CheckWSTrader import CheckWSTrader
from utils.work_with_dataframe.load_df import simple_load_df
from testing.risk_map import risk_map_fut_vtb
# from Traders.TestingTrader.wss_groups import wssMoexFut5 as wss
# from Traders.TestingTrader.wss_groups import wssMoexStocks5 as wss
# map_wss = {
#     'IMOEXF_1':wss[14:],
#     'default':wss,
# }
from testing.wss_step_test import map_wss
phys_cores = psutil.cpu_count(logical=False) 

type_test = 0 # window
# type_test = 1 # child
# type_test = 69 #fast

if type_test == 0:
    main_folder = 'TestNewResults/WindowTest'
elif type_test == 1:
    main_folder = 'TestNewResults/ChildTest'
else:
    main_folder = 'TestNewResults/FastTest'
if not os.path.exists(main_folder):
    os.makedirs(main_folder)

save_cores = 1
fee_base = 0.001
window = 60
# window = 200
close_on_time = True
# close_on_time = False
normalization=True
# normalization=False
# vtb = True
vtb = False
use_risk = False
close_map = ((23,30),(23,30),(23,30),(23,30),(23,30),(17,50),(17,50),)
need_plot = True
timeframe = '5min'

# test_folder = 'DataForTests\DataMoexFutP'
test_folder = 'DataForTests\DataMoexStock5P'
test_folder = 'DataForTests\DataMoexStockP'

list_dir = os.listdir(test_folder)


def create_folder(variant_folder):
    image_folder = os.path.join(variant_folder,'images')
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)
    xls_folder = os.path.join(variant_folder,'xls')
    if not os.path.exists(xls_folder):
        os.makedirs(xls_folder)
    return image_folder,xls_folder

def process_ws(variant_name,image_folder, xls_folder, clear_df,ws):
    try:
        name_bot = str(ws[0].__name__)
        name_file = f"{name_bot}_{'_'.join(map(str, ws[1]))}"
        
        # Создаем стратегию и проверяем ее
        strategy = ws[0](variant_name, '5', "1", 1, *ws[1])
        if use_risk:
            stop_risk = risk_map_fut_vtb.get(variant_name[:-2],None)
        else:
            stop_risk = False
        cwt = CheckWSTrader(clear_df,strategy,fee_base,variant_name,timeframe,close_on_time,close_map,False,False,stop_risk)
        if type_test == 0:
            cwt.check_strategy_window(window,normalization,vtb)
        elif type_test == 1:
            cwt.check_strategy_child(timeframe,window,normalization,vtb)
        else:
            cwt.check_strategy_fast(vtb)
        print(name_file)
        # Сохраняем график если нужно
        if need_plot:
            full_name_img = os.path.join(image_folder, f"{name_file}.png")
            cwt.plot_chart_and_sequtity(timeframe,vtb,show=False)
            plt.savefig(full_name_img, bbox_inches='tight')
            plt.close()
        
        # Формируем результаты
        result_row = {"name": name_file} | cwt.get_statistics()
        df_results = pd.DataFrame([result_row])
        
        # Сохраняем в Excel
        full_name_doc = os.path.join(xls_folder, name_file + '.xlsx')
        with pd.ExcelWriter(full_name_doc, engine='xlsxwriter') as writer:  
            df_results.to_excel(writer, sheet_name='total')
            
        return name_file, True  # Возвращаем имя файла и статус успеха
    except Exception as e:
        print(e)
        return name_file, str(e)  # Возвращаем имя файла и ошибку

def process_rw(variant_name,variant_folder,clear_df):
    # Ваши параметры
    # Создаем пул процессов (используем все ядра кроме одного)
    num_processes = max(1, phys_cores - save_cores)
    image_folder, xls_folder = create_folder(variant_folder)
    # Подготавливаем функцию с фиксированными аргументами
    worker = partial(process_ws, 
                    variant_name,
                    image_folder,
                    xls_folder,
                    clear_df)
    
    # Запускаем в мультипроцессинге с прогресс-баром
    if variant_name in map_wss:
        wss = map_wss[variant_name]
    else:
        wss = map_wss['default']
    with Pool(num_processes) as pool:
        results = list(tqdm(pool.imap(worker, wss), total=len(wss)))
    success = 0
    for name, status in results:
        if status is True:
            success += 1
        else:
            print(f"Ошибка в {name}: {status}")
    print(f"Успешно обработано: {success}/{len(wss)}")

if __name__ == '__main__':
    for rw in list_dir:
        print(rw)
        start = time()
        raw_file = os.path.join(test_folder,rw)
        sep = '\\' if '\\' in raw_file else '/'
        variant_name = raw_file.split(sep)[-1]
        variant_name = variant_name.split('_')
        variant_name = variant_name[0]+'_'+variant_name[1]
        variant_folder = os.path.join(main_folder,variant_name)
        if not os.path.exists(variant_folder):
            os.makedirs(variant_folder)
        clear_df = simple_load_df(raw_file)
        process_rw(variant_name,variant_folder,clear_df)
        print('Time (m):',round((time()-start)/60,2))
    print('END')

