import cv2
import matplotlib.pyplot as plt
from Traders.VT.VT5 import VT5
from Traders.VT.VT6 import VT6
from Traders.VT.utils import configuration_traiders_grid
from strategies.work_strategies.BaseTA import BaseTABitget
from utils.draw_utils import draw_bars_chart

stock_groups= { 
    'GRID_test': (
        ['VTBR1','ETLN1','MTLR1','SGZH1'],

    )
}
file_config = 'Traders\VT\configsVT\config_grid_test.json'

file_img = 'DataForTests\ImgCs\Screenshot_41.png'
img = cv2.imread(file_img)

lines,price_step = configuration_traiders_grid(file_config)

work_traders:list[list[VT5]]=[]

for s in stock_groups['GRID_test']:
    traders = []
    for i in range(len(s)):
        ws,close18 = (BaseTABitget,(1,)),False
        glass:tuple = lines[0+5*i]
        chart:tuple = lines[1+5*i]
        position:tuple = lines[2+5*i]
        tape:tuple = lines[3+5*i]
        cluster:tuple = lines[4+5*i]
        price_step = price_step
        # trader = VT5(glass,chart,position,tape,cluster,price_step,s[i],ws)
        trader = VT6(glass,chart,position,tape,cluster,price_step,s[i],ws)
        traders.append(trader)
    work_traders.append(traders)

for wt in work_traders:
    for t in wt:
        df = t._get_df(img)
        print(df)
        fig = draw_bars_chart(df)
        plt.show()
