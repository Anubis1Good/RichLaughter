import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
from datetime import datetime
from utils.draw_utils import draw_lite_chart,draw_chart_channel,draw_hb_chart,draw_bollinger,draw_dynamics,draw_rails
from ForBots.Indicators.classic_indicators import add_donchan_channel,add_vangerchik,add_sma, add_slice_df,add_bollinger,add_over_bb,add_attached_bb,add_big_volume,add_dynamics_ma

file = 'logs\work_logs\MMH5_1_MTA_LORD.txt'

with open(file,'a+') as f:
    f.write(f'{datetime.now()} : JOPPA\n')
    f.seek(0)  # Перемещаем указатель в начало файла
    lines = f.readlines()
if len(lines) > 5:
    lines = lines[-2:]
    with open(file,'w') as f:
        f.writelines(lines)
