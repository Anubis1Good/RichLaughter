import os 
import json
import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime,timedelta
from Screening.utils.db_analisys_func import get_best_strategies_v6,get_top5_strategies,get_top5_best_strategies_stable,get_top5_best_day_strategies,get_top5_best_today_strategies,get_top5_stable_by_ncandles,get_top5_best_today_strategies_filtered,get_top5_best_window_strategies_filtered

class Architect:
    def __init__(self,db_path,granularities,hourss):
        self.db_path = db_path
        self.granularities = granularities
        self.hourss = hourss
        self.folder_picks = 'Screening/strat_picks/'
        if not os.path.exists(self.folder_picks):
            os.mkdir(self.folder_picks)


    def get_fix_count_strategies(self,granularity):
        df = get_best_strategies_v6(self.db_path,granularity,10)
        if df is None or df.empty or 'ticker' not in df.columns or 'bot' not in df.columns:
            return {}
        return df.dropna(subset=['ticker', 'bot']).set_index('ticker')['bot'].to_dict()
    
    def get_fix_count_5strategies(self,granularity):
        df = get_top5_strategies(self.db_path,granularity,10)
        if df is None or df.empty or 'ticker' not in df.columns or 'bot' not in df.columns:
            return {}
        # Удаляем строки с пропусками
        df_clean = df.dropna(subset=['ticker', 'bot', 'score'])
        
        # Создаем список кортежей (бот, score) для каждого тикера
        result_dict = (
            df_clean.groupby('ticker')
            .apply(lambda x: list(zip(x['bot'], x['score'])))
            .to_dict()
        )
        return result_dict
    
    def get_fix_count_half_5strategies(self,granularity):
        df = get_top5_strategies(self.db_path,granularity,5)
        if df is None or df.empty or 'ticker' not in df.columns or 'bot' not in df.columns:
            return {}
        # Удаляем строки с пропусками
        df_clean = df.dropna(subset=['ticker', 'bot', 'score'])
    
        
        # Создаем список кортежей (бот, score) для каждого тикера
        result_dict = (
            df_clean.groupby('ticker')
            .apply(lambda x: list(zip(x['bot'], x['score'])))
            .to_dict()
        )
        return result_dict
    
    def get_stable_5strategies(self,granularity,hours):
        df = get_top5_best_strategies_stable(self.db_path,granularity,hours)
        if df is None or df.empty or 'ticker' not in df.columns or 'bot' not in df.columns:
            return {}
        # Удаляем строки с пропусками
        df_clean = df.dropna(subset=['ticker', 'bot', 'score'])
        
        # Создаем список кортежей (бот, score) для каждого тикера
        result_dict = (
            df_clean.groupby('ticker')
            .apply(lambda x: list(zip(x['bot'], x['score'])))
            .to_dict()
        )
        return result_dict
    
    def get_day_5strategies(self,granularity,hour=24):
        df = get_top5_best_day_strategies(self.db_path,granularity,hour)
        if df is None or df.empty or 'ticker' not in df.columns or 'bot' not in df.columns:
            return {}
        # Удаляем строки с пропусками
        df_clean = df.dropna(subset=['ticker', 'bot', 'total_result_fee'])
        
        # Создаем список кортежей (бот, score) для каждого тикера
        result_dict = (
            df_clean.groupby('ticker')
            .apply(lambda x: list(zip(x['bot'], x['total_result_fee'])))
            .to_dict()
        )
        return result_dict
    
    def get_window_5strategies_filter(self,granularity,hour=24):
        df = get_top5_best_window_strategies_filtered(self.db_path,granularity,hour,('PTA19','PTA18','LTA2'))
        if df is None or df.empty or 'ticker' not in df.columns or 'bot' not in df.columns:
            return {}
        # Удаляем строки с пропусками
        df_clean = df.dropna(subset=['ticker', 'bot', 'total_result_fee'])
        
        # Создаем список кортежей (бот, score) для каждого тикера
        result_dict = (
            df_clean.groupby('ticker')
            .apply(lambda x: list(zip(x['bot'], x['total_result_fee'])))
            .to_dict()
        )
        return result_dict
    
    def get_today_5strategies_filter(self,granularity):
        df = get_top5_best_today_strategies_filtered(self.db_path,granularity,('PTA19','PTA18','LTA2'))
        if df is None or df.empty or 'ticker' not in df.columns or 'bot' not in df.columns:
            return {}
        # Удаляем строки с пропусками
        df_clean = df.dropna(subset=['ticker', 'bot', 'total_result_fee'])
        
        # Создаем список кортежей (бот, score) для каждого тикера
        result_dict = (
            df_clean.groupby('ticker')
            .apply(lambda x: list(zip(x['bot'], x['total_result_fee'])))
            .to_dict()
        )
        return result_dict
    
    def get_today_5(self,granularity):
        df = get_top5_best_today_strategies(self.db_path,granularity)
        if df is None or df.empty or 'ticker' not in df.columns or 'bot' not in df.columns:
            return {}
        # Удаляем строки с пропусками
        df_clean = df.dropna(subset=['ticker', 'bot', 'total_result_fee'])
        
        # Создаем список кортежей (бот, score) для каждого тикера
        result_dict = (
            df_clean.groupby('ticker')
            .apply(lambda x: list(zip(x['bot'], x['total_result_fee'])))
            .to_dict()
        )
        return result_dict
    
    def get_ncandels_5(self,granularity,ncandels=100):
        df = get_top5_stable_by_ncandles(self.db_path,granularity,ncandels)
        if df is None or df.empty or 'ticker' not in df.columns or 'bot' not in df.columns:
            return {}
        # Удаляем строки с пропусками
        df_clean = df.dropna(subset=['ticker', 'bot', 'score'])
        # Создаем список кортежей (бот, score) для каждого тикера
        result_dict = (
            df_clean.groupby('ticker')
            .apply(lambda x: list(zip(x['bot'], x['score'])))
            .to_dict()
        )
        return result_dict
    
    def universal_save_file(self,strategies,prefix,granularity):
        filename = f"{prefix}_{granularity}_{self.db_path.split('/')[-1].replace('.db','')}.json"
        try:
            with open(os.path.join(self.folder_picks, filename), 'w') as f:
                json.dump(strategies, f, indent=2)
        except Exception as e:
            print(f"Save error: {e}")

    def save_file(self,ticker_bot_dict,hours,granularity):
        filename = str(hours) + '_' + str(granularity) + '_' + self.db_path.split('/')[-1].replace('.db','') +  '.json'
        filename = os.path.join(self.folder_picks,filename)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(ticker_bot_dict, f, ensure_ascii=False, indent=2)

    def save_file2(self,strategies, granularity):
        filename = f"FC_{granularity}_{self.db_path.split('/')[-1].replace('.db','')}.json"
        try:
            with open(os.path.join(self.folder_picks, filename), 'w') as f:
                json.dump(strategies, f, indent=2)
        except Exception as e:
            print(f"Save error: {e}")

    def save_file3(self,strategies, granularity):
        filename = f"FC5_{granularity}_{self.db_path.split('/')[-1].replace('.db','')}.json"
        try:
            with open(os.path.join(self.folder_picks, filename), 'w') as f:
                json.dump(strategies, f, indent=2)
        except Exception as e:
            print(f"Save error: {e}")


    def open_file3(self,granularity):
        filename = f"FC5_{granularity}_{self.db_path.split('/')[-1].replace('.db','')}.json"
        full_path = os.path.join(self.folder_picks, filename)
        if not os.path.exists(full_path):
            return {}
        try:
            with open(full_path, 'r') as f:
                data = json.load(f)
                return data
        except Exception as e:
            print(f"Save error: {e}")

    def save_file4(self,strategies, granularity):
        filename = f"FC5H_{granularity}_{self.db_path.split('/')[-1].replace('.db','')}.json"
        try:
            with open(os.path.join(self.folder_picks, filename), 'w') as f:
                json.dump(strategies, f, indent=2)
        except Exception as e:
            print(f"Save error: {e}")

    def open_file4(self,granularity):
        filename = f"FC5H_{granularity}_{self.db_path.split('/')[-1].replace('.db','')}.json"
        full_path = os.path.join(self.folder_picks, filename)
        if not os.path.exists(full_path):
            return {"poor": "0_sleep_0"}
        try:
            with open(full_path, 'r') as f:
                data = json.load(f)
                return data
        except Exception as e:
            print(f"Save error: {e}")

    def open_file(self,hours,granularity):
        filename = str(hours) + '_' + str(granularity) + '_' + self.db_path.split('/')[-1].replace('.db','') +  '.json'
        full_path = os.path.join(self.folder_picks, filename)
        if not os.path.exists(full_path):
            return {"poor": "0_sleep_0"}
        try:
            with open(full_path, 'r') as f:
                data = json.load(f)
                return data
        except Exception as e:
            print(f"Save error: {e}")
    
    def universal_open_file(self,prefix,granularity):
        filename = str(prefix) + '_' + str(granularity) + '_' + self.db_path.split('/')[-1].replace('.db','') +  '.json'
        full_path = os.path.join(self.folder_picks, filename)
        if not os.path.exists(full_path):
            return {"poor": "0_sleep_0"}
        try:
            with open(full_path, 'r') as f:
                data = json.load(f)
                return data
        except Exception as e:
            print(f"Save error: {e}")

    
    def check_old_strategies(self,new_strategies,old_strategies):
        final_data = {}
        for ticker in new_strategies:
            new_d = None
            if ticker in old_strategies:
                old_strat = old_strategies[ticker]
                for i in range(len(new_strategies[ticker])):
                    if old_strat in new_strategies[ticker][i]:
                        new_d = new_strategies[ticker][i]
                        break
            best_strat = new_strategies[ticker][0]
            if best_strat[1] < 0:
                continue
            if new_d:
                if best_strat[1] /  (new_d[1]+ 1e-6) < 1.5:
                    best_strat = new_d
            final_data[ticker] = best_strat[0]
        return final_data

    def processing_strategies(self,strategies,prefix,granularity):
        old_strategies = self.universal_open_file(prefix,granularity)
        strategies = self.check_old_strategies(strategies,old_strategies)
        if not strategies:
            strategies = {"poor": "0_sleep_0"}
        self.universal_save_file(strategies,prefix,granularity)

    def run(self):
        for granularity in self.granularities:
            for hours in self.hourss:
                strategies = self.get_stable_5strategies(granularity,hours)
                self.processing_strategies(strategies,hours,granularity)

            strategies = self.get_fix_count_strategies(granularity)
            if not strategies:
                strategies = {"poor": "0_sleep_0"}
            self.save_file2(strategies,granularity)
            self.universal_save_file(strategies,'FC',granularity)

            strategies = self.get_fix_count_5strategies(granularity)
            self.processing_strategies(strategies,'FC5',granularity)

            strategies = self.get_fix_count_half_5strategies(granularity)
            self.processing_strategies(strategies,'FC5H',granularity)

            strategies = self.get_today_5strategies_filter(granularity)
            self.processing_strategies(strategies,'BTDF',granularity)

            strategies = self.get_day_5strategies(granularity)
            self.processing_strategies(strategies,'B24',granularity)

            strategies = self.get_day_5strategies(granularity,100)
            self.processing_strategies(strategies,'B100',granularity)

            strategies = self.get_window_5strategies_filter(granularity)
            self.processing_strategies(strategies,'BF24',granularity)

            strategies = self.get_window_5strategies_filter(granularity,100)
            self.processing_strategies(strategies,'BF100',granularity)

            strategies = self.get_today_5(granularity)
            self.processing_strategies(strategies,'BTD',granularity)

            strategies = self.get_ncandels_5(granularity)
            self.processing_strategies(strategies,'C100',granularity)

            strategies = self.get_ncandels_5(granularity,500)
            self.processing_strategies(strategies,'C500',granularity)


