import os 
import json
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication,QWidget,QListWidget,QPushButton,QHBoxLayout,QVBoxLayout,QLabel
from Traders.TestingTrader.tickers_groups import tickersBitgetFut,tickersMoexFut,tickersMoexStock
from Traders.TestingTrader.wss_maps import moexFutMap,bitgetFutMap,moexStockMap
from Screening.utils.keys_strategies import get_dict_strategies
from Screening.robots.AgentSmith import AgentSmith
from Screening.utils.db_analisys_func import get_top_today_king

bitgetFutDC = get_dict_strategies(bitgetFutMap)
moexFutDC = get_dict_strategies(moexFutMap)
moexStockDC = get_dict_strategies(moexStockMap)

tickersExchange = (
    tickersBitgetFut,
    tickersMoexFut,
    tickersMoexStock
)
wss_maps = (
    bitgetFutMap,
    moexFutMap,
    moexStockMap
)
allDC = {
    0:bitgetFutDC,
    1:moexFutDC,
    2:moexStockDC
}
exchages = (
    'Bitget_FUT',
    'MOEX_FUT',
    'MOEX_STOCK',
)

dbs_base = (
    'dbs/test_Bitget_FUT.db',
    'dbs/test_MOEX_FUT.db',
    'dbs/test_MOEX_STOCK.db'
)

dbs_mta = (
    'dbs/test_BitgetM_FUT.db',
    'dbs/test_MOEXM_FUT.db',
    'dbs/test_MOEXM_STOCK.db'
)


def prepare_tickers(raw_tickers):
    tickers = list(map(lambda x: x[0],raw_tickers))
    tickers.insert(0,'Other')
    return tuple(tickers)

def prepare_timeframe(raw_map:dict):
    keys = raw_map.keys()
    keys = tuple(map(lambda x: str(x),keys))
    return keys

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('StartKing')
        self.main_layout = QHBoxLayout()
        self.resize(1400,800)
        self.setStyleSheet("""
            QWidget {
                background-color: #5CCDC9;
            }
            QListWidget {
                background-color: #FFFFFF;
                border-radius: 5px;
                border: none;

            }
            QListWidget::item {
                border: 1px solid #ccc;
                border-radius: 3px;
                padding: 2px;
                margin: 2px;
                background-color: #009B95;
                color: white;
            }
            
            QListWidget::item:selected {
                background-color: #A6A600;;
                border: 1px solid #999;
            }
            QListWidget::item:hover {
                background-color: #6C0AAB;
                border: 1px solid #999;
            }
            QLabel {
                background-color: #009B95;
                qproperty-alignment: 'AlignCenter';
                border-radius: 5px;
                color: white;
                font-size:18px;
            }
            QPushButton {
                background-color: #006561;
                color: white;
                padding: 5px;
                border-radius: 5px;
                border: none;
                font-size:14px;
            }
            QPushButton:hover {
                background-color: #6C0AAB;
            }
            QPushButton:pressed {
                background-color: #A6A600;
            }
        """)
        self.init_btn_style = """
            QPushButton {
                background-color: #006561;
                color: white;
                padding: 5px;
                border-radius: 5px;
                border: none;
                font-size:14px;
            }
            QPushButton:hover {
                background-color: #6C0AAB;
            }
            QPushButton:pressed {
                background-color: #A6A600;
            }
        """
        self.folder = 'Screening/strat_picks'
        if not os.path.exists(self.folder):
            os.mkdir(self.folder)
        self.line1 = QVBoxLayout()
        self.line2 = QVBoxLayout()
        self.line3 = QVBoxLayout()
        self.line4 = QVBoxLayout()
        self.line5 = QVBoxLayout()
        self.prepare_exchange()

        self.main_layout.addLayout(self.line1,stretch=1)
        self.main_layout.addLayout(self.line2,stretch=1)
        self.main_layout.addLayout(self.line3,stretch=2)
        self.main_layout.addLayout(self.line4,stretch=3)
        self.main_layout.addLayout(self.line5,stretch=2)
        self.setLayout(self.main_layout)
        

    def prepare_exchange(self):
        self.qlwss = [] #symbol
        self.qlwts = [] #timeframe
        self.qlwbs = [] #bot
        self.bws = [] #button widget
        self.picks = {} 
        self.locks = {}
        self.qllws = [] #locks
        for dc in allDC:
            qlsw = QListWidget()
            tickers = prepare_tickers(tickersExchange[dc])
            qlsw.addItems(tickers)
            qlsw.setCurrentRow(0)
            self.line1.addWidget(qlsw)
            self.qlwss.append(qlsw)
            qltw = QListWidget()
            qltw.addItems(prepare_timeframe(wss_maps[dc]))
            qltw.setCurrentRow(0)
            self.line2.addWidget(qltw)
            self.qlwts.append(qltw)
            qlbw = QListWidget()
            self.default_bots(dc,qltw,qlbw)
            self.line3.addWidget(qlbw)
            self.qlwbs.append(qlbw)
            bw = QWidget()
            bwl = QHBoxLayout(bw)
            bwll1 = QVBoxLayout()
            bwll2 = QVBoxLayout()
            bwl.addLayout(bwll1)
            bwl.addLayout(bwll2)
            write_btn = QPushButton(text='WritePicks')
            load_btn = QPushButton(text='LoadPicks')
            send_btn = QPushButton(text='SendPicks')
            best_today_btn = QPushButton(text='SetBestToday')
            best_mta_today_btn = QPushButton(text='SetMTAToday')
            unlock_all_btn = QPushButton(text='UnlockAll')
            unlock_btn = QPushButton(text='Unlock')
            check_best_today_btn = QPushButton(text='CheckBestToday')
            set_start_ticker_btn = QPushButton(text="SetStrategy")
            sleep_all_btn = QPushButton(text="SleepAll")
            close_all_btn = QPushButton(text="CloseAll")
            reserve_btn = QPushButton(text='GetMillion')
            reserve_btn.setDisabled(True)
            bwll1.addWidget(best_today_btn)
            bwll1.addWidget(best_mta_today_btn)
            bwll1.addWidget(check_best_today_btn)
            bwll1.addWidget(set_start_ticker_btn)
            bwll1.addWidget(sleep_all_btn)
            bwll1.addWidget(close_all_btn)
            bwll2.addWidget(load_btn)
            bwll2.addWidget(write_btn)
            bwll2.addWidget(send_btn)
            bwll2.addWidget(unlock_btn)
            bwll2.addWidget(unlock_all_btn)
            bwll2.addWidget(reserve_btn)
            self.line4.addWidget(bw)
            self.bws.append(bw)

            qllw = QListWidget()
            self.line5.addWidget(qllw)
            qllw.setSelectionMode(QListWidget.ExtendedSelection)
            self.qllws.append(qllw)

            self.qlwts[dc].itemClicked.connect(
                lambda checked, dc=dc: self.default_bots(dc, self.qlwts[dc], self.qlwbs[dc])
            )
            write_btn.clicked.connect(lambda check,dc=dc: self.write_files(exchages[dc]))
            load_btn.clicked.connect(lambda check,dc=dc: self.load_files(exchages[dc]))
            send_btn.clicked.connect(lambda check,dc=dc: self.send_files(exchages[dc]))
            set_start_ticker_btn.clicked.connect(lambda check,dc=dc: self.set_strategy(dc))
            unlock_all_btn.clicked.connect(lambda check,dc=dc: self.unlock_all(dc))
            unlock_btn.clicked.connect(lambda check,dc=dc: self.unlock(dc))
            close_all_btn.clicked.connect(lambda check,dc=dc: self.set_help_all(dc,'CloseTA'))
            sleep_all_btn.clicked.connect(lambda check,dc=dc: self.set_help_all(dc,'SleepTA'))
            best_mta_today_btn.clicked.connect(lambda check,dc=dc: self.set_best_mta_strategies(dc))

            self.locks[exchages[dc]] = {}
            self.picks[exchages[dc]] = {}
            for t in wss_maps[dc]:
                t = str(t)
                self.picks[exchages[dc]][t] = {}
                self.locks[exchages[dc]][t] = []
                for ticker in tickers:
                    self.picks[exchages[dc]][t][ticker] = "SleepTA"

    def default_bots(self,tickers:int,intervals:str,bots:QListWidget):
        bots.clear()
        interval = intervals.currentItem().text()
        dc = list(filter(lambda x: x.startswith(interval),allDC[tickers].keys()))
        dc.insert(0,'SleepTA')
        dc.insert(0,'CloseTA')
        bots.addItems(dc)
    
    def update_lock(self,index_ex):
        self.qllws[index_ex].clear()
        lock_picks = []
        for tf in self.locks[exchages[index_ex]]:
            for ticker in self.locks[exchages[index_ex]][tf]:
                lp = f"{ticker}_{tf} : {self.picks[exchages[index_ex]][tf][ticker]}"
                lock_picks.append(lp)
        self.qllws[index_ex].addItems(lock_picks)
    
    def unlock_all(self,index_ex):
        self.qllws[index_ex].clear()
        for tf in self.locks[exchages[index_ex]]:
            self.locks[exchages[index_ex]][tf].clear()


    def unlock(self,index_ex):
        tickers = self.qllws[index_ex].selectedItems()
        tickers = [item.text().split(' :')[0].split('_') for item in tickers]
        tickers = tuple(map(lambda x: (x[0],x[1]),tickers))
        for ticker,tf in tickers:
            self.locks[exchages[index_ex]][tf].remove(ticker)
        self.update_lock(index_ex)


    def set_strategy(self,index_ex):
        try:
            ticker = self.qlwss[index_ex].currentItem().text()
            timeframe = self.qlwts[index_ex].currentItem().text()
            strategy = self.qlwbs[index_ex].currentItem().text()
            self.picks[exchages[index_ex]][timeframe][ticker] = strategy
            if not ticker in self.locks[exchages[index_ex]][timeframe]:
                self.locks[exchages[index_ex]][timeframe].append(ticker)
            self.update_lock(index_ex)
        except:
            print('Choice strategy')

    def set_help_all(self,index_ex,bot):
        for t in self.picks[exchages[index_ex]]:
            for ticker in self.picks[exchages[index_ex]][t]:
                if not ticker in self.locks[exchages[index_ex]][t]:
                    self.picks[exchages[index_ex]][t][ticker] = bot

    def processing_df(self,df):
        if df is None or df.empty or 'ticker' not in df.columns or 'bot' not in df.columns:
            return {}
        # Удаляем строки с пропусками
        df_clean = df.dropna(subset=['ticker', 'bot', 'total_result_fee'])
        
        # Создаем список кортежей (бот, score) для каждого тикера
        result_dict = (
            df_clean.groupby('ticker')
            .apply(lambda x: list(zip(x['bot'], x['total_result_fee'])))
            .to_dict()
        )
        return result_dict
    
    def check_old_strategies(self,new_strategies,old_strategies,locks):
        final_data = {}
        for ticker in new_strategies:
            if ticker in locks:
                final_data[ticker] = old_strategies[ticker]
                continue
            new_d = None
            if ticker in old_strategies:
                old_strat = old_strategies[ticker]
                for i in range(len(new_strategies[ticker])):
                    if old_strat in new_strategies[ticker][i]:
                        new_d = new_strategies[ticker][i]
                        break
            best_strat = new_strategies[ticker][0]
            if best_strat[1] < 0:
                continue
            if new_d:
                if best_strat[1] /  (new_d[1]+ 1e-6) < 1.5:
                    best_strat = new_d
            final_data[ticker] = best_strat[0]
        return final_data
    
    def set_best_mta_strategies(self,index_ex):
        for t in self.picks[exchages[index_ex]]:
            bots = get_top_today_king(dbs_mta[index_ex],t)
            bots = self.processing_df(bots)
            self.check_old_strategies(bots,self.picks[exchages[index_ex]][t],self.locks[exchages[index_ex]][t])

    def write_files(self,ex):
        for tf in self.picks[ex]:
            filename = f"KING_{tf}_{ex}.json"
            picks = self.picks[ex][tf]
            file_path = os.path.join(self.folder,filename)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(picks, f, ensure_ascii=False, indent=2)

    def load_files(self,ex):
        for tf in self.picks[ex]:
            filename = f"KING_{tf}_{ex}.json"
            file_path = os.path.join(self.folder,filename)
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.picks[ex][tf] = data
            else:
                print('File not exist!')
    
    def send_files(self,ex):
        for tf in self.picks[ex]:
            filename = f"KING_{tf}_{ex}.json"
            smith = AgentSmith(filename)
            smith.upload()

if __name__ == '__main__':
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec()

# TODO
"""
    1.доделать SetMTAToday для Other
    2.сделать SetBestToday
    3.сделать CheckBestToday
"""