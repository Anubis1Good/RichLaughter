import pandas as pd
import matplotlib.pyplot as plt
from utils.work_with_dataframe.convert_timeframe import convert_timeframe
from utils.draw_utils import draw_hb_chart_fast

raw_file = 'DataForTests\oldMoex\MMH5_1_1739993452.csv'
df = pd.read_csv(raw_file)
# df.info()
# df = convert_timeframe(df,'5min')
# df.info()
# print(df.tail())
# print(df.head())
draw_hb_chart_fast(df)
plt.show()