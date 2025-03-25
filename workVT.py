import os
from random import choice
import pyautogui as pag
import cv2
import matplotlib.pyplot as plt
from utils.draw_utils import draw_hb_chart,draw_hbwv_chart
from Traders.VT.VT5 import VT5
from Traders.VT.utils import configuration_traiders

config_file = 'Traders\VT\configsVT\config.txt'

param_bots = configuration_traiders(config_file)
trader = VT5(*param_bots,name='MXI')
data_folder = 'DataForTests\DataFromVT'
list_imgs = os.listdir(data_folder)
rand_img = choice(list_imgs)

img = cv2.imread(os.path.join(data_folder,rand_img))

df = trader._get_df(img)
print(df.tail())
# trader.run(img)
# df.apply(draw_hbwv_chart,axis=1)
cv2.imshow('work',img)
cv2.moveWindow('work',-10,-10)
# plt.show()
cv2.waitKey(0)