import pandas as pd
import numpy as np
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




#TODO trades['total_fee_per'] считается неправильно
# Ускоренная версия work_action (если нужно)
# @jit(nopython=True)
def work_action_v2(action, trades, cur_price, fee, fees, equity, equity_fee, pos, open_price,open_fee):
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
    # if reward != 0:
    #     delta_per = (delta  / cur_price) * 100
    #     debug['delta'].append(delta)
    #     debug['delta_per'].append(delta_per)
    #     debug['fee'].append(fee)
    #     debug['reward'].append(reward)
    #     debug['d_p-r'].append(delta_per-reward)
    #     debug['total_per'].append(trades['total_fee_per'])
    #     debug['cur_price'].append(cur_price)
    #     debug['eq'].append(equity[-1])
    #     debug['eq_f'].append(equity_fee[-1])
    #     print(len(debug['delta']))
    #     # if delta_per-reward < 0:
    #     #     print(delta,delta_per,fee,reward,delta_per-reward)
    #     #     print(trades['total_fee_per'])
    return pos,open_price,fees,open_fee

def check_strategy_v3(df: pd.DataFrame, work_strategy, fee=0.0002):
    """
    Улучшенная версия:
    - Возвращает словарь с метриками (Sharpe, MaxDD, Profit и т.д.).
    - Поддержка векторных операций.
    """
    trades = {'total': 0, 'count': 0, 'total_fee_per': 0}
    pos = 0
    open_price = 0
    equity = [0]
    equity_fee = [0]
    fees = 0
    
    # Получаем сигналы
    signals = df.apply(work_strategy, axis=1).values
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
    win_rate = round((wins / (wins + loss)) * 100,2)

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
