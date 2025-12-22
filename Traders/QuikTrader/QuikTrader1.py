import os
import traceback
from time import sleep,time
from datetime import datetime
import pandas as pd
from Traders.QuikTrader.QuikFuncs import get_bars,get_best_glass,get_pos_futures,close_active_order,send_transaction,get_code_orders,smart_close_active_order,get_order_by_trans_id, get_result_futures
from strategies.work_strategies.BaseTA import BaseTABitget

class QuikTrader1:
    def __init__(self,sec_code,class_code='SPBFUT',granularity='M5',quantity = 1,ws:tuple=(BaseTABitget,(20,)),need_debug=False,smart_reset=True):
        self.sec_code = sec_code
        self.class_code = class_code
        self.granularity = granularity
        self.quantity = quantity
        conf = ws[1]
        self.count = conf[0]*3
        self.ws:BaseTABitget = ws[0](sec_code,'1m',"moex_stock",1,*conf)
        self.need_debug = need_debug
        self.smart_reset = smart_reset
        folder_error = 'logs/error_logsQT'
        folder_debug = 'logs/debug_logsQT'
        if not os.path.exists(folder_error):
            os.makedirs(folder_error)
        if not os.path.exists(folder_debug):
            os.makedirs(folder_debug)
        self.error_log = os.path.join(folder_error,'QT1' + '_' + self.sec_code + '.txt')
        if need_debug:
            self.debug_log = os.path.join(folder_debug,'QT1_' + self.sec_code + '.txt')  

    def _check_position(self):
        pos = get_pos_futures(self.sec_code)
        return pos
    
    def _send_open(self,direction,quantity):
        bbid,bask = get_best_glass(self.sec_code,self.class_code)
        price = bbid if direction == 'B' else bask
        if self.smart_reset:
            skip_close = smart_close_active_order(self.sec_code,price)
            if skip_close == 0:
                send_transaction(self.sec_code,price,direction,quantity,self.class_code)
        else:
            close_active_order(self.sec_code)
            send_transaction(self.sec_code,price,direction,quantity,self.class_code)

    def _send_close(self,direction,quantity):
        rev_direction = 'B' if direction == 'S' else 'S'
        self._send_open(rev_direction,quantity)
    
    def _reset_req(self):
        close_active_order(self.sec_code)

    def _get_df(self) -> pd.DataFrame:
        df = get_bars(self.sec_code,self.granularity,self.count,self.class_code)
        return df
    
    def _check_time(self):
        now = datetime.now()
        chour = now.hour
        cminute = now.minute
        if chour > 8:
            if chour == 23:
                if cminute > 20:
                    return -1
                else:
                    return -2
            return 1
        return 0
    def _debug_log(self,pos,action):
        now = datetime.now()
        with open(self.debug_log,'a',encoding="utf-8") as f:
            f.write('vvvvvvvvvvvvv__' + str(now) + '__vvvvvvvvvvvvv' + '\n')
            f.write('pos: '+ str(pos) + '\n')
            f.write('action: '+ action + '\n')
    def _action_debug_log(self,pos,action):
        if self.need_debug:
            self._debug_log(pos,action)
    def _work_action(self,action,pos):
        # print(action,pos)
        if pos > self.quantity:
            self._send_close('B',pos-self.quantity)
            self._action_debug_log(pos,action)
        elif pos < -self.quantity:
            self._send_close('S',abs(pos)-self.quantity)
            self._action_debug_log(pos,action)
        elif action:
            if 'close_long' in action:
                if pos > 0:
                    self._send_close('B',pos)
                    self._action_debug_log(pos,action)
                else:
                    self._reset_req()
            elif 'close_short' in action:
                if pos < 0:
                    self._send_close('S',abs(pos))
                    self._action_debug_log(pos,action)
                else:
                    self._reset_req()
            elif 'long' in action:
                if pos < 0:
                    # print('B',self.quantity + abs(pos))
                    self._send_open('B',self.quantity + abs(pos))
                    self._action_debug_log(pos,action)
                elif pos == 0:
                    self._send_open('B',self.quantity)
                    self._action_debug_log(pos,action)
                elif pos < self.quantity:
                    self._send_open('B',self.quantity - pos)
                    self._action_debug_log(pos,action)
            elif 'short' in action:
                if pos > 0 :
                    # print('S',self.quantity + pos)
                    self._send_open('S',self.quantity + pos)
                    self._action_debug_log(pos,action)
                elif pos == 0:
                    self._send_open('S',self.quantity)
                    self._action_debug_log(pos,action)
                elif pos > -self.quantity:
                    self._send_open('S',self.quantity - abs(pos))
                    self._action_debug_log(pos,action)
            elif 'close_all' in action:
                if pos < 0 :
                    self._send_close('S',abs(pos))
                    self._action_debug_log(pos,action)
                elif pos > 0 :
                    self._send_close('B',pos)
                    self._action_debug_log(pos,action)
            else:
                self._reset_req()
        else:
            self._reset_req()

    def run(self):
        try:
            time_mode = self._check_time()
            if time_mode == 0:
                sleep(60*5)
                return
            else:
                df = self._get_df()
                row = self.ws.get_test_row(df)
                # print(self.sec_code,self.ws)
                action = self.ws(row)
                pos = self._check_position()
                if time_mode == -1:
                    action = 'close_all'
                if time_mode == -2:
                    action = action if 'close' in action else None
                self._work_action(action,pos)

        except Exception as err:
            print(datetime.now(), f"!!!! {type(err).__name__}: {err} !!!!")
            with open(self.error_log,'a',encoding="utf-8") as f:
                f.write(str(datetime.now()) + "\n")
                f.write('\n')
                f.write(traceback.format_exc() + "\n")

class QuikTrader2(QuikTrader1):
    def __init__(self, sec_code, class_code='SPBFUT', granularity='M5', quantity=1, ws = (BaseTABitget, (20, )), need_debug=False):
        super().__init__(sec_code, class_code, granularity, quantity, ws, need_debug)
        folder_error = 'logs/error_logsQT2'
        folder_debug = 'logs/debug_logsQT2'
        self.error_log = os.path.join(folder_error,'QT2' + '_' + self.sec_code + '.txt')
        if need_debug:
            self.debug_log = os.path.join(folder_debug,'QT2_' + self.sec_code + '.txt')
        if not os.path.exists(folder_error):
            os.makedirs(folder_error)
        if not os.path.exists(folder_debug):
            os.makedirs(folder_debug)
        self.start_pos = self._check_position()
        now = datetime.now()
        self.start_time = {
            'day': now.day,
            'hour': now.hour,
            'min': now.minute,
            'month': now.month,
            'sec': now.second,
            'year': now.year
        }

    def _check_today(self,order):
        date_order = order['datetime']
        if date_order['year'] != self.start_time['year']:
            return False
        if date_order['month'] != self.start_time['month']:
            return False
        if date_order['day'] != self.start_time['day']:
            return False
        if date_order['hour'] > self.start_time['hour']:
            return True
        if date_order['hour'] < self.start_time['hour']:
            return False
        if date_order['hour'] == self.start_time['hour']:
            if date_order['min'] < self.start_time['min']:
                return False
            if date_order['min'] == self.start_time['min'] and date_order['sec'] < self.start_time['sec']:
                return False
        return True
    
    def _check_pos_on_orders(self):
        orders = get_code_orders(self.sec_code)
        pos = self.start_pos
        for order in orders:
            flags = bin(order['flags'])
            if flags[-1] == '0' and flags[-2] == '0':
                delta = order['qty']
            else:
                delta = order['qty'] - order['balance']
            if self._check_today(order):
                if flags[-3] == '1':
                    pos -= delta
                else:
                    pos += delta
        return int(pos)
    
    def _debug_diff_pos(self,pos_old,pos_new):
        now = datetime.now()
        with open(self.debug_log,'a',encoding="utf-8") as f:
            f.write('POS_PROBLEM__' + str(now) + '__POS_PROBLEM' + '\n')
            f.write('pos_old: '+ str(pos_old) + '\n')
            f.write('pos_new: '+ str(pos_new) + '\n')

    def run(self):
        try:
            time_mode = self._check_time()
            if time_mode == 0:
                sleep(60*5)
                return
            else:
                df = self._get_df()
                row = self.ws.get_test_row(df)
                action = self.ws(row)
                pos_old = self._check_position()
                pos_new = self._check_pos_on_orders()
                # print(self.sec_code,self.ws,self.start_pos,pos_old,pos_new)
                if pos_old != pos_new and self.need_debug:
                    self._debug_diff_pos(pos_old,pos_new)
                if time_mode == -1:
                    action = 'close_all'
                self._work_action(action,pos_new)

        except Exception as err:
            print(datetime.now(),f"!!!! {type(err).__name__}: {err} !!!!")
            with open(self.error_log,'a',encoding="utf-8") as f:
                f.write(str(datetime.now()) + "\n")
                f.write('\n')
                f.write(traceback.format_exc() + "\n")

class QuikTrader3:
    def __init__(
            self,
            sec_code,
            class_code='SPBFUT',
            granularity='M5',
            quantity = 1,
            ws:tuple=(BaseTABitget,(20,)),
            need_debug=False,
            smart_reset=True,
            close_on_time:bool=True,
            close_map:tuple=((22,30),(22,30),(22,30),(22,30),(22,30),(17,30),(17,30),),
            stop_risk:int|float|None=None,
            cur_margin:bool=True
            ):
        self.sec_code = sec_code
        self.class_code = class_code
        self.granularity = granularity
        self.quantity = quantity
        conf = ws[1]
        self.count = conf[0]*3 #количество дней
        self.ws:BaseTABitget = ws[0](sec_code,'1m',"moex_stock",1,*conf)
        self.need_debug = need_debug
        self.smart_reset = smart_reset
        folder_error = 'logs/error_logsQT3'
        folder_debug = 'logs/debug_logsQT3'
        if not os.path.exists(folder_error):
            os.makedirs(folder_error)
        if not os.path.exists(folder_debug):
            os.makedirs(folder_debug)
        self.error_log = os.path.join(folder_error,'QT3' + '_' + self.sec_code + '.txt')
        if need_debug:
            self.debug_log = os.path.join(folder_debug,'QT3_' + self.sec_code + '.txt')  
        self.start_pos = self._check_position()
        now = datetime.now()
        cwd = now.weekday()
        self.close_on_time = close_on_time
        self.close_time = close_map[cwd]
        self.start_time = {
            'day': now.day,
            'hour': now.hour,
            'min': now.minute,
            'month': now.month,
            'sec': now.second,
            'year': now.year
        }
        self.last_order_id = None
        self.last_kill_order_id = None
        self.orders_start = False
        self.time_forgot_order = 0
        self.first_forgot = False
        self.index_margin = 0 if cur_margin else 1
        self.stop_risk = -stop_risk*self.quantity if stop_risk is not None else False
        self.first_risk = True
        self.time_mode = None
        print(self.sec_code,self.stop_risk)

    def _check_position(self):
        pos = get_pos_futures(self.sec_code)
        return pos

    def _check_risk(self):
        margin_total = get_result_futures(self.sec_code)[self.index_margin]
        return margin_total > self.stop_risk
    
    def _check_time(self):
        now = datetime.now()
        chour = now.hour
        cminute = now.minute
        if chour > 8:
            if chour >= self.close_time[0] - 1:
                if cminute > self.close_time[1]:
                    if chour >= self.close_time[0]:
                        return -1
                    else:
                        return -2
                elif chour == self.close_time[0]:
                    return -2
                elif chour > self.close_time[0]:
                    return -1
            return 1
        return 0
    
    def _check_today(self,order):
        date_order = order['datetime']
        if date_order['year'] != self.start_time['year']:
            return False
        if date_order['month'] != self.start_time['month']:
            return False
        if date_order['day'] != self.start_time['day']:
            return False
        if date_order['hour'] > self.start_time['hour']:
            return True
        if date_order['hour'] < self.start_time['hour']:
            return False
        if date_order['hour'] == self.start_time['hour']:
            if date_order['min'] < self.start_time['min']:
                return False
            if date_order['min'] == self.start_time['min'] and date_order['sec'] < self.start_time['sec']:
                return False
        return True
    
    def _check_pos_on_orders(self):
        orders = get_code_orders(self.sec_code)
        pos = self.start_pos
        for order in orders:
            flags = bin(order['flags'])
            if flags[-1] == '0' and flags[-2] == '0':
                delta = order['qty']
            else:
                delta = order['qty'] - order['balance']
            if self._check_today(order):
                if flags[-3] == '1':
                    pos -= delta
                else:
                    pos += delta
        return int(pos)
    
    def _send_open(self,direction,quantity):
        bbid,bask = get_best_glass(self.sec_code,self.class_code)
        price = bbid if direction == 'B' else bask
        if self.smart_reset:
            self.last_kill_order_id, skip_close = smart_close_active_order(self.sec_code,price)
            if skip_close == 0:
                self.last_order_id = send_transaction(self.sec_code,price,direction,quantity,self.class_code)
        else:
            self.last_kill_order_id = close_active_order(self.sec_code)
            self.last_order_id = send_transaction(self.sec_code,price,direction,quantity,self.class_code)
        if not self.orders_start:
            self.orders_start = True

    def _send_close(self,direction,quantity):
        rev_direction = 'B' if direction == 'S' else 'S'
        self._send_open(rev_direction,quantity)
    
    def _reset_req(self):
        self.last_kill_order_id = close_active_order(self.sec_code)

    def _get_df(self) -> pd.DataFrame:
        df = get_bars(self.sec_code,self.granularity,self.count,self.class_code)
        return df
    
    def _debug_log(self,pos,action):
        now = datetime.now()
        with open(self.debug_log,'a',encoding="utf-8") as f:
            f.write('vvvvvvvvvvvvv__' + str(now) + '__vvvvvvvvvvvvv' + '\n')
            f.write('pos: '+ str(pos) + '\n')
            f.write('action: '+ action + '\n')

    def _action_debug_log(self,pos,action):
        if self.need_debug:
            self._debug_log(pos,action)

    def _work_action(self,action,pos):
        # print(action,pos)
        if pos > self.quantity:
            self._send_close('B',pos-self.quantity)
            self._action_debug_log(pos,action)
        elif pos < -self.quantity:
            self._send_close('S',abs(pos)-self.quantity)
            self._action_debug_log(pos,action)
        elif action:
            if 'close_long' in action:
                if pos > 0:
                    self._send_close('B',pos)
                    self._action_debug_log(pos,action)
                else:
                    self._reset_req()
            elif 'close_short' in action:
                if pos < 0:
                    self._send_close('S',abs(pos))
                    self._action_debug_log(pos,action)
                else:
                    self._reset_req()
            elif 'long' in action:
                if pos < 0:
                    # print('B',self.quantity + abs(pos))
                    self._send_open('B',self.quantity + abs(pos))
                    self._action_debug_log(pos,action)
                elif pos == 0:
                    self._send_open('B',self.quantity)
                    self._action_debug_log(pos,action)
                elif pos < self.quantity:
                    self._send_open('B',self.quantity - pos)
                    self._action_debug_log(pos,action)
            elif 'short' in action:
                if pos > 0 :
                    # print('S',self.quantity + pos)
                    self._send_open('S',self.quantity + pos)
                    self._action_debug_log(pos,action)
                elif pos == 0:
                    self._send_open('S',self.quantity)
                    self._action_debug_log(pos,action)
                elif pos > -self.quantity:
                    self._send_open('S',self.quantity - abs(pos))
                    self._action_debug_log(pos,action)
            elif 'close_all' in action:
                if pos < 0 :
                    self._send_close('S',abs(pos))
                    self._action_debug_log(pos,action)
                elif pos > 0 :
                    self._send_close('B',pos)
                    self._action_debug_log(pos,action)
            else:
                self._reset_req()
        else:
            self._reset_req()

    
    def _debug_diff_pos(self,pos_old,pos_new):
        now = datetime.now()
        with open(self.debug_log,'a',encoding="utf-8") as f:
            f.write('POS_PROBLEM__' + str(now) + '__POS_PROBLEM' + '\n')
            f.write('pos_old: '+ str(pos_old) + '\n')
            f.write('pos_new: '+ str(pos_new) + '\n')

    def _check_bug_order(self):
        if self.orders_start:
            last_order = get_order_by_trans_id(self.last_order_id)
            if not last_order:
                print(datetime.now(),self.sec_code, 'not see last order:', self.last_order_id)
                if not self.first_forgot:
                    self.time_forgot_order = time()
                    self.first_forgot = True
                    return False
                else:
                    delta = time() - self.time_forgot_order
                    if delta < 1000:
                        return False
                    else:
                        self.first_forgot = False
        return True
    def run(self):
        try:
            time_mode = self._check_time()
            if time_mode != self.time_mode:
                print('TimeMode:',time_mode)
                self.time_mode = time_mode
            if time_mode == 0:
                sleep(60*5)
                return
            else:
                if not self._check_bug_order():
                    return
                df = self._get_df()
                row = self.ws.get_test_row(df)
                action = self.ws(row)
                pos_old = self._check_position()
                pos_new = self._check_pos_on_orders()
                # print(self.sec_code,self.ws,self.start_pos,pos_old,pos_new)
                if pos_old != pos_new and self.need_debug:
                    self._debug_diff_pos(pos_old,pos_new)
                if self.close_on_time:
                    if time_mode == -1:
                        action = 'close_all'
                    if time_mode == -2:
                        if action == 'long':
                            action = 'close_short'
                        elif action == 'short':
                            action = 'close_long'
                if self.stop_risk: #risk_management
                    if not self._check_risk():
                        if self.first_risk:
                            print(datetime.now(),self.sec_code, 'риск', self.stop_risk, 'превышен!')
                            self.first_risk = False
                        action = 'close_all'
                self._work_action(action,pos_new)

        except Exception as err:
            print(datetime.now(),self.sec_code,f"!!!! {type(err).__name__}: {err} !!!!")
            with open(self.error_log,'a',encoding="utf-8") as f:
                f.write(str(datetime.now()) + "\n")
                f.write('\n')
                f.write(traceback.format_exc() + "\n")