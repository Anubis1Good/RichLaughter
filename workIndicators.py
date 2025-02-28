import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from Loader.BitgetLoader import bitget_loader
from utils.draw_utils import draw_lite_chart,draw_chart_channel,draw_hb_chart,draw_bollinger,draw_dynamics,draw_rails
from ForBots.Indicators.classic_indicators import *
from xgboost import XGBRegressor

raw_file = 'DataForTests\DataFromBitget\DOGEUSDT_1m_1739873922.csv'
period = 10
df = bitget_loader(raw_file)
# df = df.iloc[:100]

# Параметры
future_steps = 10  # Предсказание на 10 шагов вперёд
lags = 50  # Количество лагов для признаков

# Создание признаков (фичей) — лаги цен (close, high, low)
for i in range(1, lags + 1):
    df[f'close_lag_{i}'] = df['close'].shift(i)
    df[f'high_lag_{i}'] = df['high'].shift(i)
    df[f'low_lag_{i}'] = df['low'].shift(i)

# Целевые переменные — максимумы и минимумы на future_steps вперёд
df['target_high'] = df['high'].shift(-future_steps)
df['target_low'] = df['low'].shift(-future_steps)

# Убираем строки с NaN (из-за лагов и целевых переменных)
df = df.dropna()

# Признаки
X = df[[f'close_lag_{i}' for i in range(1, lags + 1)] + 
     [f'high_lag_{i}' for i in range(1, lags + 1)] + 
     [f'low_lag_{i}' for i in range(1, lags + 1)]]

# Целевые переменные
y_high = df['target_high']
y_low = df['target_low']

# Обучение модели XGBoost для предсказания максимумов
model_high = XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
model_high.fit(X, y_high)

# Обучение модели XGBoost для предсказания минимумов
model_low = XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
model_low.fit(X, y_low)

# Предсказание максимумов и минимумов
df['predicted_high'] = model_high.predict(X)
df['predicted_low'] = model_low.predict(X)
# Сдвигаем предсказания на future_steps назад
df['predicted_high_shifted'] = df['predicted_high'].shift(future_steps)
df['predicted_low_shifted'] = df['predicted_low'].shift(future_steps)

# Оценка модели
# mse = mean_squared_error(y_test, y_pred)
# print(f'Среднеквадратичная ошибка (MSE): {mse}')


# df = add_stochastic(df)
# df = add_slice_df(df,period)
# plt.subplot(2,1,1)
df.apply(draw_hb_chart,axis=1)
# df = add_fractals(df)
# plt.plot(df['high'], label='Реальные максимумы', color='green', alpha=0.7)
# plt.plot(df['low'], label='Реальные минимумы', color='red', alpha=0.7)
plt.plot(df['predicted_high'], label='Предсказанные максимумы', color='green', linestyle='--')
plt.plot(df['predicted_low'], label='Предсказанные минимумы', color='red', linestyle='--')

plt.plot(df['predicted_high_shifted'], label='Предсказанные максимумы', color='blue', linestyle=':')
plt.plot(df['predicted_low_shifted'], label='Предсказанные минимумы', color='blue', linestyle=':')
# plt.plot(df['sma'])

# print(df.tail())
# draw_chart_channel(df,'top_mean', 'bottom_mean', 'avarege_mean')

plt.show()