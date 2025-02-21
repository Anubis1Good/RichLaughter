import os
import pandas as pd
from datetime import datetime
# from utils.data_work_func import join_df

# folder = 'DataForTests\TicksBitget'

# join_df(folder,'DataForTests\TicksBidgetUnion')

df = pd.read_csv('DataForTests\TicksBidgetUnion\DOGEUSDT_union.csv')

start = df.iloc[0]['ts']//1000
end = df.iloc[-1]['ts']//1000

print(datetime.fromtimestamp(start))
print(datetime.fromtimestamp(end))