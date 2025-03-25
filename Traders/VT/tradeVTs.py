import shutil
import os
import sys
import keyboard
import cv2
import pyautogui as pag
import numpy as np
from time import sleep
from PyQt5.QtCore import QThread, pyqtSignal,QMutex
from Traders.VT.VT5 import VT5
from Traders.VT.bot_on_ticker import init_trader
from Traders.VT.sgs import stock_groups

error_folder = 'logs\error_logs'


class TradeWorker(QThread):
    update_signal = pyqtSignal(str)
    def __init__(self, sg_key,param_bots):
        super().__init__()
        self.sg_key = sg_key  # Сохраняем параметры
        self.param_bots = param_bots
        self._active = True  # Дополнительный флаг контроля
        self._lock = QMutex()  # Для thread-safe операций
    def stop(self):
        self._lock.lock()
        self._active = False
        self._lock.unlock()
        self.requestInterruption()

    def run(self,):
        try:
            shutil.rmtree(error_folder)
        except Exception as e:
            pass
        self.work_traders:list[VT5] = []
        sg = stock_groups[self.sg_key]
        for s in sg:
            ws = init_trader(s)
            trader = VT5(*self.param_bots,s,ws)
            self.work_traders.append(trader)
        self.msleep(3000)
        while not self.isInterruptionRequested():
            self._lock.lock()
            active = self._active
            self._lock.unlock()
            
            if not active:
                break
            self.execute_trade_cycle()
            self.msleep(50)

    def execute_trade_cycle(self):
        for wt in self.work_traders:
            for _ in range(20):  # 20 * 100мс = 2 секунды
                if self.isInterruptionRequested():
                    return
                self.msleep(100)
            if self.isInterruptionRequested():
                return
            keyboard.send('shift')
            if self.isInterruptionRequested():
                return
            # pag.screenshot('Traders\VT\Screen.png')
            # img = cv2.imread('Traders\VT\Screen.png')
            img = np.array(pag.screenshot()) 
            img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
            # cv2.imwrite('test.png',img)
            wt.run(img)
            if keyboard.is_pressed('Esc'):
                print("\nyou pressed Esc, so exiting...")
                self.requestInterruption()  # Устанавливаем флаг прерывания
                return  # Выходим из цикла
                # sys.exit(0)
            pag.moveTo(wt.glass[0]+10,wt.glass[1]+10)
            keyboard.send('tab') 
            if self.isInterruptionRequested():
                return


def main_trade(sg_key,param_bots):
    try:
        shutil.rmtree(error_folder)
    except Exception as e:
        pass
    work_traders:list[VT5] = []
    sg = stock_groups[sg_key]
    for s in sg:
        ws = init_trader(s)
        trader = VT5(*param_bots,s,ws)
        work_traders.append(trader)
    
    # for wt in work_traders:
    #     print(wt.name,wt.ws)
    sleep(3)
    while True:
        for wt in work_traders:
            sleep(2)
            keyboard.send('shift')
            pag.screenshot('Traders\VT\Screen.png')
            img = cv2.imread('Traders\VT\Screen.png')
            wt.run(img)
            if keyboard.is_pressed('Esc'):
                print("\nyou pressed Esc, so exiting...")
                sys.exit(0)
            # pag.moveTo(wt.glass[0]+10,wt.glass[1]+10)
            keyboard.send('tab') 