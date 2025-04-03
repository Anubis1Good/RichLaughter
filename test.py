import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
import sqlite3
import zlib
import io
from datetime import datetime
from utils.draw_utils import draw_lite_chart,draw_chart_channel,draw_hb_chart,draw_bollinger,draw_dynamics,draw_rails
from ForBots.Indicators.classic_indicators import add_donchan_channel,add_vangerchik,add_sma, add_slice_df,add_bollinger,add_over_bb,add_attached_bb,add_big_volume,add_dynamics_ma

file = 'logs\work_logs\MMH5_1_MTA_LORD.txt'



db_path = 'dbs/moex_fut.db'
db_path = 'dbs/test_MOEX_FUT.db'

db = sqlite3.connect(db_path)
cursor = db.cursor()

robot_id = 11
ticker_id = 2

# cursor.execute('''
#     SELECT * FROM history_positions
#     WHERE close_timestamp >= datetime('now', '-1 hour')
#     ORDER BY close_timestamp DESC
# ''')
# res = cursor.fetchone()
# cursor.close()
# print(res)

# cursor.execute('''
# SELECT 
#     COUNT(*) AS total_trades,
#     SUM(result) AS gross_profit,
#     SUM(result_fee) AS net_profit,
#     SUM(CASE WHEN result > 0 THEN 1 ELSE 0 END) AS profitable_trades
# FROM history_positions
# WHERE robot_id = ? AND ticker_id = ?
# ''', (robot_id, ticker_id))

# existing_results = cursor.fetchone()

# print(existing_results)          

# # cursor.execute('''
# #     SELECT result, result_fee FROM history_positions
# #     WHERE robot_id = ? AND ticker_id = ?
# #     ''', (robot_id, ticker_id))
# cursor.execute('''
# SELECT 
#     result,
#     result_fee,
#     SUM(result) OVER (ORDER BY open_timestamp) AS cumulative_result,
#     SUM(result_fee) OVER (ORDER BY open_timestamp) AS cumulative_result_fee
# FROM history_positions
# WHERE robot_id = ? AND ticker_id = ? AND close_timestamp >= datetime('now', '-1 hour')
# ORDER BY open_timestamp
# ''', (robot_id, ticker_id))
# cursor.execute('''
# SELECT 
#     result,
#     result_fee,
#     SUM(result) OVER (ORDER BY open_timestamp) AS cumulative_result,
#     SUM(result_fee) OVER (ORDER BY open_timestamp) AS cumulative_result_fee
# FROM history_positions
# WHERE robot_id = ? AND ticker_id = ?
# ORDER BY open_timestamp
# ''', (robot_id, ticker_id))
# existing_results = cursor.fetchall()

# existing_results = np.array(existing_results)
# # res = existing_results[:,0].cumsum()
# # res_fee = existing_results[:,1].cumsum()
# # print(existing_results)
# res = existing_results[:,2]
# res_fee = existing_results[:,3]
# print(res)     
# print(res_fee)     

# cursor.close()
# db.close()

# plt.plot(res)
# plt.plot(res_fee)
# plt.show()


# import dropbox

# from utils.settings import settings

# # Токен доступа
# access_token = settings.dropbox_token

# dbx = dropbox.Dropbox(access_token)

# local_file_path = './Screening/strat_picks/1_1_test_MOEX_FUT.json'
# remote_file_path = '/MTA_SKYNET/1_1_utest_MOEX_FUT.json'

# mode = dropbox.files.WriteMode.overwrite

# with open(local_file_path, 'rb') as file:
#     dbx.files_upload(file.read(), remote_file_path,mode=mode)


# from Screening.robots.Architect import Architect
from Screening.robots.AgentSmith import AgentSmith

# # arch = Architect('dbs/test_MOEX_FUT.db',(1,5),(1,4))
# # arch.run()

smith = AgentSmith('1_1_test_MOEX_FUT.json')
smith.download_all()
# # smith.upload()
# smith.download()