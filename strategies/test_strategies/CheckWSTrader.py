import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from time import time
from strategies.work_strategies.BaseTA import BaseTABitget
from utils.processing_results.add_vtb_fee_fut import get_func_vtb_fee
from utils.work_with_dataframe.convert_timeframe import convert_timeframe
from utils.work_with_dataframe.help_child_test import convert_datetime_CT,get_child_candles
from utils.draw_utils import draw_hb_chart_fast

def duration_time(func):
    def wrapper(self, *args, **kwargs):
        if self.measure_time:
            start = time()
            print('start', func.__name__)
            result = func(self, *args, **kwargs)
            print('Time:', time() - start)
        else:
            result = func(self, *args, **kwargs)
        return result
    return wrapper

#добавить учет риск-менеджмента
class CheckWSTrader:
    def __init__(self,
                 df:pd.DataFrame | str, 
                 ws:list|tuple|BaseTABitget,
                 fee:float = 0.0002,
                 symbol:str = 'TS',
                 tf:str = '5m',
                 close_on_time:bool=False,
                 close_map:tuple|list=(
                     (23,30),(23,30),(23,30),(23,30),(23,30),(17,50),(17,50),),
                 measure_time:bool=False,
                 use_tqdm:bool=False,
                 stop_risk:int|float|None = None
                 ):
        self.symbol = symbol
        self.tf = tf
        self.reload_data()
        if isinstance(df,str):
            path_df = df
            self.df = self.read_df(path_df)
        else:
            self.df = df.copy()
        if isinstance(ws,tuple) or isinstance(ws,list):
            self.ws = ws[0](self.symbol,self.tf,'e',1,*ws[1])
        else:
            self.ws = ws
        self.fee = fee
        self.fee_one_p = fee  * 100
        self.close_on_time = close_on_time
        self.close_map = close_map
        self.vtb_fee_func = get_func_vtb_fee(symbol)
        self.actions = (None,'long_pw','short_pw','close_long_pw','close_short_pw','close_all_pw')
        self.actions_dict = {action: idx for idx, action in enumerate(self.actions)}
        self.measure_time = measure_time
        self.use_tqdm = use_tqdm
        self.df = self.add_time_features(self.df)
        self.stop_risk = -stop_risk if stop_risk is not None else False

    def reload_data(self):
        self.trade_data = {
            'total':0,
            'count':0, #количество разворотов
            'fees': 0, #комиссия в абсолютных
            'total_wfees_per':0, #прибыль в процентах с учетом комиссии
            'equity':[0], #динамика дохода
            'equity_fee':[0], #динамика дохода с комиссией
            'step_eq_fee':[0], #equity каждый шаг
            'unclosed_fee':[0], #equity незакрытый каждый шаг
            'step_eq_vtb':[0], #equity каждый шаг
            'unclosed_vtb':[0], #equity незакрытый каждый шаг
            'pos':0, #текущая позиция
            'hist_pos':[0],
            'open_price':0, #текущая цена
            'o_longs':[], #входы в лонг
            'o_shorts':[], #входы в шорт
            'c_longs':[], #закрытие лонгов
            'c_shorts':[], #закрытие шортов 
            'c_risks':[], #закрытие по риск менеджменту
        }
        self.open_fee = 0
        self.cur_wday = None
        self.cur_eq = None
        self.first_risk = True
        self.last_c_risk = None
    
    def read_df(self,path_df):
        if path_df.endswith('.parquet'):
            self.df = pd.read_parquet(path_df)
        else:
            self.df = pd.read_csv(path_df)

    def get_iterator(self,data):
        if self.use_tqdm:
            return tqdm(data)
        return data
    
    def open_pos(self,price,feei):
        self.trade_data['open_price']= price
        self.trade_data['fees'] += feei
        self.open_fee = feei
        self.trade_data['total_wfees_per'] -= self.fee_one_p # комиссия за открытие
    
    def open_long(self,price,feei,row_name):
        self.open_pos(price,feei)
        self.trade_data['o_longs'].append((row_name,price))
        self.trade_data['pos'] = 1
        self.trade_data['count'] += 1

    def open_short(self,price,feei,row_name):
        self.open_pos(price,feei)
        self.trade_data['o_shorts'].append((row_name,price))
        self.trade_data['pos'] = -1
        self.trade_data['count'] += 1

    def close_pos(self,price,feei,delta):
        self.trade_data['total'] += delta
        self.trade_data['total_wfees_per'] += ((delta  / price) * 100) - self.fee_one_p  # комиссия за закрытие
        self.trade_data['fees'] += feei
        self.trade_data['equity'].append(self.trade_data['equity'][-1] + delta)
        self.trade_data['equity_fee'].append(self.trade_data['equity_fee'][-1] + delta - feei - self.open_fee)
        self.open_fee = 0

    def close_long(self,price,feei,row_name):
        delta = price - self.trade_data['open_price']  # прибыль по лонгу (как при action=3)
        self.close_pos(price,feei,delta)
        self.trade_data['c_longs'].append((row_name,price))
        self.trade_data['pos'] = 0
    
    def close_short(self,price,feei,row_name):
        delta = self.trade_data['open_price'] - price  # прибыль по шорту (как при action=4)
        self.close_pos(price,feei,delta)
        self.trade_data['c_shorts'].append((row_name,price))
        self.trade_data['pos'] = 0

    def work_action(self,signal, price, row_name):
        """return pos,open_price,fees,open_fee"""
        # actions = (None,'long_pw','short_pw','close_long_pw','close_short_pw','close_all_pw')
        feei = self.fee * price  # fee абсолютное значение
        # print(feei)
        if signal == 1:  # long
            if self.trade_data['pos'] != 1:
                if self.trade_data['pos'] < 0: # был шорт, закрываем его и открываем лонг
                    self.close_short(price,feei,row_name)
                self.open_long(price,feei,row_name)
        elif signal == 2:  # short
            if self.trade_data['pos'] != -1:
                if self.trade_data['pos'] > 0:
                    self.close_long(price,feei,row_name)
                self.open_short(price,feei,row_name)  
        elif signal == 3:  # close long
            if self.trade_data['pos'] == 1:
                self.close_long(price,feei,row_name)
        elif signal == 4:  # close short
            if self.trade_data['pos'] == -1:
                self.close_short(price,feei,row_name)
        elif signal == 5:
            if self.trade_data['pos'] == 1:
                self.close_long(price,feei,row_name)
            elif self.trade_data['pos'] == -1:
                self.close_short(price,feei,row_name)

    def add_time_features(self,df):
        df = df.copy()
        df['ms'] = pd.to_datetime(df['ms'], format='%Y-%m-%d %H:%M:%S')
        df['hour'] = df['ms'].dt.hour
        df['minute'] = df['ms'].dt.minute
        df['weekday'] = df['ms'].dt.weekday
        return df

    def update_step_data(self,price):
        self.trade_data['step_eq_fee'].append(self.trade_data['equity_fee'][-1])
        self.trade_data['step_eq_vtb'].append(self.vtb_fee_func(self.trade_data['equity'][-1],1))
        self.trade_data['hist_pos'].append(self.trade_data['pos'])
        if self.trade_data['pos'] > 0:
            unclosed_profit = price - self.trade_data['open_price']
        elif self.trade_data['pos'] < 0:
            unclosed_profit = self.trade_data['open_price'] - price
        else:
            unclosed_profit = 0
        self.trade_data['unclosed_fee'].append(self.trade_data['step_eq_fee'][-1] + unclosed_profit)
        self.trade_data['unclosed_vtb'].append(self.trade_data['step_eq_vtb'][-1] + self.vtb_fee_func(unclosed_profit,0))

    def check_risk(self,weekday,row_name,price,vtb=True):
        if self.stop_risk:
            eq = self.trade_data['unclosed_vtb'][-1] if vtb else self.trade_data['unclosed_fee'][-1]
            if self.cur_wday != weekday:
                self.cur_wday = weekday
                self.cur_eq = eq
                if not self.first_risk:
                    self.trade_data['c_risks'][-1] += self.last_c_risk
                    self.last_c_risk = None
                    self.first_risk = True
            else:
                if self.first_risk:
                    delta = eq - self.cur_eq
                    if delta < self.stop_risk:
                        self.first_risk = False
                        self.trade_data['c_risks'].append([row_name,price])
                        self.last_c_risk = [row_name,price]
                        return False
                else:
                    self.last_c_risk = [row_name,price]
                    return False
        return True
        
    # CHECKS_FUNCS
    @duration_time
    def check_strategy_window(self,window=150, normalization=False,vtb=True):
        """
        оконная версия
        """
        self.reload_data()
        price = None
        for i in self.get_iterator(range(len(self.df))):
            if i > window:
                df_slice = self.df.iloc[i-window:i].copy()
                row = df_slice.iloc[-1]
                price = row['close']
                row_name = row['x']
                
                if normalization:
                    candel_max = df_slice['high'].max()
                    df_norm = df_slice.copy()
                    df_norm['volume'] = df_norm['volume'] / df_norm['volume'].max()
                    df_norm['close'] = df_norm['close'] / candel_max
                    df_norm['open'] = df_norm['open'] / candel_max
                    df_norm['low'] = df_norm['low'] / candel_max
                    df_norm['high'] = df_norm['high'] / candel_max
                    row = self.ws.get_test_row(df_norm)
                else:
                    row = self.ws.get_test_row(df_slice)
                action = self.ws(row)
                if self.close_on_time:
                    time_close = self.close_map[row['weekday']]
                    if row['hour'] >= time_close[0] and row['minute'] >= time_close[1]:
                        action = 'close_all_pw'
                action = action if self.check_risk(row['weekday'],row_name,price,vtb) else 'close_all_pw'
                signal = self.actions_dict.get(action, None)
                self.work_action(signal, price, row_name)
            self.update_step_data(price)
    
    @duration_time
    def check_strategy_child(self,timeframe='5min',window=150, normalization=False,vtb=True):
        df = self.df.copy()
        self.reload_data()
        price = None
        df['ms'] = convert_datetime_CT(df['ms'])
        df_big = convert_timeframe(df,timeframe)
        df_big = self.add_time_features(df_big)
        for i in self.get_iterator(range(len(df_big.index))):
            if i > window:
                lc = df_big.iloc[i-1]
                start_time = lc['ms']
                end_time = start_time + pd.Timedelta(minutes=5)
                df_child = df[(df['ms'] >= start_time)&(df['ms'] < end_time)]
                child_candles = get_child_candles(df_child,lc['x'])
                df_slice = df_big.iloc[i-window:i].copy()
                row = df_slice.iloc[-1]
                row_name = row['x']
                for sc in child_candles:
                    df_slice.iloc[-1] = sc
                    df_temp = df_slice.copy()
                    price = sc['close']
                    if normalization:
                        candel_max = df_temp['high'].max()
                        df_norm = df_temp.copy()
                        df_norm['volume'] = df_norm['volume'] / df_norm['volume'].max()
                        df_norm['close'] = df_norm['close'] / candel_max
                        df_norm['open'] = df_norm['open'] / candel_max
                        df_norm['low'] = df_norm['low'] / candel_max
                        df_norm['high'] = df_norm['high'] / candel_max
                        row = self.ws.get_test_row(df_norm)
                    else:
                        row = self.ws.get_test_row(df_slice)
                    action = self.ws(row)
                    if self.close_on_time:
                        time_close = self.close_map[row['weekday']]
                        if row['hour'] >= time_close[0] and row['minute'] >= time_close[1]:
                            action = 'close_all_pw'
                    action = action if self.check_risk(row['weekday'],row_name,price,vtb) else 'close_all_pw'
                    signal = self.actions_dict.get(action, None)
                    self.work_action(signal, price, row_name)
            self.update_step_data(price)

    # POST_PROCESS_RESULT_FUNCS
    def process_old_type_result(self):
        df_eq = pd.DataFrame({'eq':self.trade_data['equity'],'eq_fee':self.trade_data['equity_fee']})
        trades = {'total': self.trade_data['total'], 'count': self.trade_data['count'], 'total_fee_per': self.trade_data['total_wfees_per']}
        if df_eq.empty:
            trades.update({
            'total_abs_fee': 0,
            'win_rate_wf': 0,
            'total_fee': self.trade_data['fees'],
            'mean_eq':0,
            'median_eq':0,
            'max_eq':0,
            'min_eq':0,
            'balance_eq':0,
            'mean_eqf':0,
            'median_eqf':0,
            'max_eqf':0,
            'min_eqf':0,
            'balance_eqf':0
            })
        else:
            df_eq['diff_eq'] = df_eq['eq'].diff()
            df_eq['diff_eq_fee'] = df_eq['eq_fee'].diff()
            mean_eq = df_eq['diff_eq'].mean()
            median_eq = df_eq['diff_eq'].median()
            min_eq = df_eq['diff_eq'].min()
            max_eq = df_eq['diff_eq'].max()
            mean_eqf = df_eq['diff_eq_fee'].mean()
            median_eqf = df_eq['diff_eq_fee'].median()
            min_eqf = df_eq['diff_eq_fee'].min()
            max_eqf = df_eq['diff_eq_fee'].max()
            wins = len(df_eq[df_eq['diff_eq'] > 0].index)
            loss = len(df_eq[df_eq['diff_eq'] < 0].index)
            if loss > 0:
                win_rate = round((wins / (wins + loss)) * 100,2)
            else:
                win_rate = 0

            trades['total_fee_per'] = round(self.trade_data['total_wfees_per'],2)
            trades.update({
                'total_abs_fee': self.trade_data['equity_fee'][-1],
                'win_rate_wf': win_rate,
                'total_fee': self.trade_data['fees'],
                'mean_eq':mean_eq,
                'median_eq':median_eq,
                'max_eq':max_eq,
                'min_eq':min_eq,
                'balance_eq':max_eq+min_eq,
                'mean_eqf':mean_eqf,
                'median_eqf':median_eqf,
                'max_eqf':max_eqf,
                'min_eqf':min_eqf,
                'balance_eqf':max_eqf+min_eqf
            })
        longs = np.array(self.trade_data['o_longs'])
        shorts = np.array(self.trade_data['o_shorts'])
        closes = np.array(self.trade_data['c_longs'] + self.trade_data['c_shorts'])
        equity = np.array(self.trade_data['equity'])
        equity_fee = np.array(self.trade_data['equity_fee'])
        return trades,equity,equity_fee,longs,shorts,closes

    def print_statistics(self,vtb=True):
        """Печать статистики по торгам"""
        td = self.trade_data
        print(f"\n=== СТАТИСТИКА ДЛЯ {self.symbol} ===")
        print(f"Прибыль ABC без комисии: {td['equity'][-1]:.2f}")
        if vtb:
            print(f"Прибыль ВТБ: {td['step_eq_vtb'][-1]}")
            print(f"Комиссия ВТБ: {td['count']*2}")
            type_unclosed = 'unclosed_vtb'
        else:
            type_unclosed = 'unclosed_fee'
            print(f"Прибыль ABC c комиссией: {td['equity_fee'][-1]:.2f}")
            print(f"Комисии: {td['fees']:.2f}")
            print(f"Прибыль PER c комиссией: {td['total_wfees_per']:.2f}")
        print(f"Всего сделок: {td['count']}")
        print(f"Максимальная прибыль: {max(td[type_unclosed]):.2f}")
        print(f"Максимальная просадка: {min(td[type_unclosed]):.2f}")
        print(f"Открыто лонгов: {len(td['o_longs'])}")
        print(f"Открыто шортов: {len(td['o_shorts'])}")
        print(f"Превышений просадок: {len(td['c_risks'])}")

    def plot_transaction(self):
        td = self.trade_data
        td['o_longs'] = np.array(td['o_longs'])
        td['o_shorts'] = np.array(td['o_shorts'])
        td['c_longs'] = np.array(td['c_longs'])
        td['c_shorts'] = np.array(td['c_shorts'])
        td['c_risks'] = np.array(td['c_risks'])
        if len(td['o_longs'].shape) > 1:
            plt.scatter(td['o_longs'][:,0],td['o_longs'][:,1],marker='^',color='blue')
        if len(td['o_shorts'].shape) > 1:
            plt.scatter(td['o_shorts'][:,0],td['o_shorts'][:,1],marker='v',color='black')
        if len(td['c_longs'].shape) > 1:
            plt.scatter(td['c_longs'][:,0],td['c_longs'][:,1],marker='x',color='blue')
        if len(td['c_shorts'].shape) > 1:
            plt.scatter(td['c_shorts'][:,0],td['c_shorts'][:,1],marker='x',color='black')
        if len(td['c_risks'].shape) > 1:
            x_starts = td['c_risks'][:,0]
            y_starts = td['c_risks'][:,1]
            x_ends = td['c_risks'][:,2]
            y_ends = td['c_risks'][:,3]

            # Создаём массивы для plot (чередуем start-end)
            x_lines = np.empty((len(td['c_risks']) * 3,))
            y_lines = np.empty((len(td['c_risks']) * 3,))
            x_lines[0::3] = x_starts
            x_lines[1::3] = x_ends
            x_lines[2::3] = np.nan
            y_lines[0::3] = y_starts
            y_lines[1::3] = y_ends
            y_lines[2::3] = np.nan

            plt.plot(x_lines, y_lines, color='black')
    
    def plot_equity(self,show=True):
        plt.plot(self.trade_data['equity'],color='r')
        plt.plot(self.trade_data['equity_fee'],color='b')
        if show:
            plt.show()
    
    def plot_chart(self,convert_tf=None,show=True):
        chart = self.df.copy()
        if convert_tf:
            chart = convert_timeframe(chart,convert_tf)
        td = self.trade_data
        draw_hb_chart_fast(chart)
        self.plot_transaction()
        if show:
            plt.show()
    
    def plot_chart_and_sequtity(self,convert_tf=None,vtb=True,help_info='complex',show=True):
        """Создаем фигуру с двумя subplot'ами
            Варианты:
            'step_equity'
            'pos'
            'complex'
        """
        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)  # sharex=True для синхронизации по оси X
        
        # Первый график
        plt.sca(ax1)
        self.plot_chart(convert_tf, show=False)
        
        # Второй график
        plt.sca(ax2)
        if help_info == 'step_equity':
            sequity = self.trade_data['step_eq_vtb'] if vtb else self.trade_data['step_eq_fee']
        elif help_info == 'pos':
            sequity = self.trade_data['hist_pos']
        elif help_info == 'unclosed':
            sequity = self.trade_data['unclosed_vtb'] if vtb else self.trade_data['unclosed_fee']
        elif help_info == 'complex':
            sequity = self.trade_data['unclosed_vtb'] if vtb else self.trade_data['unclosed_fee']
            ax2.plot(sequity)
            sequity = self.trade_data['step_eq_vtb'] if vtb else self.trade_data['step_eq_fee']
        else:
            sequity = np.array([])
        ax2.plot(sequity)
            
        
        # Добавляем подписи для удобства
        ax1.set_title(f'Chart for {self.symbol}')
        ax2.set_title('Sequity')
        ax2.set_xlabel('Time')
        
        # Автоматическая регулировка layout'а
        plt.tight_layout()
        if show:
            plt.show()   