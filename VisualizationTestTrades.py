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
# print(df.head())
db_path = 'dbs/test_MOEX_FUT.db'


# 2. Загрузка сделок из базы данных
def load_trades(db_path, bot_id, ticker):
    conn = sqlite3.connect(db_path)
    query = '''
    SELECT hp.open_timestamp, hp.close_timestamp, hp.open_price, hp.close_price, 
           hp.direction, hp.result, hp.fee, hp.result_fee, t.name as ticker
    FROM history_positions hp
    JOIN tickers t ON hp.ticker_id = t.id
    WHERE hp.robot_id = ? AND t.name = ?
    ORDER BY hp.open_timestamp
    '''
    df_trades = pd.read_sql(query, conn, params=(bot_id, ticker))
    conn.close()
    
    # Конвертируем timestamp в datetime
    df_trades['open_timestamp'] = pd.to_datetime(df_trades['open_timestamp'])
    df_trades['close_timestamp'] = pd.to_datetime(df_trades['close_timestamp'])
    
    return df_trades

df_trades = load_trades(db_path, bot_id, ticker)
# df_trades.info()
# print(df_trades.head())
# 3. Функция для создания графика
def plot_trades_with_candles(candles_df, trades_df, title=''):
    # Настройка стиля
    mc = mpf.make_marketcolors(up='g', down='r', edge='inherit', wick='inherit')
    s = mpf.make_mpf_style(marketcolors=mc, gridstyle=':', y_on_right=False)
    
    # Подготовка дополнительных графиков для сделок
    apds = []
    
    print(f"Всего сделок для отображения: {len(trades_df)}")
    
    for idx, trade in trades_df.iterrows():
        # Преобразуем timestamp в тот же формат, что и в candles_df
        open_time = pd.to_datetime(trade['open_timestamp'])
        close_time = pd.to_datetime(trade['close_timestamp'])
        
        # Проверяем, что сделка в пределах отображаемых данных
        if open_time in candles_df.index and close_time in candles_df.index:
            print(f"Отображаем сделку {idx}: {open_time} - {close_time}")
            
            # Линия между точками
            line_data = pd.Series(
                [trade['open_price'], trade['close_price']],
                index=[open_time, close_time]
            )
            apds.append(mpf.make_addplot(
                line_data,
                type='line',
                color='#1f77b4' if trade['direction'] > 0 else '#ff7f0e',
                width=2
            ))
            
            # Точка входа
            apds.append(mpf.make_addplot(
                pd.Series(trade['open_price'], index=[open_time]),
                type='scatter',
                color='#1f77b4' if trade['direction'] > 0 else '#ff7f0e',
                marker='o',
                markersize=100
            ))
            
            # Точка выхода с результатом
            result_color = 'darkgreen' if trade['result_fee'] > 0 else 'darkred'
            apds.append(mpf.make_addplot(
                pd.Series(trade['close_price'], index=[close_time]),
                type='scatter',
                color=result_color,
                marker=f"${trade['result_fee']:.1f}",
                markersize=100
            ))
        else:
            print(f"Сделка {idx} вне диапазона графика: {open_time} - {close_time}")
    
    if not apds:
        print("Нет сделок в видимом диапазоне графика!")
        print(f"Диапазон графика: {candles_df.index.min()} - {candles_df.index.max()}")
        print(f"Диапазон сделок: {trades_df['open_timestamp'].min()} - {trades_df['close_timestamp'].max()}")
    
    # Параметры графика
    plot_kwargs = {
        'type': 'candle',
        'style': s,
        'addplot': apds,
        'title': f'{title}\nТикер: {ticker} | Бот: {bot_id}',
        'ylabel': 'Цена',
        'figratio': (15, 8),
        'datetime_format': '%Y-%m-%d %H:%M',
        'xrotation': 45,
        'show_nontrading': True,
        'warn_too_much_data': 10000
    }
    
    # Создание графика
    fig, axes = mpf.plot(candles_df, returnfig=True, **plot_kwargs)
    
    # Добавление легенды
    legend_elements = [
        mlines.Line2D([], [], color='#1f77b4', marker='o', linestyle='-', 
                     markersize=8, label='Покупка (Long)'),
        mlines.Line2D([], [], color='#ff7f0e', marker='o', linestyle='-', 
                     markersize=8, label='Продажа (Short)'),
        mlines.Line2D([], [], color='darkgreen', marker='$...$', linestyle='None',
                     markersize=10, label='Прибыль'),
        mlines.Line2D([], [], color='darkred', marker='$...$', linestyle='None',
                     markersize=10, label='Убыток')
    ]
    
    axes[0].legend(handles=legend_elements, loc='upper left')
    plt.tight_layout()
    plt.show()

# 4. Генерация графика
plot_title = f'Торговые сделки | {pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")}'
plot_trades_with_candles(df, df_trades, plot_title)