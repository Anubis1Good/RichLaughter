import os
from random import choice
import pyautogui as pag
import cv2
import matplotlib.pyplot as plt
from utils.draw_utils import draw_hb_chart,draw_hbwv_chart,draw_chart_channel
from Traders.VT.VT5 import VT5
from Traders.VT.utils import configuration_traiders
from ForBots.Indicators.classic_indicators import add_donchan_channel,add_vangerchik,add_sma, add_slice_df,add_bollinger,add_over_bb,add_attached_bb,add_big_volume,add_dynamics_ma,add_rsi,add_rsi_tw
config_file = 'Traders\VT\configsVT\config.txt'

param_bots = configuration_traiders(config_file)
trader = VT5(*param_bots,name='MXI')
data_folder = 'DataForTests\DataFromVT'
list_imgs = os.listdir(data_folder)
rand_img = choice(list_imgs)

img = cv2.imread(os.path.join(data_folder,rand_img))

df = trader._get_df(img)
df = add_donchan_channel(df,11)
df = add_rsi(df,11)
df = add_rsi_tw(df,11)

print(df.tail())
# trader.run(img)
plt.subplot(2,1,1)
draw_chart_channel(df)
df.apply(draw_hbwv_chart,axis=1)
plt.subplot(2,1,2)
plt.axline((0,70),(180,70))
plt.axline((0,30),(180,30))
plt.plot(df['rsi'],color='violet')
plt.plot(df['rsi_tw'],color='green')
# cv2.imshow('work',img)
# cv2.moveWindow('work',-10,-10)
plt.show()
# cv2.waitKey(0)