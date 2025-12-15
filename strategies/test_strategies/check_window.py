import pandas as pd
import numpy as np
from tqdm import tqdm

actions = (None,'long_pw','short_pw','close_long_pw','close_short_pw','close_all_pw')
actions_dict = {action: idx for idx, action in enumerate(actions)}

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


def check_strategy_window(df: pd.DataFrame, work_strategy, fee=0.0002,close_2330=False,window=150, normalization=False):
    """
    return trades,equity,equity_fee,longs,shorts,closes
    оконная версия
    """
    trades = {'total': 0, 'count': 0, 'total_fee_per': 0}
    pos = 0
    open_price = 0
    equity = [0]
    equity_fee = [0]
    fees = 0
    # Получаем сигналы
    # signals = df.apply(work_strategy, axis=1).values
    longs = []
    shorts = []
    closes = []
    fee_one_p = (fee / 2) * 100
    open_fee = 0
    if close_2330:
        df['ms'] = pd.to_datetime(df['ms'], format='%Y-%m-%d %H:%M:%S')
        df['hour'] = df['ms'].dt.hour
        df['minute'] = df['ms'].dt.minute
    for i in tqdm(range(len(df))):
        if i > window:
            df_slice = df.iloc[i-window:i]
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
                row = work_strategy.get_test_row(df_norm)
            else:
                row = work_strategy.get_test_row(df_slice)
            action = work_strategy(row)
            if close_2330:
                if row['hour'] == 23 and row['minute'] > 25:
                    action = 'close_all_pw'
            signal = actions_dict.get(action, None)
            pos, open_price, fees, open_fee = work_action_v3_CA(
                signal, trades, price, fee_one_p, fees, equity, equity_fee, pos, open_price,open_fee,row_name,longs,shorts,closes
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


