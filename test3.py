import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# Загрузка данных
data = pd.read_csv('DataForTests\DataFromMOEX\MMH5_1_1739993452.csv', parse_dates=['ms'], index_col='ms')
# data = data.iloc[:100]
# Прогнозирование
def forecast_prices(data, steps):
    model = ExponentialSmoothing(data['close']).fit()
    forecast = model.forecast(steps)
    return forecast

# Прогноз на 10, 20, 30 и 60 шагов вперед
forecasts = {
    '10 bars': forecast_prices(data, 10),
    '20 bars': forecast_prices(data, 20),
    '30 bars': forecast_prices(data, 30),
    '60 bars': forecast_prices(data, 60)
}

print(forecasts)