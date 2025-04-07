import os 
import json
import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime,timedelta
from Screening.utils.db_analisys_func import get_best_strategies,get_best_strategies_v2,get_best_strategies_v3,get_best_strategies_stable,get_best_strategies_v6

class Architect:
    def __init__(self,db_path,granularities,hourss):
        self.db_path = db_path
        self.granularities = granularities
        self.hourss = hourss
        self.folder_picks = 'Screening/strat_picks/'

    def save_file(self,ticker_bot_dict,hours,granularity):
        filename = str(hours) + '_' + str(granularity) + '_' + self.db_path.split('/')[-1].replace('.db','') +  '.json'
        filename = os.path.join(self.folder_picks,filename)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(ticker_bot_dict, f, ensure_ascii=False, indent=2)
    
    def run(self):
        for granularity in self.granularities:
            for hours in self.hourss:
                res = get_best_strategies_v3(self.db_path,granularity,hours)
                if not res.empty:
                    ticker_bot_dict = res.set_index('ticker')['bot'].to_dict()
                else:
                    ticker_bot_dict = {"poor": "0_sleep_0"}
                self.save_file(ticker_bot_dict,hours,granularity)
                


class StrategyTracker:
    def __init__(self, db_path):
        self.db_path = db_path
        self.previous_picks = {}
        self.hysteresis = 0.15  # Уменьшенный порог для большей стабильности
        self.min_score = 1.5    # Минимальный допустимый score

    def _get_current_candidates(self, granularity, lookback):
        df = get_best_strategies_stable(self.db_path, granularity, lookback)
        if df is None or df.empty or 'ticker' not in df.columns or 'bot' not in df.columns:
            return {}
        return df.dropna(subset=['ticker', 'bot']).set_index('ticker')['bot'].to_dict()

    def _get_strategy_score(self, ticker, bot_name, granularity, lookback):
        time_threshold = datetime.now() - timedelta(hours=lookback)
        time_threshold_str = time_threshold.strftime('%Y-%m-%d %H:%M:%S')
        
        query = """
        WITH strategy_stats AS (
            SELECT 
                AVG(hp.result_fee) AS avg_profit,
                SQRT(ABS(AVG(hp.result_fee * hp.result_fee) - POWER(AVG(hp.result_fee), 2))) AS stddev,
                AVG(CASE WHEN hp.result_fee > 0 THEN 1.0 ELSE 0.0 END) AS win_rate,
                MAX(hp.close_timestamp) AS last_trade_time
            FROM history_positions hp
            JOIN robots r ON hp.robot_id = r.id
            JOIN tickers t ON hp.ticker_id = t.id
            WHERE r.granularity = ?
            AND hp.close_timestamp >= ?
            AND r.name = ?
            AND t.name = ?
        )
        SELECT 
            (avg_profit / NULLIF(stddev, 0)) * win_rate AS stability_score,
            JULIANDAY(datetime('now')) - JULIANDAY(last_trade_time) AS recency
        FROM strategy_stats
        """
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                data = pd.read_sql(query, conn, 
                                params=(granularity, time_threshold_str, bot_name, ticker))
            
            if data.empty:
                return 0.0
                
            stability_score = data['stability_score'].iloc[0] or 0.0
            recency_score = 1 / (1 + data['recency'].iloc[0]) if data['recency'].iloc[0] > 0 else 0.0
            
            return 0.8 * stability_score + 0.2 * recency_score
            
        except Exception as e:
            print(f"Score calculation error: {e}")
            return 0.0

    def _should_keep_previous(self, ticker, new_bot, granularity, lookback):
        prev = self.previous_picks.get(ticker)
        if not prev:
            return False
        
        prev_score = self._get_strategy_score(ticker, prev['bot'], granularity, lookback)
        new_score = self._get_strategy_score(ticker, new_bot, granularity, lookback)
        
        # Новая логика: учитываем абсолютную разницу вместо относительной
        return (new_score - prev_score) < self.hysteresis * prev_score

    def update_strategies(self, granularity='1h', lookback=24):
        current = self._get_current_candidates(granularity, lookback)
        updated = {}
        
        for ticker, new_bot in current.items():
            current_score = self._get_strategy_score(ticker, new_bot, granularity, lookback)
            
            if current_score < self.min_score:
                continue  # Пропускаем стратегии с низким рейтингом
                
            if self._should_keep_previous(ticker, new_bot, granularity, lookback):
                updated[ticker] = self.previous_picks[ticker]['bot']
            else:
                updated[ticker] = new_bot
                self.previous_picks[ticker] = {
                    'bot': new_bot,
                    'timestamp': datetime.now(),
                    'score': current_score
                }
        
        return updated

class Architect_v2(StrategyTracker):
    def __init__(self, db_path, granularities, hourss):
        super().__init__(db_path)
        self.granularities = granularities
        self.hourss = hourss
        self.folder_picks = 'Screening/strat_picks/'
        self._load_previous_state()

    def _load_previous_state(self):
        if not os.path.exists(self.folder_picks):
            os.makedirs(self.folder_picks, exist_ok=True)
            return

        for fname in os.listdir(self.folder_picks):
            if fname.endswith('.json'):
                try:
                    with open(os.path.join(self.folder_picks, fname), 'r') as f:
                        data = json.load(f)
                        for ticker, bot in data.items():
                            if ticker not in self.previous_picks:
                                self.previous_picks[ticker] = {
                                    'bot': bot,
                                    'timestamp': datetime.now()
                                }
                except Exception as e:
                    print(f"Error loading {fname}: {e}")

    def save_file(self, strategies, hours, granularity):
        filename = f"{hours}_{granularity}_{self.db_path.split('/')[-1].replace('.db','')}.json"
        try:
            with open(os.path.join(self.folder_picks, filename), 'w') as f:
                json.dump(strategies, f, indent=2)
        except Exception as e:
            print(f"Save error: {e}")

    def get_fix_count_strategies(self,granularity):
        df = get_best_strategies_v6(self.db_path,granularity,10)
        if df is None or df.empty or 'ticker' not in df.columns or 'bot' not in df.columns:
            return {}
        return df.dropna(subset=['ticker', 'bot']).set_index('ticker')['bot'].to_dict()
    
    def save_file2(self,strategies, granularity):
        filename = f"FC_{granularity}_{self.db_path.split('/')[-1].replace('.db','')}.json"
        try:
            with open(os.path.join(self.folder_picks, filename), 'w') as f:
                json.dump(strategies, f, indent=2)
        except Exception as e:
            print(f"Save error: {e}")

    def run(self):
        for granularity in self.granularities:
            for hours in self.hourss:
                strategies = self.update_strategies(granularity, hours)
                if strategies:
                    self.save_file(strategies, hours, granularity)
            strategies = self.get_fix_count_strategies(granularity)
            if strategies:
                self.save_file2(strategies,granularity)
# if __name__ == "__main__":
#     arch = Architect('dbs/test_MOEX_FUT.db',(1,5),(1,4))
#     arch.run()