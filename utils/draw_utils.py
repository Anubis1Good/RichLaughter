import matplotlib.pyplot as plt
import pandas as pd

def draw_chart(df):
    plt.subplot(2,1,1)
    plt.plot(df['high'])
    plt.plot(df['low'])
    plt.subplot(2,1,2)
    plt.plot(df['volume'])

def draw_lite_chart(df):
    plt.plot(df['high'])
    plt.plot(df['low'])

def draw_hb_chart(row):
    clr = '#b7ea00' if row['direction'] == 1 else '#ff0013'
    plt.vlines(row.name,row['low'],row['high'],colors=clr)

def draw_hb_chart_fast(df):
    # Разделяем данные по направлениям
    longs = df[df['direction'] == 1]
    shorts = df[df['direction'] != 1]
    
    # Рисуем все линии за один вызов для каждого направления
    plt.vlines(longs.index, longs['low'], longs['high'], colors='#b7ea00')
    plt.vlines(shorts.index, shorts['low'], shorts['high'], colors='#ff0013')

def draw_hbwv_chart(row):
    clr = '#b7ea00' if row['direction'] == 1 else '#ff0013'
    plt.subplot(2,1,1)
    plt.vlines(row.name,row['low'],row['high'],colors=clr)
    plt.subplot(2,1,2)
    plt.vlines(row.name,0,row['volume'],colors='#6c6eff')

def draw_bars_chart(df):
    fig, (ax_price, ax_volume) = plt.subplots(2, 1, figsize=(12, 8))
    longs = df[df['direction'] == 1]
    shorts = df[df['direction'] != 1]
    
    tick_width = 1.5
    longs_index = longs['x']
    short_index = shorts['x']

    # tick_width = 0.3
    # longs_index = longs.index
    # short_index = shorts.index
        # Рисуем вертикальные линии (high-low)
    ax_price.vlines(longs_index, longs['low'], longs['high'], 
                    colors='#b7ea00', linewidth=1.5)
    ax_price.vlines(short_index, shorts['low'], shorts['high'], 
                    colors='#ff0013', linewidth=1.5)
    ax_price.hlines(longs['open'], 
                    longs_index - tick_width,
                    longs_index, 
                    colors='#b7ea00', linewidth=2)
    ax_price.hlines(shorts['open'], 
                    short_index - tick_width,
                    short_index, 
                    colors='#ff0013', linewidth=2)
    ax_price.hlines(longs['close'], 
                    longs_index, 
                    longs_index + tick_width,
                    colors='#b7ea00', linewidth=2)
    ax_price.hlines(shorts['close'], 
                    short_index, 
                    short_index + tick_width,
                    colors='#ff0013', linewidth=2)
    ax_price.grid(True, alpha=0.3)
    ax_volume.vlines(longs_index, 0, longs['volume'], 
                    colors='#b7ea00', linewidth=1.5)
    ax_volume.vlines(short_index, 0, shorts['volume'], 
                    colors='#ff0013', linewidth=1.5)
    ax_volume.grid(True, alpha=0.3)
    ax_price.autoscale_view()
    ax_volume.autoscale_view()
    plt.subplots_adjust(hspace=0)
    plt.tight_layout()
    fig.canvas.draw()
    return fig

def draw_chart_channel(df,top='max_hb',bottom='min_hb',median='avarege'):
    plt.plot(df[top])
    plt.plot(df[bottom])
    plt.plot(df[median])

def draw_bollinger(df,clr='blue'):
    plt.plot(df['bbu'],color=clr)
    plt.plot(df['bbd'],color=clr)
    plt.plot(df['sma'],color=clr)



def draw_dynamics(df,clr='red'):
    df.apply(lambda row: plt.text(row.name,row['low'],round(row['dynamics_ma'],1), fontsize=10,rotation='vertical'),axis=1)

def draw_rails(df,clr='blue'):
    df.apply(lambda row: plt.vlines(row.name,row['low'],row['high'],colors=clr) if row['rails'] else None,axis=1)

def draw_fractals_williams(df):
    df.apply(lambda row: plt.scatter(row.name,row['high'],color='#d64040' ) if row['fractal_up'] else 1,axis=1)
    df.apply(lambda row: plt.scatter(row.name,row['low'],color='#74992b' ) if row['fractal_down'] else 1,axis=1)

def draw_rsi(df):
    plt.plot(df['rsi'])
    plt.axhline(70, color='gray', linestyle='--', label='Перекупленность (70)')
    plt.axhline(30, color='gray', linestyle='--', label='Перепроданность (30)')

def draw_stochastic(df):
    plt.plot(df['%K'],color='blue')
    plt.plot(df['%D'],color='green')

def plot_pattern_forecast(df:pd.DataFrame, window=30):
    df = df.copy()
    df = df.reset_index(drop=True)
    fig, ax = plt.subplots(figsize=(15, 7))
    # Цена
    ax.plot(df.index, df['close'], label='Цена', color='black', lw=1.5)
    
    # Текущий паттерн
    current_start = df.index[-window]
    ax.axvspan(current_start, df.index[-1], color='red', alpha=0.1, label='Текущий паттерн')
    
    # Похожий паттерн
    if 'similar_pattern' in df.columns:
        similar_idx = df['similar_pattern'].first_valid_index()
        if similar_idx:
            similar_values = df.loc[similar_idx:similar_idx+window-1, 'similar_pattern']
            ax.plot(similar_values.index, similar_values, 'b-', label='Похожий паттерн', lw=2)
    
    # Прогноз
    if 'forecast' in df.columns:
        forecast_values = df['forecast'].dropna()
        ax.plot(forecast_values.index, forecast_values, 'g--', label='Прогноз', lw=2)
    
    ax.set_title('Прогноз на основе похожих паттернов')
    ax.legend()
    plt.show()