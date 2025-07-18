import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import psutil
from time import time 
from tqdm import tqdm
from multiprocessing import Pool
from functools import partial
from strategies.test_strategies.check import check_strategy_v5
from Loader.BitgetLoader import bitget_loader
# from strategies.work_strategies.PTA import PTA4_WDDCr,PTA4_WDDCrE,PTA4_WDDCrVG,PTA4_WDVCr,PTA4_WLISICA,PTA8_WDOBBY_FREEr,PTA4_UNIVERSAL,PTA2_LISICA,PTA2_DDCrWork,PTA2_BDDCr_UNIVERSAL,PTA2_BDDC_FIX,PTA2_BVGFIX,PTA2_BBBU,PTA2_BBBUr,PTA2_DDCrVG,PTA2_DVCr,PTA2_VOLCHARA,PTA4_U3
# from Traders.TestingTrader.wss_groups import wssMoexFut5 as wss
from testing.wss_step_test import wss_br,wss_cny,wss_ed,wss_euf,wss_ng,wss_si,wss_sr
phys_cores = psutil.cpu_count(logical=False) 

main_folder = 'TestNewResults/StepTest'
if not os.path.exists(main_folder):
    os.makedirs(main_folder)
save_cores = 2
fee = 0.0002
close_2330 = True
need_plot = True
# test_folder = 'DataForTests\DataFromMoexFast'
test_folder = 'DataForTests\DataFromMoexForStepTests'
list_dir = os.listdir(test_folder)
# wss = (
#     (PTA2_LISICA,(10,1)), 
#     (PTA2_DDCrWork,(20,)),
# )
map_wss = {
    '5BRQ5_1':wss_br,
    '5CNYRUBF_1':wss_cny,
    '5EDU5_1':wss_ed,
    '5EURRUBF_1':wss_euf,
    '5NGN5_1':wss_ng,
    '5SiU5_1':wss_si,
    '5SRU5_1':wss_sr,
    'default':wss_cny
}

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
        trades, equity, equity_fee = check_strategy_v5(clear_df.copy(), strategy, fee, close_2330)
        
        # Сохраняем график если нужно
        if need_plot:
            full_name_img = os.path.join(image_folder, f"{name_file}.png")
            plt.figure(figsize=(12, 6))
            plt.plot(equity, color='red', label='Equity')
            plt.plot(equity_fee, color='blue', label='Equity with Fees')
            plt.title(f"{name_bot}")
            plt.legend()
            plt.savefig(full_name_img, bbox_inches='tight')
            plt.close()
        
        # Формируем результаты
        result_row = {"name": name_file} | trades
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
        clear_df = bitget_loader(raw_file)
        process_rw(variant_name,variant_folder,clear_df)
        print('Time (m):',round((time()-start)/60,2))
    print('END')
    # for ws in tqdm(wss):
    #     image_folder,xls_folder = create_folder(variant_folder)
    #     name_bot = str(ws[0].__name__)
    #     name_file = f"{name_bot}_{'_'.join(map(str, ws[1]))}"
    #     strategy = ws[0](variant_name,'5',"1",1,*ws[1])
    #     trades,equity,equity_fee = check_strategy_v5(clear_df.copy(),strategy,fee,close_2330)
    #     if need_plot:
    #         full_name_img = os.path.join(image_folder, f"{name_file}.png")
    #         plt.figure(figsize=(12, 6))
    #         plt.plot(equity, color='red', label='Equity')
    #         plt.plot(equity_fee, color='blue', label='Equity with Fees')
    #         plt.title(f"{name_bot}")
    #         plt.legend()
    #         plt.savefig(full_name_img, bbox_inches='tight')
    #         plt.close()
    #     result_row = {"name": name_file}
    #     result_row = result_row | trades
    #     df_results = pd.DataFrame([result_row])
    #     full_name_doc = os.path.join(xls_folder, name_file + '.xlsx')
    #     with pd.ExcelWriter(full_name_doc, engine='xlsxwriter') as writer:  
    #         df_results.to_excel(writer, sheet_name='total')
