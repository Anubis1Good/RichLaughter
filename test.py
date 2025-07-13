# from datetime import datetime
# from Traders.QuikTrader.QuikFuncs import *
# from pprint import pprint
# sec_code = 'SRU5'
# # sec_code = 'MMU5'
# # sec_code = 'IMOEXF'
# # sec_code = 'CRU5'
# # sec_code = 'GZU5'
# # sec_code = 'RMU5'

# # pos = get_pos_futures(sec_code)

# # print(pos)

# # trans = send_transaction(sec_code,29000,'B',1)

# # print(trans)
# now = datetime.now()
# start_time = {
#     'day': now.day,
#     'hour': now.hour,
#     'min': now.minute,
#     'month': now.month,
#     'sec': now.second,
#     'year': now.year
# }
# class Help:
#     def __init__(self):
#         now = datetime.now()
#         self.start_time = {
#             'day': now.day,
#             'hour': now.hour,
#             'min': now.minute,
#             'month': now.month,
#             'sec': now.second,
#             'year': now.year
# }
# def check_time(self,order):
#     date_order = order['datetime']
#     if date_order['year'] != self.start_time['year']:
#         return False
#     if date_order['month'] != self.start_time['month']:
#         return False
#     if date_order['day'] != self.start_time['day']:
#         return False
#     if date_order['hour'] > self.start_time['hour']:
#         return True
#     if date_order['hour'] < self.start_time['hour']:
#         return False
#     if date_order['hour'] == self.start_time['hour']:
#         if date_order['min'] < self.start_time['min']:
#             return False
#         if date_order['min'] == self.start_time['min'] and date_order['sec'] < self.start_time['sec']:
#             return False
#     return True


# print(now)
# orders = get_code_orders(sec_code)
# pos = 0
# for order in orders:
#     # if order['order_num'] == 2022429262790821654:
#     # if order['order_num'] == 2033125311905973803:
#     #     pprint(order)
#     # if order['order_num'] == 2033125311905973848:
#     #     pprint(order)
#     flags = bin(order['flags'])
#     if flags[-1] == '0' and flags[-2] == '0':
#         delta = order['qty']
#     else:
#         # if order['balance'] > 0:
#         delta = order['qty'] - order['balance']
#     date_order = order['datetime']
#     if date_order['day'] == now.day and date_order['month'] == now.month and date_order['year'] == now.year:
#         if flags[-3] == '1':
#             pos -= delta
#         else:
#             pos += delta
#     # if flags[-1] == '0':
#     #     if flags[-2] == '0':
#     #         delta = order['qty']
#     #     else:
#     #         delta = order['qty'] - order['balance']
# print(sec_code,pos)
# #     # print(bin(int(flags)))
# #     if flags[-1] == '1':
# #         print(order['order_num'],'активна')
# #     elif flags[-2] == '1':
# #         print(order['order_num'],'снята')
# #     else:
# #         print(order['order_num'],'исполнена')
# #     if flags[-3] == '1':
# #         print(order['order_num'],'продажа')
# #     else:
# #         print(order['order_num'],'покупка')

# # pprint(orders[0])
