import matplotlib.pyplot as plt
from utils.draw_utils import draw_hb_chart_fast
from ForBots.Indicators.help_pva_indicators import get_all_enter_exit_DC
from ForBots.Indicators.pva_indicators import add_benefit
from Loader.BitgetLoader import bitget_loader
from ForBots.Indicators.classic_indicators import *
raw_file = 'DataForTests\DataFromBitget\DOGEUSDT_1m_1739873922.csv'
raw_file = 'DataForTests\DataFromMOEX\MMH5_1_1739993452.csv'
period = 10
df = bitget_loader(raw_file)
# df = df.iloc[-100:]
df = df.iloc[:200]
df = add_donchan_channel(df,20)
period = 30
all_starts,all_ends = get_all_enter_exit_DC(df,'max_hb','min_hb')
df = add_benefit(df,all_starts,all_ends,'DCr',period)
all_starts,all_ends = get_all_enter_exit_DC(df,'max_hb','avarege')
df = add_benefit(df,all_starts,all_ends,'DCmaxa',period)
all_starts,all_ends = get_all_enter_exit_DC(df,'avarege','min_hb')
df = add_benefit(df,all_starts,all_ends,'DCmina',period)
print(df.tail())

draw_hb_chart_fast(df)
for k in 'max_hb, min_hb, avarege'.split(', '):
    plt.plot(df[k],color='r',linestyle='--')

plt.show()