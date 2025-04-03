import sqlite3
import pandas as pd
import mplfinance as mpf
from matplotlib import lines as mlines
import matplotlib.pyplot as plt
from datetime import date, timedelta,datetime
from request_functions.download_moex import download_moex,create_df
board = "RFUD"
market = "forts"
engine= "futures"
ticker = 'MMM5'
bot_id = 17
start = str(date.today() - timedelta(days=2))
end = None

df = download_moex(ticker,1,start=start,end=end,board=board,market=market,engine=engine)
df = create_df(df)
df = df.set_index('ms')  # Устанавливаем время как индекс
df.index = pd.to_datetime(df.index)

def load_and_prepare_data(db_path, bot_id, ticker):
    """Загрузка и подготовка данных"""
    conn = sqlite3.connect(db_path)
    
    # 1. Загрузка сделок
    trades_query = """
    SELECT hp.open_timestamp, hp.close_timestamp, hp.open_price, hp.close_price,
           hp.direction, hp.result, hp.fee, hp.result_fee
    FROM history_positions hp
    JOIN tickers t ON hp.ticker_id = t.id
    WHERE hp.robot_id = ? AND t.name = ?
    ORDER BY hp.open_timestamp
    """
    df_trades = pd.read_sql(trades_query, conn, params=(bot_id, ticker))
    
    # Преобразование временных меток
    df_trades['open_timestamp'] = pd.to_datetime(df_trades['open_timestamp'])
    df_trades['close_timestamp'] = pd.to_datetime(df_trades['close_timestamp'])
    
    # 2. Проверка данных
    print("\n=== Проверка данных ===")
    print(f"Найдено сделок: {len(df_trades)}")
    if len(df_trades) > 0:
        print(f"Первая сделка: {df_trades['open_timestamp'].min()}")
        print(f"Последняя сделка: {df_trades['close_timestamp'].max()}")
    
    conn.close()
    return df_trades

def plot_trades_with_candles(candles_df, trades_df, title=''):
    # Настройка стиля
    mc = mpf.make_marketcolors(up='g', down='r', edge='inherit', wick='inherit')
    s = mpf.make_mpf_style(marketcolors=mc, gridstyle=':', y_on_right=False)
    
    # Подготовка дополнительных графиков
    apds = []
    visible_trades = 0
    
    # Преобразуем индекс свечей в datetime
    candles_df.index = pd.to_datetime(candles_df.index)
    
    for idx, trade in trades_df.iterrows():
        try:
            # Преобразуем timestamp сделок
            open_time = pd.to_datetime(trade['open_timestamp'])
            close_time = pd.to_datetime(trade['close_timestamp'])
            
            # Находим ближайшие свечи
            open_idx = candles_df.index.get_indexer([open_time], method='nearest')[0]
            close_idx = candles_df.index.get_indexer([close_time], method='nearest')[0]
            
            open_candle_time = candles_df.index[open_idx]
            close_candle_time = candles_df.index[close_idx]
            
            # Проверяем диапазон
            if (open_candle_time >= candles_df.index.min() and 
                close_candle_time <= candles_df.index.max()):
                
                visible_trades += 1
                color = 'blue' if trade['direction'] > 0 else 'red'
                
                # Точка входа
                apds.append(mpf.make_addplot(
                    pd.Series(trade['open_price'], index=[open_candle_time]),
                    type='scatter',
                    color=color,
                    marker='o',
                    markersize=80
                ))
                
                # Точка выхода
                result_color = 'green' if trade['result_fee'] > 0 else 'darkred'
                apds.append(mpf.make_addplot(
                    pd.Series(trade['close_price'], index=[close_candle_time]),
                    type='scatter',
                    color=result_color,
                    marker=f"${trade['result_fee']:.1f}",
                    markersize=100
                ))
                
                # Линия между точками (исправленный вариант)
                line_data = pd.DataFrame({
                    'price': [trade['open_price'], trade['close_price']],
                    'time': [open_candle_time, close_candle_time]
                }).set_index('time')['price']
                
                apds.append(mpf.make_addplot(
                    line_data,
                    type='line',
                    color=color,
                    width=1
                ))
        except Exception as e:
            print(f"Ошибка при обработке сделки {idx}: {e}")
            continue
    
    print(f"\nСделок в видимой области: {visible_trades}")
    
    if visible_trades == 0:
        print("\nПРИЧИНЫ ОТСУТСТВИЯ СДЕЛОК:")
        print("1. Разные форматы времени в сделках и свечах")
        print("2. Сделки вне диапазона свечей")
        print("3. Проблемы с преобразованием времени")
        
        if len(trades_df) > 0:
            sample = trades_df.iloc[0]
            print("\nПример первой сделки:")
            print("Вход:", sample['open_timestamp'])
            print("Выход:", sample['close_timestamp'])
    
    # Параметры графика
    plot_kwargs = {
        'type': 'candle',
        'style': s,
        'addplot': apds if apds else None,
        'title': f'{title}\nТикер: {ticker} | Бот: {bot_id} | Сделок: {visible_trades}',
        'ylabel': 'Цена',
        'figratio': (15, 8),
        'warn_too_much_data': 10000
    }
    
    # Создание графика
    try:
        fig, axes = mpf.plot(candles_df, returnfig=True, **plot_kwargs)
        
        # Добавление легенды
        if visible_trades > 0:
            legend_elements = [
                mlines.Line2D([], [], color='blue', marker='o', linestyle='-', 
                            markersize=8, label='Покупка (Long)'),
                mlines.Line2D([], [], color='red', marker='o', linestyle='-', 
                            markersize=8, label='Продажа (Short)')
            ]
            axes[0].legend(handles=legend_elements, loc='upper left')
        
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"Ошибка при построении графика: {e}")
        # Резервный вариант - только свечи
        mpf.plot(candles_df, type='candle', style=s, 
                title=f'{ticker} (ошибка отображения сделок)')

# Основной код выполнения
if __name__ == "__main__":
    ticker = 'MMM5'
    bot_id = 1
    db_path = 'dbs/test_MOEX_FUT.db'
    
    # 1. Загрузка сделок
    df_trades = load_and_prepare_data(db_path, bot_id, ticker)
    
    # 2. Проверка данных
    print("\n=== Проверка данных ===")
    print(f"Свечей: {len(df)}, от {df.index.min()} до {df.index.max()}")
    print(f"Сделок: {len(df_trades)}, от {df_trades['open_timestamp'].min()} до {df_trades['close_timestamp'].max()}")
    
    # 3. Построение графика
    plot_trades_with_candles(df, df_trades, 'Торговые сделки')