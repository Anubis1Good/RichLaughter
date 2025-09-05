# from Traders.QuikTrader.QuikFuncs import *
# sec_code = 'CRU5'
# sec_code = 'GZU5'
# acts = get_active_order(sec_code)
# smart_close_active_order(sec_code,'11.318')
# bbid,bask = get_best_glass(sec_code)
# print(type(bbid),bbid)
# # print(type(bask),bask)
# from Optimiztion.optimizations_groups.optuna_groups import group
# print(group)
# name_bot = 'RevPSTA7_ADVENTURE'
# print(name_bot[3:])
import torch

print(torch.cuda.is_available())