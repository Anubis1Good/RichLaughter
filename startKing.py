import os 
import json
import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication,QWidget,QListWidget,QPushButton,QHBoxLayout,QVBoxLayout,QDialog,QLabel,QTextBrowser
from Traders.TestingTrader.tickers_groups import tickersBitgetFut,tickersMoexFut,tickersMoexStock,tickersMoexSpecial
from Traders.TestingTrader.wss_maps import moexFutMap,bitgetFutMap,moexStockMap,moexMTAFutMap,moexMTAStockMap,bitgetMTAFutMap
from strategies.work_strategies.HelpTA import CloseTA,BaseTABitget
from Screening.utils.keys_strategies import get_dict_strategies
from Screening.robots.AgentSmith import AgentSmith
from Screening.utils.db_analisys_func import get_top_today_king

def join_maps(*maps):
    new_map = {}
    for t in maps[0]:
        new_map[t] = []
        for m in maps:
           new_map[t] += list(m[t])
        new_map[t].insert(0,(CloseTA,(10,)))
        new_map[t].insert(0,(BaseTABitget,(10,)))
        new_map[t] = tuple(new_map[t])
    return new_map

allbitgetFutMap = join_maps(bitgetFutMap,bitgetMTAFutMap)
allMoexFutMap = join_maps(moexFutMap,moexMTAFutMap)
allMoexStockMap = join_maps(moexStockMap,moexMTAStockMap)

bitgetFutDC = get_dict_strategies(allbitgetFutMap)
moexFutDC = get_dict_strategies(allMoexFutMap)
moexStockDC = get_dict_strategies(allMoexStockMap)

tickersExchange = (
    tickersBitgetFut,
    tickersMoexFut,
    tickersMoexStock,
    tickersMoexSpecial
)
wss_maps = (
    bitgetFutMap,
    moexFutMap,
    moexStockMap
)
allDC = {
    0:bitgetFutDC,
    1:moexFutDC,
    2:moexStockDC,
    3:moexStockDC,
}
exchages = (
    'Bitget_FUT',
    'MOEX_FUT',
    'MOEX_STOCK',
    'MOEX_SPECIAL',
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

stylesheet = """
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
                font-size:14px;
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
            QTextBrowser {
                background-color: #009B95;
                border-radius: 5px;
                color: white;
                font-size:14px;
                padding: 5px;
                margin: 5px;
            }
        """

class StrategySelectionDialog(QDialog):
    def __init__(self, strategies, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Выбор стратегии")
        self.setGeometry(100, 100, 400, 300)
        
        self.layout = QVBoxLayout()
        
        # Список стратегий
        self.list_widget = QListWidget()
        for bot, score in strategies.items():
            self.list_widget.addItem(f"{bot}: {score:.5f}")
        self.layout.addWidget(self.list_widget)
        
        # Кнопка выбора
        self.select_button = QPushButton("Выбрать")
        self.select_button.clicked.connect(self.accept)
        self.layout.addWidget(self.select_button)
        
        self.setLayout(self.layout)
        self.center_on_parent()

    def center_on_parent(self):
        if self.parent():
            # Получаем геометрию родительского окна
            parent_geometry = self.parent().geometry()
            
            # Вычисляем центр родительского окна
            x = parent_geometry.x() + (parent_geometry.width() - self.width()) // 2
            y = parent_geometry.y() + (parent_geometry.height() - self.height()) // 2
            
            # Устанавливаем позицию
            self.move(x, y)
    def selected_strategy(self):
        # Возвращает выбранную стратегию (без значения)
        selected_item = self.list_widget.currentItem()
        if selected_item:
            return selected_item.text().split(":")[0].strip()
        return None

class InfoWindow(QDialog):
    def __init__(self, data, parent=None):
        super().__init__()
        text = ''
        for d in data:
            text += f"{d} : {data[d]}\n"
        self.data = text
        self.initUI()
        self.center_on_parent()

    def center_on_parent(self):
        if self.parent():
            # Получаем геометрию родительского окна
            parent_geometry = self.parent().geometry()
            
            # Вычисляем центр родительского окна
            x = parent_geometry.x() + (parent_geometry.width() - self.width()) // 2
            y = parent_geometry.y() + (parent_geometry.height() - self.height()) // 2
            
            # Устанавливаем позицию
            self.move(x, y)

    def initUI(self):
        self.setWindowTitle('Детальная информация')
        self.setFixedSize(500, 500)
        self.setStyleSheet(stylesheet)
        label = QTextBrowser(self)
        label.setText(self.data)
        close_btn = QPushButton('Закрыть', self)
        close_btn.clicked.connect(self.close)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(close_btn)
        self.setLayout(layout)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('StartKing')
        self.main_layout = QHBoxLayout()
        self.resize(1400,800)
        self.setStyleSheet(stylesheet)
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
            set_strat_ticker_btn = QPushButton(text="SetStrategy")
            cur_choices_btn = QPushButton(text="CurrentChoices")
            close_all_btn = QPushButton(text="CloseAll")
            set_strat_all_btn = QPushButton(text='SetAllInterval')

            bwll1.addWidget(best_today_btn)
            bwll1.addWidget(best_mta_today_btn)
            bwll1.addWidget(check_best_today_btn)
            bwll1.addWidget(set_strat_ticker_btn)
            bwll1.addWidget(set_strat_all_btn)
            bwll1.addWidget(close_all_btn)
            bwll2.addWidget(load_btn)
            bwll2.addWidget(write_btn)
            bwll2.addWidget(send_btn)
            bwll2.addWidget(unlock_btn)
            bwll2.addWidget(unlock_all_btn)
            bwll2.addWidget(cur_choices_btn)
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
            set_strat_ticker_btn.clicked.connect(lambda check,dc=dc: self.set_strategy(dc))
            unlock_all_btn.clicked.connect(lambda check,dc=dc: self.unlock_all(dc))
            unlock_btn.clicked.connect(lambda check,dc=dc: self.unlock(dc))
            close_all_btn.clicked.connect(lambda check,dc=dc: self.set_help_all(dc,'CloseTA'))
            cur_choices_btn.clicked.connect(lambda check,dc=dc: self.show_cur_choice(dc))
            best_mta_today_btn.clicked.connect(lambda check,dc=dc: self.set_best_mta_strategies(dc))
            best_today_btn.clicked.connect(lambda check,dc=dc: self.set_best_bot_strategies(dc))
            set_strat_all_btn.clicked.connect(lambda check,dc=dc: self.set_strat_all(dc))
            check_best_today_btn.clicked.connect(lambda check,dc=dc: self.check_best_strategies_on_bot(dc))

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
        # dc.insert(0,'SleepTA')
        # dc.insert(0,'CloseTA')
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
            bot_key = next((key for key in allDC[index_ex] if str(t)+'_'+bot in key), 'SleepTA')
            for ticker in self.picks[exchages[index_ex]][t]:
                if not ticker in self.locks[exchages[index_ex]][t]:
                    self.picks[exchages[index_ex]][t][ticker] = bot_key
    
    def show_cur_choice(self,index_ex):
        # Получаем выбранный timeframe
        if self.qlwts[index_ex].currentItem():
            timeframe = self.qlwts[index_ex].currentItem().text()
            data = self.picks[exchages[index_ex]][timeframe]
            
            self.info_window = InfoWindow(data, self)  # Передаем self как родителя
            self.info_window.setWindowModality(Qt.WindowModal)  # Модальное окно
            self.info_window.show()

    def set_strat_all(self,index_ex):
        try:
            ticker = self.qlwss[index_ex].currentItem().text()
            t = self.qlwts[index_ex].currentItem().text()
            strategy = self.qlwbs[index_ex].currentItem().text()
            for ticker in self.picks[exchages[index_ex]][t]:
                if not ticker in self.locks[exchages[index_ex]][t]:
                    self.picks[exchages[index_ex]][t][ticker] = strategy
        except:
            print('Choice strategy')


    def processing_df(self, df):
        if df is None or df.empty or 'ticker' not in df.columns or 'bot' not in df.columns:
            return {}

        # Удаляем строки с пропусками
        df_clean = df.dropna(subset=['ticker', 'bot', 'total_result_fee'])
        
        # 1. Создаем основной словарь {тикер: [(бот1, score1), ...]}
        result_dict = (
            df_clean.groupby('ticker')[['bot', 'total_result_fee']]
            .apply(lambda x: list(zip(x['bot'], x['total_result_fee'])))
            .to_dict()
        )

        # 2. Рассчитываем средние места для раздела "Other"
        if not df_clean.empty:
            all_tickers = df_clean['ticker'].unique()
            all_bots = df_clean['bot'].unique()
            max_place_per_ticker = df_clean.groupby('ticker').size()  # Максимальное место в каждом тикере
            
            # Словарь для хранения мест каждой стратегии
            bot_rankings = {bot: [] for bot in all_bots}
            
            # Заполняем места для каждого тикера
            for ticker, bot_scores in result_dict.items():
                max_place = max_place_per_ticker[ticker]
                for place, (bot, score) in enumerate(bot_scores, start=1):
                    bot_rankings[bot].append(place)
                
                # Для ботов, которых нет в этом тикере, добавляем max_place + 1
                missing_bots = set(all_bots) - {b for b, s in bot_scores}
                for bot in missing_bots:
                    bot_rankings[bot].append(max_place + 1)
            
            # Вычисляем среднее место для каждого бота
            avg_places = {
                bot: sum(places) / len(places)
                for bot, places in bot_rankings.items()
                if places  # На всякий случай проверяем, что список не пустой
            }
            
            # Берем топ-5 ботов с наименьшим средним местом (чем меньше - тем лучше)
            top_bots_other = sorted(
                avg_places.items(),
                key=lambda x: x[1]
            )[:10]
            
            # Добавляем в результат
            result_dict["Other"] = top_bots_other

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
            self.picks[exchages[index_ex]][t] = self.check_old_strategies(bots,self.picks[exchages[index_ex]][t],self.locks[exchages[index_ex]][t])

    def get_top_today_all(self,index_ex,t):
        botsMta = get_top_today_king(dbs_mta[index_ex],t)
        botsBase = get_top_today_king(dbs_base[index_ex],t)
        bots = pd.concat([botsMta,botsBase],axis=0)
        bots = (
            bots
            .sort_values('total_result_fee', ascending=False)
            .groupby('ticker').head(10).reset_index(drop=True)
        )
        bots = self.processing_df(bots)
        return bots
    
    def set_best_bot_strategies(self,index_ex):
        for t in self.picks[exchages[index_ex]]:
            bots = self.get_top_today_all(index_ex,t)
            self.picks[exchages[index_ex]][t] = self.check_old_strategies(bots,self.picks[exchages[index_ex]][t],self.locks[exchages[index_ex]][t])
    
    def check_best_strategies_on_bot(self, index_ex):
        ticker = self.qlwss[index_ex].currentItem().text()
        timeframe = self.qlwts[index_ex].currentItem().text()
        
        # Получаем стратегии
        strategies = dict(self.get_top_today_all(index_ex, timeframe)[ticker])
        
        # Создаем и показываем диалоговое окно
        dialog = StrategySelectionDialog(strategies, self)
        if dialog.exec_() == QDialog.Accepted:
            selected_strategy = dialog.selected_strategy()
            if selected_strategy:
                self.picks[exchages[index_ex]][timeframe][ticker] = selected_strategy
                if not ticker in self.locks[exchages[index_ex]][timeframe]:
                    self.locks[exchages[index_ex]][timeframe].append(ticker)
                self.update_lock(index_ex)


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
    3.сделать CheckBestToday
    4. изменить other
"""