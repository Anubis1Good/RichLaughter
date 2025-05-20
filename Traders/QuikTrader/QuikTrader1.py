import os
import traceback
from time import sleep
from datetime import datetime
import pandas as pd
from Traders.QuikTrader.QuikFuncs import get_bars,get_best_glass,get_pos_futures,close_active_order,send_transaction
from strategies.work_strategies.BaseTA import BaseTABitget

class QuikTrader1:
    def __init__(self,sec_code,class_code='SPBFUT',granularity='M5',quantity = 1,ws:tuple=(BaseTABitget,(20,))):
        self.sec_code = sec_code
        self.class_code = class_code
        self.granularity = granularity
        self.quantity = quantity
        conf = ws[1]
        self.count = conf[0]*3
        self.ws:BaseTABitget = ws[0](sec_code,'1m',"moex_stock",1,*conf)
        folder_error = 'logs/error_logsQT'
        if not os.path.exists(folder_error):
            os.makedirs(folder_error)
        self.error_log = os.path.join(folder_error,'QT1' + '_' + self.sec_code + '.txt')   

    def _check_position(self):
        pos = get_pos_futures(self.sec_code)
        return pos
    
    def _send_open(self,direction,quantity):
        close_active_order(self.sec_code)
        bbid,bask = get_best_glass(self.sec_code,self.class_code)
        price = bbid if direction == 'B' else bask
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
            if chour == 23 and cminute > 20:
                return -1
            return 1
        return 0
 
    def _work_action(self,action,pos):
        # print(action,pos)
        if pos > self.quantity:
            self._send_close('B',pos-self.quantity)
        elif pos < -self.quantity:
            self._send_close('S',abs(pos)-self.quantity)
        elif 'close_long' in action:
            if pos > 0:
                self._send_close('B',pos)
            else:
                self._reset_req()
        elif 'close_short' in action:
            if pos < 0:
                self._send_close('S',abs(pos))
            else:
                self._reset_req()
        elif 'long' in action:
            if pos < 0:
                # print('B',self.quantity + abs(pos))
                self._send_open('B',self.quantity + abs(pos))
            if pos == 0:
                self._send_open('B',self.quantity)
        elif 'short' in action:
            if pos > 0 :
                # print('S',self.quantity + pos)
                self._send_open('S',self.quantity + pos)
            if pos == 0:
                self._send_open('S',self.quantity)
        elif 'close_all' in action:
            if pos < 0 :
                self._send_close('S',abs(pos))
            elif pos > 0 :
                self._send_close('B',pos)
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
                action = self.ws(row)
                pos = self._check_position()
                if time_mode == -1:
                    action = 'close_all'
                if action:
                    self._work_action(action,pos)
                else:
                    self._reset_req()
        except Exception as err:
            print(f"!!!! {type(err).__name__}: {err} !!!!")
            with open(self.error_log,'a',encoding="utf-8") as f:
                f.write(str(datetime.now()) + "\n")
                f.write('\n')
                f.write(traceback.format_exc() + "\n")