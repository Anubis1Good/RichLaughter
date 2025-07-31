import pandas as pd
import numpy as np
from tqdm import tqdm
from utils.work_with_dataframe.convert_timeframe import convert_timeframe
# from numba import jit  # Ускорение вычислений (опционально)
def check_strategy(df,test_strategy,work_strategy):
    """
    trades,longs,shorts,closes,equity
    """
    trades = {
        'pos':0,
        'open_price':0,
        'total':0,
        'count':0
    }
    longs = []
    shorts = []
    closes = []
    equity = []
    df.apply(lambda row: test_strategy(row,trades,shorts,longs,closes,equity,work_strategy),axis=1)
    return trades,longs,shorts,closes,equity
#No use
def work_action(action,trades,cur_price,fee,fees,equity,equity_fee,pos,open_price):
    """actions = (None,'long_pw','short_pw','close_long_pw','close_short_pw','close_all_pw')"""
    reward = 0
    feei = fee * cur_price  # fee абсолютное значение
    if action == 1:  # long
        if pos != 1:
            if pos == 0:
                open_price = cur_price
                reward = -fee * 100  # комиссия за открытие
                fees += feei
                equity_fee.append(equity_fee[-1] - feei)
            else:  # был шорт, закрываем его и открываем лонг
                delta = open_price - cur_price  # прибыль по шорту (как при action=4)
                trades['total'] += delta
                reward = ((delta - fee * 2) / cur_price) * 100   # комиссия за закрытие + открытие
                open_price = cur_price  # новая цена для лонга
                fees += feei * 2
                equity.append(equity[-1] + delta)
                equity_fee.append(equity_fee[-1] + delta - feei * 2)
            pos = 1
            trades['count'] += 1

    elif action == 2:  # short
        if pos != -1:
            if pos == 0:
                open_price = cur_price
                reward = -fee * 100  # комиссия за открытие
                fees += feei
                equity_fee.append(equity_fee[-1] - feei)
            else:  # был лонг, закрываем его и открываем шорт
                delta = cur_price - open_price  # прибыль по лонгу (как при action=3)
                trades['total'] += delta
                reward = ((delta - fee * 2) / cur_price) * 100  # комиссия за закрытие + открытие
                open_price = cur_price  # новая цена для шорта
                fees += feei * 2
                equity.append(equity[-1] + delta)
                equity_fee.append(equity_fee[-1] + delta - feei * 2)
            pos = -1
            trades['count'] += 1

    elif action == 3:  # close long
        if pos == 1:
            delta = cur_price - open_price
            trades['total'] += delta
            reward = ((delta - fee) / cur_price) * 100 
            pos = 0
            fees += feei
            equity.append(equity[-1] + delta)
            equity_fee.append(equity_fee[-1] + delta - feei)

    elif action == 4:  # close short
        if pos == -1:
            delta = open_price - cur_price
            trades['total'] += delta
            reward = ((delta - fee) / cur_price) * 100 
            pos = 0
            fees += feei
            equity.append(equity[-1] + delta)
            equity_fee.append(equity_fee[-1] + delta - feei)
    elif action == 5:
        if pos == 1:
            delta = cur_price - open_price
            trades['total'] += delta
            reward = ((delta - fee) / cur_price) * 100 
            pos = 0
            fees += feei
            equity.append(equity[-1] + delta)
            equity_fee.append(equity_fee[-1] + delta - feei)
        elif pos == -1:
            delta = open_price - cur_price
            trades['total'] += delta
            reward = ((delta - fee) / cur_price) * 100 
            pos = 0
            fees += feei
            equity.append(equity[-1] + delta)
            equity_fee.append(equity_fee[-1] + delta - feei)
        
    trades['total_fee_per'] += reward
    return pos,open_price,fees

actions = (None,'long_pw','short_pw','close_long_pw','close_short_pw','close_all_pw')
actions_array = np.array(actions, dtype=object)

def check_strategy_v2(df:pd.DataFrame,work_strategy,fee=0.0002):
    """
    trades,equity,equity_fee
    """
    trades = {
        'total':0,
        'count':0,
        'total_fee_per':0
    }
    pos = 0
    open_price = 0
    equity = [0]
    equity_fee = [0]
    fees = 0
    signals = df.apply(work_strategy,axis=1).values
    prices = df['close'].values
    # Преобразуем actions в массив NumPy
    # Получаем индексы через np.where (None автоматически даст 0)
    signals = np.where(signals[:, None] == actions_array)[1]
    for i in range(signals.shape[0]):
        cur_price = prices[i]
        pos, open_price, fees = work_action(signals[i],trades,cur_price,fee,fees,equity,equity_fee,pos,open_price)


    trades['total_min_fee'] = trades['total'] - fees
    trades['total_average_fee'] = trades['total'] - fees*2
    trades['total_max_fee'] = trades['total'] - fees*3
    trades['open_price'] = cur_price
    return trades,equity,equity_fee


class TradeTracker:
    def __init__(self):
        self.pos = 0
        self.open_price = 0
        self.total = 0
        self.count = 0


def check_strategy_fast(df:pd.DataFrame, test_strategy, work_strategy):
    """
    Быстрая функция для проверки стратегии.
    """
    trades = {
        'pos':0,
        'open_price':0,
        'total':0,
        'count':0,
        'signal':None
    }
    # Векторизованная обработка данных
    df.apply(lambda row: test_strategy(row,trades,work_strategy),axis=1)
    row = df.iloc[-1]
    if trades['pos'] == 1:
        trades['pos'] = 0
        trades['total'] += row['close'] - trades['open_price']
        trades['count'] += 1  
    if trades['pos'] == -1:
        trades['pos'] = 0
        trades['total'] += trades['open_price'] - row['close']
        trades['count'] += 1 
    trades['open_price'] = df['middle'].median()
    return trades


# Ускоренная версия work_action (если нужно)
# @jit(nopython=True)
def work_action_v2(action, trades, cur_price, fee, fees, equity, equity_fee, pos, open_price,open_fee):
    """return pos,open_price,fees,open_fee"""
    """actions = (None,'long_pw','short_pw','close_long_pw','close_short_pw','close_all_pw')"""
    reward = 0
    delta = 0
    feei = (fee * cur_price) / 100  # fee абсолютное значение
    # print(feei)
    if action == 1:  # long
        if pos != 1:
            if pos == 0:
                open_price = cur_price
                reward = -fee  # комиссия за открытие
                fees += feei
                # equity_fee.append(equity_fee[-1] - feei)
                open_fee = feei
            else:  # был шорт, закрываем его и открываем лонг
                delta = open_price - cur_price  # прибыль по шорту (как при action=4)
                trades['total'] += delta
                reward = ((delta  / cur_price) * 100) - fee*2   # комиссия за закрытие + открытие
                open_price = cur_price  # новая цена для лонга
                fees += feei * 2
                equity.append(equity[-1] + delta)
                equity_fee.append(equity_fee[-1] + delta - feei * 2 - open_fee)
                open_fee = 0
            pos = 1
            trades['count'] += 1

    elif action == 2:  # short
        if pos != -1:
            if pos == 0:
                open_price = cur_price
                reward = -fee  # комиссия за открытие
                fees += feei
                open_fee = feei
                # equity_fee.append(equity_fee[-1] - feei)
            else:  # был лонг, закрываем его и открываем шорт
                delta = cur_price - open_price  # прибыль по лонгу (как при action=3)
                trades['total'] += delta
                reward = ((delta  / cur_price) * 100) - fee*2  # комиссия за закрытие + открытие
                open_price = cur_price  # новая цена для шорта
                fees += feei * 2
                equity.append(equity[-1] + delta)
                equity_fee.append(equity_fee[-1] + delta - feei * 2 - open_fee)
                open_fee = 0
            pos = -1
            trades['count'] += 1

    elif action == 3:  # close long
        if pos == 1:
            delta = cur_price - open_price
            trades['total'] += delta
            reward = ((delta  / cur_price) * 100) - fee 
            pos = 0
            fees += feei
            equity.append(equity[-1] + delta)
            equity_fee.append(equity_fee[-1] + delta - feei - open_fee)
            open_fee = 0

    elif action == 4:  # close short
        if pos == -1:
            delta = open_price - cur_price
            trades['total'] += delta
            reward = ((delta  / cur_price) * 100) - fee 
            pos = 0
            fees += feei
            equity.append(equity[-1] + delta)
            equity_fee.append(equity_fee[-1] + delta - feei - open_fee)
            open_fee = 0
    elif action == 5:
        if pos == 1:
            delta = cur_price - open_price
            trades['total'] += delta
            reward = ((delta  / cur_price) * 100) - fee
            pos = 0
            fees += feei
            equity.append(equity[-1] + delta)
            equity_fee.append(equity_fee[-1] + delta - feei - open_fee)
            open_fee = 0
        elif pos == -1:
            delta = open_price - cur_price
            trades['total'] += delta
            reward = ((delta  / cur_price) * 100) - fee
            pos = 0
            fees += feei
            equity.append(equity[-1] + delta)
            equity_fee.append(equity_fee[-1] + delta - feei - open_fee)
            open_fee = 0
    trades['total_fee_per'] += reward
    return pos,open_price,fees,open_fee

def check_strategy_v3(df: pd.DataFrame, work_strategy, fee=0.0002,close_2330=False):
    """
    return trades,equity,equity_fee
    Улучшенная версия:
    - Поддержка векторных операций.
    """
    trades = {'total': 0, 'count': 0, 'total_fee_per': 0}
    pos = 0
    open_price = 0
    equity = [0]
    equity_fee = [0]
    fees = 0
    # Получаем сигналы
    # signals = df.apply(work_strategy, axis=1).values
    df['action'] = df.apply(work_strategy, axis=1)
    if close_2330:
        df['ms'] = pd.to_datetime(df['ms'], format='%Y-%m-%d %H:%M:%S')
        df['action'] = np.where((df['ms'].dt.hour == 23)&(df['ms'].dt.minute > 25),'close_all_pw',df['action'])
    signals = df['action'].values
    signals = np.where(signals[:, None] == actions_array)[1]  # Ваш метод конвертации в индексы
    
    prices = df['close'].values
    fee_one_p = (fee / 2) * 100
    open_fee = 0
    # from collections import defaultdict
    # debug = defaultdict(list)
    for i in range(len(signals)):
        pos, open_price, fees, open_fee = work_action_v2(
            signals[i], trades, prices[i], fee_one_p, fees, equity, equity_fee, pos, open_price,open_fee
        )
    # with open('debug.json','w') as f:
    #     import json
    #     json.dump(debug,f)
    df_eq = pd.DataFrame({'eq':equity,'eq_fee':equity_fee})
    if df_eq.empty:
        trades.update({
        'total_abs_fee': 0,
        'win_rate_wf': 0,
        'total_fee': fees,
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

        trades['total_fee_per'] = round(trades['total_fee_per'],2)
        trades.update({
            'total_abs_fee': equity_fee[-1],
            'win_rate_wf': win_rate,
            'total_fee': fees,
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
    
    return trades,equity,equity_fee

def check_strategy_v3_LSC(df: pd.DataFrame, work_strategy, fee=0.0002,close_2330=False):
    """
    return trades,equity,equity_fee,longs,shorts,closes
    Улучшенная версия:
    - Поддержка векторных операций.
    """
    trades = {'total': 0, 'count': 0, 'total_fee_per': 0}
    pos = 0
    open_price = 0
    equity = [0]
    equity_fee = [0]
    fees = 0
    # Получаем сигналы
    # signals = df.apply(work_strategy, axis=1).values
    df['action'] = df.apply(work_strategy, axis=1)
    if close_2330:
        df['ms'] = pd.to_datetime(df['ms'], format='%Y-%m-%d %H:%M:%S')
        df['action'] = np.where((df['ms'].dt.hour == 23)&(df['ms'].dt.minute > 25),'close_all_pw',df['action'])
    signals = df['action'].values
    signals = np.where(signals[:, None] == actions_array)[1]  # Ваш метод конвертации в индексы
    row_names = df.index.to_series().values
    longs = []
    shorts = []
    closes = []
    prices = df['close'].values
    fee_one_p = (fee / 2) * 100
    open_fee = 0
    # from collections import defaultdict
    # debug = defaultdict(list)
    for i in range(len(signals)):
        pos, open_price, fees, open_fee = work_action_v3_CA(
            signals[i], trades, prices[i], fee_one_p, fees, equity, equity_fee, pos, open_price,open_fee,row_names[i],longs,shorts,closes
        )
    # with open('debug.json','w') as f:
    #     import json
    #     json.dump(debug,f)
    df_eq = pd.DataFrame({'eq':equity,'eq_fee':equity_fee})
    if df_eq.empty:
        trades.update({
        'total_abs_fee': 0,
        'win_rate_wf': 0,
        'total_fee': fees,
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

        trades['total_fee_per'] = round(trades['total_fee_per'],2)
        trades.update({
            'total_abs_fee': equity_fee[-1],
            'win_rate_wf': win_rate,
            'total_fee': fees,
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
    longs = np.array(longs)
    shorts = np.array(shorts)
    closes = np.array(closes)
    equity = np.array(equity)
    equity_fee = np.array(equity_fee)
    return trades,equity,equity_fee,longs,shorts,closes

def get_step_candles(lc):
    candles = []
    volume = lc['volume'] / 5
    candel = lc.copy()
    candel['close'] = candel['open']
    candel['high'] = candel['open']
    candel['low'] = candel['open']
    candel['middle'] = candel['open']
    candles.append(candel)
    candel = candel.copy()
    if lc['direction'] == 1:
        candel['close'] = lc['low']
        candel['low'] = lc['low']
        candel['middle'] = (candel['high'] + candel['low']) / 2
        candles.append(candel)
        candel = candel.copy()
        candel['close'] = lc['middle']
        candel['high'] = max([candel['open'],lc['middle']])
        candel['middle'] = (candel['high'] + candel['low']) / 2           
        candles.append(candel)
        candel = candel.copy()
        candel['close'] = lc['high']
        candel['high'] = lc['high']
        candel['middle'] = lc['middle']
        candles.append(candel)
    else:
        candel['close'] = lc['high']
        candel['high'] = lc['high']
        candel['middle'] = (candel['high'] + candel['low']) / 2
        candles.append(candel)
        candel = candel.copy()
        candel['close'] = lc['middle']
        candel['low'] = min([candel['open'],lc['middle']])
        candel['middle'] = (candel['high'] + candel['low']) / 2           
        candles.append(candel)
        candel = candel.copy()
        candel['close'] = lc['low']
        candel['low'] = lc['low']
        candel['middle'] = lc['middle']
        candles.append(candel)
    candles.append(lc)
    new_candles = []
    for i,candel in enumerate(candles):
        candel = candel.copy()
        candel['volume'] = volume * (i+1)
        candel['direction'] = 1 if candel['open'] <= candel['close'] else -1
        new_candles.append(candel)
    return new_candles

def work_action_v3_CA(action, trades, cur_price, fee, fees, equity, equity_fee, pos, open_price,open_fee,row_name,longs:list,shorts:list,closes:list):
    """return pos,open_price,fees,open_fee"""
    # actions = (None,'long_pw','short_pw','close_long_pw','close_short_pw','close_all_pw')
    reward = 0
    delta = 0
    feei = (fee * cur_price) / 100  # fee абсолютное значение
    # print(feei)
    if action == 1:  # long
        if pos != 1:
            if pos == 0:
                open_price = cur_price
                reward = -fee  # комиссия за открытие
                fees += feei
                # equity_fee.append(equity_fee[-1] - feei)
                open_fee = feei
            else:  # был шорт, закрываем его и открываем лонг
                delta = open_price - cur_price  # прибыль по шорту (как при action=4)
                trades['total'] += delta
                reward = ((delta  / cur_price) * 100) - fee*2   # комиссия за закрытие + открытие
                open_price = cur_price  # новая цена для лонга
                fees += feei * 2
                equity.append(equity[-1] + delta)
                equity_fee.append(equity_fee[-1] + delta - feei * 2 - open_fee)
                open_fee = 0
            longs.append((row_name,cur_price))
            pos = 1
            trades['count'] += 1

    elif action == 2:  # short
        if pos != -1:
            if pos == 0:
                open_price = cur_price
                reward = -fee  # комиссия за открытие
                fees += feei
                open_fee = feei
                # equity_fee.append(equity_fee[-1] - feei)
            else:  # был лонг, закрываем его и открываем шорт
                delta = cur_price - open_price  # прибыль по лонгу (как при action=3)
                trades['total'] += delta
                reward = ((delta  / cur_price) * 100) - fee*2  # комиссия за закрытие + открытие
                open_price = cur_price  # новая цена для шорта
                fees += feei * 2
                equity.append(equity[-1] + delta)
                equity_fee.append(equity_fee[-1] + delta - feei * 2 - open_fee)
                open_fee = 0
            shorts.append((row_name,cur_price))
            pos = -1
            trades['count'] += 1

    elif action == 3:  # close long
        if pos == 1:
            delta = cur_price - open_price
            trades['total'] += delta
            reward = ((delta  / cur_price) * 100) - fee 
            pos = 0
            fees += feei
            equity.append(equity[-1] + delta)
            equity_fee.append(equity_fee[-1] + delta - feei - open_fee)
            open_fee = 0
            closes.append((row_name,cur_price))

    elif action == 4:  # close short
        if pos == -1:
            delta = open_price - cur_price
            trades['total'] += delta
            reward = ((delta  / cur_price) * 100) - fee 
            pos = 0
            fees += feei
            equity.append(equity[-1] + delta)
            equity_fee.append(equity_fee[-1] + delta - feei - open_fee)
            open_fee = 0
            closes.append((row_name,cur_price))
    elif action == 5:
        if pos == 1:
            delta = cur_price - open_price
            trades['total'] += delta
            reward = ((delta  / cur_price) * 100) - fee
            pos = 0
            fees += feei
            equity.append(equity[-1] + delta)
            equity_fee.append(equity_fee[-1] + delta - feei - open_fee)
            open_fee = 0
            closes.append((row_name,cur_price))
        elif pos == -1:
            delta = open_price - cur_price
            trades['total'] += delta
            reward = ((delta  / cur_price) * 100) - fee
            pos = 0
            fees += feei
            equity.append(equity[-1] + delta)
            equity_fee.append(equity_fee[-1] + delta - feei - open_fee)
            open_fee = 0
            closes.append((row_name,cur_price))
    trades['total_fee_per'] += reward
    return pos,open_price,fees,open_fee

def work_action_v3(action, trades, cur_price, fee, fees, equity, equity_fee, pos, open_price,open_fee,row_name,longs:list,shorts:list,closes:list):
    """return pos,open_price,fees,open_fee"""
    # actions = (None,'long_pw','short_pw','close_long_pw','close_short_pw','close_all_pw')
    action = np.where(actions_array == action)[0][0]
    reward = 0
    delta = 0
    feei = (fee * cur_price) / 100  # fee абсолютное значение
    # print(feei)
    if action == 1:  # long
        if pos != 1:
            if pos == 0:
                open_price = cur_price
                reward = -fee  # комиссия за открытие
                fees += feei
                # equity_fee.append(equity_fee[-1] - feei)
                open_fee = feei
            else:  # был шорт, закрываем его и открываем лонг
                delta = open_price - cur_price  # прибыль по шорту (как при action=4)
                trades['total'] += delta
                reward = ((delta  / cur_price) * 100) - fee*2   # комиссия за закрытие + открытие
                open_price = cur_price  # новая цена для лонга
                fees += feei * 2
                equity.append(equity[-1] + delta)
                equity_fee.append(equity_fee[-1] + delta - feei * 2 - open_fee)
                open_fee = 0
            longs.append((row_name,cur_price))
            pos = 1
            trades['count'] += 1

    elif action == 2:  # short
        if pos != -1:
            if pos == 0:
                open_price = cur_price
                reward = -fee  # комиссия за открытие
                fees += feei
                open_fee = feei
                # equity_fee.append(equity_fee[-1] - feei)
            else:  # был лонг, закрываем его и открываем шорт
                delta = cur_price - open_price  # прибыль по лонгу (как при action=3)
                trades['total'] += delta
                reward = ((delta  / cur_price) * 100) - fee*2  # комиссия за закрытие + открытие
                open_price = cur_price  # новая цена для шорта
                fees += feei * 2
                equity.append(equity[-1] + delta)
                equity_fee.append(equity_fee[-1] + delta - feei * 2 - open_fee)
                open_fee = 0
            shorts.append((row_name,cur_price))
            pos = -1
            trades['count'] += 1

    elif action == 3:  # close long
        if pos == 1:
            delta = cur_price - open_price
            trades['total'] += delta
            reward = ((delta  / cur_price) * 100) - fee 
            pos = 0
            fees += feei
            equity.append(equity[-1] + delta)
            equity_fee.append(equity_fee[-1] + delta - feei - open_fee)
            open_fee = 0
            closes.append((row_name,cur_price))

    elif action == 4:  # close short
        if pos == -1:
            delta = open_price - cur_price
            trades['total'] += delta
            reward = ((delta  / cur_price) * 100) - fee 
            pos = 0
            fees += feei
            equity.append(equity[-1] + delta)
            equity_fee.append(equity_fee[-1] + delta - feei - open_fee)
            open_fee = 0
            closes.append((row_name,cur_price))
    elif action == 5:
        if pos == 1:
            delta = cur_price - open_price
            trades['total'] += delta
            reward = ((delta  / cur_price) * 100) - fee
            pos = 0
            fees += feei
            equity.append(equity[-1] + delta)
            equity_fee.append(equity_fee[-1] + delta - feei - open_fee)
            open_fee = 0
            closes.append((row_name,cur_price))
        elif pos == -1:
            delta = open_price - cur_price
            trades['total'] += delta
            reward = ((delta  / cur_price) * 100) - fee
            pos = 0
            fees += feei
            equity.append(equity[-1] + delta)
            equity_fee.append(equity_fee[-1] + delta - feei - open_fee)
            open_fee = 0
            closes.append((row_name,cur_price))
    trades['total_fee_per'] += reward
    return pos,open_price,fees,open_fee

def check_strategy_v4(df: pd.DataFrame, work_strategy, fee=0.0002):
    """
    return trades,equity,equity_fee,longs,shorts,closes
    Улучшенная версия:
    - 5-шаговый тестер
    """
    df = df.copy()
    df['volume'] = df['volume'].astype(float)
    trades = {'total': 0, 'count': 0, 'total_fee_per': 0}
    pos = 0
    open_price = 0
    equity = [0]
    equity_fee = [0]
    fees = 0
    longs = []
    shorts = []
    closes = []
    fee_one_p = (fee / 2) * 100
    open_fee = 0
    period2x = 300
    for i in tqdm(range(period2x,len(df.index))):
        
        lc = df.iloc[i-1]
        step_candles = get_step_candles(lc)
        df_slice = df.iloc[i-period2x:i].copy()
        for sc in step_candles:
            df_slice.iloc[-1] = sc
            df_temp = df_slice.copy()
            test_row= work_strategy.get_test_row(df_temp)
            action = work_strategy(test_row)
            pos, open_price, fees, open_fee = work_action_v3(
                action, trades, sc['close'], fee_one_p, fees, equity, equity_fee, pos, open_price,open_fee,test_row['x'],longs,shorts,closes
            )
            # print(test_row)
            # print(action,pos,open_price,trades)
            # print(len(longs),len(shorts),len(closes))
            # input()
            # print('-------')

    df_eq = pd.DataFrame({'eq':equity,'eq_fee':equity_fee})
    if df_eq.empty:
        trades.update({
        'total_abs_fee': 0,
        'win_rate_wf': 0,
        'total_fee': fees,
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

        trades['total_fee_per'] = round(trades['total_fee_per'],2)
        trades.update({
            'total_abs_fee': equity_fee[-1],
            'win_rate_wf': win_rate,
            'total_fee': fees,
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
    
    return trades,equity,equity_fee,longs,shorts,closes

def work_action_v4(action, trades, cur_price, fee, fees, equity, equity_fee, pos, open_price,open_fee):
    # actions = (None,'long_pw','short_pw','close_long_pw','close_short_pw','close_all_pw')
    action = np.where(actions_array == action)[0][0]
    reward = 0
    delta = 0
    feei = (fee * cur_price) / 100  # fee абсолютное значение
    # print(feei)
    if action == 1:  # long
        if pos != 1:
            if pos == 0:
                open_price = cur_price
                reward = -fee  # комиссия за открытие
                fees += feei
                # equity_fee.append(equity_fee[-1] - feei)
                open_fee = feei
            else:  # был шорт, закрываем его и открываем лонг
                delta = open_price - cur_price  # прибыль по шорту (как при action=4)
                trades['total'] += delta
                reward = ((delta  / cur_price) * 100) - fee*2   # комиссия за закрытие + открытие
                open_price = cur_price  # новая цена для лонга
                fees += feei * 2
                equity.append(equity[-1] + delta)
                equity_fee.append(equity_fee[-1] + delta - feei * 2 - open_fee)
                open_fee = 0
            pos = 1
            trades['count'] += 1

    elif action == 2:  # short
        if pos != -1:
            if pos == 0:
                open_price = cur_price
                reward = -fee  # комиссия за открытие
                fees += feei
                open_fee = feei
                # equity_fee.append(equity_fee[-1] - feei)
            else:  # был лонг, закрываем его и открываем шорт
                delta = cur_price - open_price  # прибыль по лонгу (как при action=3)
                trades['total'] += delta
                reward = ((delta  / cur_price) * 100) - fee*2  # комиссия за закрытие + открытие
                open_price = cur_price  # новая цена для шорта
                fees += feei * 2
                equity.append(equity[-1] + delta)
                equity_fee.append(equity_fee[-1] + delta - feei * 2 - open_fee)
                open_fee = 0
            pos = -1
            trades['count'] += 1

    elif action == 3:  # close long
        if pos == 1:
            delta = cur_price - open_price
            trades['total'] += delta
            reward = ((delta  / cur_price) * 100) - fee 
            pos = 0
            fees += feei
            equity.append(equity[-1] + delta)
            equity_fee.append(equity_fee[-1] + delta - feei - open_fee)
            open_fee = 0

    elif action == 4:  # close short
        if pos == -1:
            delta = open_price - cur_price
            trades['total'] += delta
            reward = ((delta  / cur_price) * 100) - fee 
            pos = 0
            fees += feei
            equity.append(equity[-1] + delta)
            equity_fee.append(equity_fee[-1] + delta - feei - open_fee)
            open_fee = 0
    elif action == 5:
        if pos == 1:
            delta = cur_price - open_price
            trades['total'] += delta
            reward = ((delta  / cur_price) * 100) - fee
            pos = 0
            fees += feei
            equity.append(equity[-1] + delta)
            equity_fee.append(equity_fee[-1] + delta - feei - open_fee)
            open_fee = 0
        elif pos == -1:
            delta = open_price - cur_price
            trades['total'] += delta
            reward = ((delta  / cur_price) * 100) - fee
            pos = 0
            fees += feei
            equity.append(equity[-1] + delta)
            equity_fee.append(equity_fee[-1] + delta - feei - open_fee)
            open_fee = 0
    trades['total_fee_per'] += reward
    return pos,open_price,fees,open_fee

def check_strategy_v5(df: pd.DataFrame, work_strategy, fee=0.0002,close_2330=False):
    """
    return trades,equity,equity_fee
    Облегченная версия:
    - 5-шаговый тестер
    """
    df = df.copy()
    if close_2330:
        df['ms'] = pd.to_datetime(df['ms'])
        df['close_2330'] = np.where((df['ms'].dt.hour == 23)&(df['ms'].dt.minute > 25),True,False)
    df['volume'] = df['volume'].astype(float)
    trades = {'total': 0, 'count': 0, 'total_fee_per': 0}
    pos = 0
    open_price = 0
    equity = [0]
    equity_fee = [0]
    fees = 0

    fee_one_p = (fee / 2) * 100
    open_fee = 0
    period2x = 300
    for i in range(period2x,len(df.index)):
        
        lc = df.iloc[i-1]
        step_candles = get_step_candles(lc)
        df_slice = df.iloc[i-period2x:i].copy()
        for sc in step_candles:
            df_slice.iloc[-1] = sc
            df_temp = df_slice.copy()
            test_row= work_strategy.get_test_row(df_temp)
            action = work_strategy(test_row)
            if close_2330:
                if test_row['close_2330']:
                    action = 'close_all_pw'
            pos, open_price, fees, open_fee = work_action_v4(
                action, trades, sc['close'], fee_one_p, fees, equity, equity_fee, pos, open_price,open_fee
            )

    df_eq = pd.DataFrame({'eq':equity,'eq_fee':equity_fee})
    if df_eq.empty:
        trades.update({
        'total_abs_fee': 0,
        'win_rate_wf': 0,
        'total_fee': fees,
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

        trades['total_fee_per'] = round(trades['total_fee_per'],2)
        trades.update({
            'total_abs_fee': equity_fee[-1],
            'win_rate_wf': win_rate,
            'total_fee': fees,
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
    
    return trades,equity,equity_fee

def get_child_candles(df:pd.DataFrame,x):
    candels = []
    df = df.copy()
    df = df.reset_index(drop=True)
    for i,row in df.iterrows():
        if i == 0:
            candel = row
            candel['x'] = x
        else:
            candel['close'] = row['close']
            candel['volume'] += row['volume']
            candel['high'] = max(candel['high'],row['high'])
            candel['low'] = min(candel['low'],row['low'])
            candel['middle'] = (candel['high'] + candel['low']) / 2
            candel['direction'] = 1 if candel['open'] < candel['close'] else -1
        candels.append(candel.copy())
    return candels

def check_strategy_v6(df: pd.DataFrame, work_strategy, fee=0.0002,close_2330=False,timeframe='5min'):
    """
    return trades,equity,equity_fee,longs,shorts,closes,df_big
    Улучшенная версия:
    - шаговый тестер через младшие таймфреймы
    """
    df = df.copy()
    df['ms'] = pd.to_datetime(df['ms'])
    df_big = convert_timeframe(df,timeframe)
    if close_2330:
        df_big['close_2330'] = np.where((df_big['ms'].dt.hour == 23)&(df_big['ms'].dt.minute > 25),True,False)
        df['close_2330'] = np.where((df['ms'].dt.hour == 23)&(df['ms'].dt.minute > 25),True,False)
    trades = {'total': 0, 'count': 0, 'total_fee_per': 0}
    pos = 0
    open_price = 0
    equity = [0]
    equity_fee = [0]
    fees = 0
    longs = []
    shorts = []
    closes = []
    fee_one_p = (fee / 2) * 100
    open_fee = 0
    period2x = 300
    for i in tqdm(range(period2x,len(df_big.index))):
        
        lc = df_big.iloc[i-1]
        start_time = lc['ms']
        end_time = start_time + pd.Timedelta(minutes=5)
        df_child = df[(df['ms'] >= start_time)&(df['ms'] < end_time)]
        child_candles = get_child_candles(df_child,lc['x'])
        df_slice = df_big.iloc[i-period2x:i].copy()
        for sc in child_candles:
            df_slice.iloc[-1] = sc
            df_temp = df_slice.copy()
            test_row= work_strategy.get_test_row(df_temp)
            action = work_strategy(test_row)
            if close_2330:
                if test_row['close_2330']:
                    action = 'close_all_pw'
            pos, open_price, fees, open_fee = work_action_v3(
                action, trades, sc['close'], fee_one_p, fees, equity, equity_fee, pos, open_price,open_fee,test_row['x'],longs,shorts,closes
            )
            # print(test_row)
            # print(action,pos,open_price,trades)
            # print(len(longs),len(shorts),len(closes))
            # input()
            # print('-------')

    df_eq = pd.DataFrame({'eq':equity,'eq_fee':equity_fee})
    if df_eq.empty:
        trades.update({
        'total_abs_fee': 0,
        'win_rate_wf': 0,
        'total_fee': fees,
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

        trades['total_fee_per'] = round(trades['total_fee_per'],2)
        trades.update({
            'total_abs_fee': equity_fee[-1],
            'win_rate_wf': win_rate,
            'total_fee': fees,
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
    
    return trades,equity,equity_fee,longs,shorts,closes,df_big