import traceback
import os
from datetime import datetime
import cv2
import pandas as pd
import numpy as np
import numpy.typing as npt
from datetime import datetime
# import pyautogui as pag
import pydirectinput as pdi
from Traders.VT.settingsPB import ColorsBtnBGR,TemplateCandle
# from Traders.VT.utils import only_close
from strategies.work_strategies.BaseTA import BaseTABitget
from utils.help_trades import funding_map

class VT5:
    def __init__(
            self,
            glass:tuple,
            chart:tuple,
            position:tuple,
            name:str,
            ws:tuple=(BaseTABitget,(20,)),
            close_on_time:bool=True,
            close_map:tuple=((22,30),(22,30),(22,30),(22,30),(22,30),(17,30),(17,30),),
            close_ff:bool=True
            ):
        self.glass_region = glass
        self.chart_region = chart
        self.position_region = position
        self.close_ff = close_ff
        now = datetime.now()
        cwd = now.weekday()
        self.close_on_time = close_on_time
        self.close_time = close_map[cwd]
        self.name = name
        self.funding = False
        for s in funding_map:
            if name in s:
                self.funding = True
        self.trader_name = 'VT5'
        conf = ws[1]
        self.ws = ws[0](name,'1m',"moex_stock",1,*conf)
        folder_error = 'logs/error_logs'
        if not os.path.exists(folder_error):
            os.makedirs(folder_error)
        self.error_log = os.path.join(folder_error,self.trader_name + '_' + self.name + '.txt')
        self.close_long = False
        self.close_short = False
        self.time_mode = None

    def _color_search(self,img:npt.ArrayLike,color:tuple[int],region:tuple[int]=(None,None,None,None),reverse:bool=False):
        try:
            result = np.argwhere(
                (img[region[1]:region[3],region[0]:region[2],0] == color[0])& 
                (img[region[1]:region[3],region[0]:region[2],1] == color[1])& 
                (img[region[1]:region[3],region[0]:region[2],2] == color[2])
            )
            y = -1 if reverse else 0
            if region[0]:
                return result[y,1]+region[0], result[y,0]+region[1]
            return result[y,1],result[y,0]

        except Exception:
            # traceback.print_exc()
            return -1,-1
        
    def _check_time(self):
        now = datetime.now()
        chour = now.hour
        cminute = now.minute
        if chour > 8:
            if chour == 18 and cminute > 20:
                return -3
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
    
    def _check_position(self,img) -> int:
        x,y = self._color_search(img,ColorsBtnBGR.best_bid,self.position_region)
        if x >= 0:
            return 1
        x,y = self._color_search(img,ColorsBtnBGR.best_ask,self.position_region)
        if x >= 0:
            return -1
        return 0
    
    def _send_open(self,direction):
        pdi.moveTo(self.glass_region[0]+11,self.glass_region[1]+11)
        pdi.press('f')
        if direction == 'long':
            button = 'a'
        elif direction == 'short':
            button = 's'
        else:
            button = 'f'
        pdi.press(button)

    def _send_close(self,direction):
        rev_direction = 'long' if direction == 'short' else 'short'
        pdi.press('z')
        self._send_open(rev_direction)
        pdi.press('z')

    def _reverse_pos(self,direction):
        pdi.moveTo(self.glass_region[0]+11,self.glass_region[1]+11)
        pdi.press('f')
        if direction == 'long':
            button = 'a'
        elif direction == 'short':
            button = 's'
        else:
            button = 'f'
        pdi.press('z')
        pdi.press(button)
        pdi.press('z')
        pdi.press(button)

    def _reset_req(self):
        pdi.moveTo(self.glass_region[0]+11,self.glass_region[1]+11)
        pdi.press('f')

    def _get_chart(self,img,region):
        chart = img[
        region[1]:region[3],
        region[0]:region[2]]
        return chart
    
    def _get_current_price(self,chart):
        x,y = self._color_search(chart,ColorsBtnBGR.cur_price_1,reverse=True)
        if y > 0:
            x,y2 = self._color_search(chart,ColorsBtnBGR.cur_price_1,reverse=False)
            return (x,(y+y2)//2)
        x,y = self._color_search(chart,ColorsBtnBGR.cur_price_2,reverse=True)
        if y > 0:
            x,y2 = self._color_search(chart,ColorsBtnBGR.cur_price_2,reverse=False)
            return (x,(y+y2)//2)
        return None,None    
    
    def _get_mask(self,chart:npt.ArrayLike,color) -> npt.ArrayLike:
        mask = cv2.inRange(chart,color,color)
        return mask
    
    def _get_candle_mask(self,chart:npt.ArrayLike) -> npt.ArrayLike:
        mask1 = self._get_mask(chart,ColorsBtnBGR.candle_color_1)
        mask2 = self._get_mask(chart,ColorsBtnBGR.candle_color_2)
        mask = cv2.add(mask1,mask2)
        kernel = np.ones((2, 1), np.uint8) 
        mask = cv2.erode(mask,kernel)
        return mask

    def _get_volume_mask(self,chart:npt.ArrayLike) -> npt.ArrayLike:
        mask1 = self._get_mask(chart,ColorsBtnBGR.volume_color_1)
        mask2 = self._get_mask(chart,ColorsBtnBGR.volume_color_2)
        mask = cv2.add(mask1,mask2)
        return mask
    
    def _get_cords_on_mask(self,mask:npt.ArrayLike) -> npt.NDArray:
        cords = np.argwhere(mask == 255)
        return cords

    def _get_help_df(self,chart,color,volume_cords: npt.NDArray,direction):
        kernel = np.ones((2, 1), np.uint8) 
        mask1 = self._get_mask(chart,color)
        candle_mask = cv2.erode(mask1,kernel)
        candle_cords = self._get_cords_on_mask(candle_mask)
        res_top = cv2.matchTemplate(candle_mask,TemplateCandle.candle_top,cv2.TM_CCOEFF_NORMED)
        res_top = np.argwhere(res_top >= 0.9)
        res_top = res_top[res_top[:, 1].argsort()]
        dir_hb = list()
        for i in range(res_top.shape[0]):
            res_top[i] = (res_top[i][0],res_top[i][1]+1)
            point_b = candle_cords[np.where(candle_cords[:,1] == res_top[i][1])]
            point_v = volume_cords[np.where(volume_cords[:,1] == res_top[i][1])]
            y_b = point_b[:,0].max()
            y_v = point_v[:,0].min()
            dir_hb.append([res_top[i][1],res_top[i][0],y_b,y_v,direction])
        dir_hb = pd.DataFrame(dir_hb,columns=['x','high','low','volume','direction'])
        return dir_hb
    
    def _get_df(self,img) -> pd.DataFrame:
        chart = self._get_chart(img,self.chart_region)
        volume_mask = self._get_volume_mask(chart)
        volume_cords = self._get_cords_on_mask(volume_mask)
        dhb_long = self._get_help_df(chart,ColorsBtnBGR.candle_color_1,volume_cords,-1)
        dhb_short = self._get_help_df(chart,ColorsBtnBGR.candle_color_2,volume_cords,1)
        dir_df = pd.concat([dhb_long,dhb_short])
        dir_df = dir_df.sort_values('x',axis=0)
        dir_df['middle'] = dir_df.apply(lambda row: (row['high'] + row['low'])//2,axis=1)
        dir_df['spred'] = dir_df.apply(lambda row:row['low']-row['high'],axis=1)
        dir_df = dir_df.reset_index(drop=True)
        offset = dir_df['volume'].max() + 1
        for k in ('high','low','volume','middle'):
            dir_df[k] = -dir_df[k] + offset
        # Временное решение вопроса open и close
        dir_df['open'] = dir_df.apply(lambda row: row['middle'] - 1 if row['direction'] > 0 else row['middle'] + 1,axis=1)
        dir_df['close'] = dir_df.apply(lambda row: row['middle'] + 1 if row['direction'] > 0 else row['middle'] - 1,axis=1)
        _,cur_price = self._get_current_price(chart)
        cur_price = - cur_price +offset
        dir_df.loc[dir_df.index[-1], 'close'] = (
            cur_price + 1 if dir_df['direction'].iloc[-1] > 0 else cur_price - 1
        )
        return dir_df
    
    def _work_action(self,action,pos):
        if 'close_long' in action:
            if pos == 1:
                self.close_long = True
                self._send_close('long')
            else:
                self._reset_req()
        elif 'close_short' in action:
            if pos == -1:
                self.close_short = True
                self._send_close('short')
            else:
                self._reset_req()
        elif 'long' in action:
            if pos == -1:
                self.close_short = True
                self._reverse_pos('long')
            if pos == 0:
                self._send_open('long')
        elif 'short' in action:
            if pos == 1:
                self.close_long = True
                self._reverse_pos('short')
            if pos == 0:
                self._send_open('short')
        elif 'close_all' in action:
            if pos == -1:
                self.close_short = True
                self._send_close('short')
            elif pos == 1:
                self.close_long = True
                self._send_close('long')
            else:
                self._reset_req()

    def run(self,img):
        try:
            time_mode = self._check_time()
            if time_mode == 0:
                return
            df = self._get_df(img)
            row = self.ws.get_test_row(df)
            action = self.ws(row)
            if self.close_on_time:
                    if time_mode == -1:
                        action = 'close_all_pw'
                    elif time_mode == -2:
                        if action == 'long_pw':
                            action = 'close_short_pw'
                        elif action == 'short_pw':
                            action = 'close_long_pw'
                    elif time_mode == -3 and self.funding and self.close_ff:
                        action = 'close_all_pw'
            # if self.close18:
            #     action = only_close(action,18,5)
            # action = only_close(action,23,5)
            pos = self._check_position(img)
            if pos == -1:
                self.close_long = False
            elif pos == 1:
                self.close_short = False
            else:
                self.close_short = False
                self.close_long = False
            if self.close_long:
                self._send_close('long')
            elif self.close_short:
                self._send_close('short')
            elif action:
                self._work_action(action,pos)
            else:
                self._reset_req()

        except Exception as err:
            print(f"!!!! {type(err).__name__}: {err} !!!!")
            with open(self.error_log,'a',encoding="utf-8") as f:
                f.write(str(datetime.now()) + "\n")
                f.write('\n')
                f.write(traceback.format_exc() + "\n")