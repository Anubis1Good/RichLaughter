import os
import shutil
import io
import sqlite3
import traceback
import numpy as np
import zlib
import json
from datetime import datetime
from functools import wraps

def with_db_cursor(func):
    """Декоратор для методов класса, ожидающий self.db_cursor"""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not hasattr(self, 'db_path'):
            self.db_path = 'dbs/trading_system.db'  # Значение по умолчанию
            
        conn = sqlite3.connect(self.db_path)
        self.db_cursor = conn.cursor()
        
        try:
            result = func(self, *args, **kwargs)
            conn.commit()
            return result
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            self.db_cursor.close()
            conn.close()
            # del self.db_cursor
    return wrapper

def backup_sqlite_db(db_path, backup_dir='dbs/backups'):
    """Создает резервную копию файла базы данных"""
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = os.path.join(backup_dir, f'{os.path.basename(db_path)}.bak_{timestamp}')
    
    # Убедимся, что нет активных соединений
    try:
        # Копируем файл
        shutil.copy2(db_path, backup_path)
        return backup_path
    except Exception as e:
        print(f"Ошибка при создании резервной копии: {e}")
        return None


class TestBot2:
    def __init__(self,db_path,fee,ticker,granularity,strategy,conf):
        self.ticker = ticker
        self.strategy = strategy
        self.name = str(granularity) + '_' + str(self.strategy).split(' ')[0].split('.')[-1] + "_" + "_".join(list(map(str,conf)))
        self.db_path = db_path
        self.fee = fee
        self.db_cursor:sqlite3.Cursor = None
        if not os.path.exists('dbs'):
            os.mkdir('dbs')
        if os.path.exists(self.db_path):
            backup_sqlite_db(self.db_path)
        self.init_db()
        self.robot_id = self.get_or_create_robot()
        self.ticker_id = self.get_or_create_ticker()
        self.pos = self.get_start_pos()

        
    @with_db_cursor
    def init_db(self):
        # Таблица роботов
        self.db_cursor.execute('''
        CREATE TABLE IF NOT EXISTS robots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
        ''')

        # Таблица тикеров
        self.db_cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
        ''')

        # Таблица position
        self.db_cursor.execute('''
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            robot_id INTEGER NOT NULL,
            ticker_id INTEGER NOT NULL,
            open_timestamp DATETIME NOT NULL,
            direction INTEGER NOT NULL,
            open_price REAL NOT NULL,
            fee REAL DEFAULT 0,
            UNIQUE(robot_id, ticker_id),
            FOREIGN KEY (robot_id) REFERENCES robots(id),
            FOREIGN KEY (ticker_id) REFERENCES tickers(id)
        )
        ''')

        # Таблица для хранения результатов
        self.db_cursor.execute('''
        CREATE TABLE IF NOT EXISTS robot_ticker_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            robot_id INTEGER NOT NULL,
            ticker_id INTEGER NOT NULL,
            timestamp DATETIME NOT NULL, 
            results_with_fee BLOB NOT NULL,
            results_without_fee BLOB NOT NULL, 
            UNIQUE(robot_id, ticker_id),
            FOREIGN KEY (robot_id) REFERENCES robots(id),
            FOREIGN KEY (ticker_id) REFERENCES tickers(id)
        )
        ''')
        self.db_cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_positions_robot_ticker 
        ON positions(robot_id, ticker_id)
        ''')
        self.db_cursor.execute('CREATE INDEX IF NOT EXISTS idx_robots_name ON robots(name)')
        self.db_cursor.execute('CREATE INDEX IF NOT EXISTS idx_tickers_name ON tickers(name)')
        self.db_cursor.execute('CREATE INDEX IF NOT EXISTS idx_positions_robot ON positions(robot_id)')
        self.db_cursor.execute('CREATE INDEX IF NOT EXISTS idx_positions_ticker ON positions(ticker_id)')

    @with_db_cursor
    def get_or_create_robot(self):
        """Получаем или создаем робота (гарантия уникальности по name)"""
        try:
            self.db_cursor.execute(
                'INSERT INTO robots (name) VALUES (?)',
                (self.name,)
            )
            return self.db_cursor.lastrowid
        except sqlite3.IntegrityError:
            # Робот уже существует, просто возвращаем его ID
            self.db_cursor.execute(
                'SELECT id FROM robots WHERE name = ?', 
                (self.name,)
            )
            return self.db_cursor.fetchone()[0]

    @with_db_cursor
    def get_or_create_ticker(self):
        """Получаем или создаем тикер (гарантия уникальности по name + fut)"""
        try:
            self.db_cursor.execute(
                'INSERT INTO tickers (name) VALUES (?)',
                (self.ticker,)
            )
            return self.db_cursor.lastrowid
        except sqlite3.IntegrityError:
            # Тикер уже существует, возвращаем его ID
            self.db_cursor.execute(
                'SELECT id FROM tickers WHERE name = ?',
                (self.ticker,)
            )
            return self.db_cursor.fetchone()[0]
    
    # def save_results(self,results: np.ndarray) -> bytes:
    #     buffer = io.BytesIO()
    #     np.save(buffer, results, allow_pickle=False)
    #     return zlib.compress(buffer.getvalue())

    # def load_results(self,blob: bytes) -> np.ndarray:
    #     buffer = io.BytesIO(zlib.decompress(blob))
    #     return np.load(buffer, allow_pickle=False)
    
    # @with_db_cursor
    def upsert_position(self, direction, open_price):
        self.db_cursor.execute('''
        INSERT INTO positions 
        (robot_id, ticker_id, open_timestamp, direction, open_price, fee)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(robot_id, ticker_id) DO UPDATE SET
            open_timestamp = excluded.open_timestamp,
            direction = excluded.direction,
            open_price = excluded.open_price,
            fee = excluded.fee
        ''', (self.robot_id, self.ticker_id, datetime.now(), direction, open_price, self.fee))

    @with_db_cursor
    def get_start_pos(self):
        self.db_cursor.execute('''
        SELECT  direction, open_price, fee 
        FROM positions 
        WHERE robot_id = ? AND ticker_id = ?
        ''', (self.robot_id, self.ticker_id))
        
        pos = self.db_cursor.fetchone()
        if not pos:
            self.upsert_position(0,0)
            direction, open_price, fee = 0,0,0
        else:
            direction, open_price, fee = pos
        return int(direction)

    @with_db_cursor
    def process_single_position(self, new_direction, price):
        """Обрабатывает позицию и добавляет результаты к существующим"""
        # 1. Получаем данные позиции
        self.db_cursor.execute('''
        SELECT  direction, open_price, fee 
        FROM positions 
        WHERE robot_id = ? AND ticker_id = ?
        ''', (self.robot_id, self.ticker_id))
        
        pos = self.db_cursor.fetchone()
        if not pos:
            self.upsert_position(0,0.0)
            direction, open_price, fee = 0,0,0
        else:
            direction, open_price, fee = pos
        
        # Пропускаем если direction = 0
        if direction == new_direction:
            return
        if direction == 0:
            self.upsert_position(new_direction,price)
            return

        # 2. Расчет новых результатов
        new_pnl_with_fee = direction * (price - open_price) - fee*(open_price + price)
        new_pnl_without_fee = direction * (price - open_price)
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 3. Получаем предыдущие результаты (если есть)
        self.db_cursor.execute('''
        SELECT results_with_fee, results_without_fee 
        FROM robot_ticker_results 
        WHERE robot_id = ? AND ticker_id = ?
        ''', (self.robot_id, self.ticker_id))
        
        existing_results = self.db_cursor.fetchone()
        
                    
        if existing_results:
            # Десериализуем существующие данные
            existing_with_fee = json.loads(existing_results[0].decode('utf-8'))
            existing_without_fee = json.loads(existing_results[1].decode('utf-8'))
        else:
            # Если записей нет - создаем пустые списки
            existing_with_fee = []
            existing_without_fee = []
        
        # Обновляем результаты
        updated_with_fee = existing_with_fee + [new_pnl_with_fee]
        updated_without_fee = existing_without_fee + [new_pnl_without_fee]
        # print(updated_with_fee)
        # 5. Сериализация с сжатием

        results_with_fee_blob = json.dumps(updated_with_fee).encode('utf-8')
        results_without_fee_blob = json.dumps(updated_without_fee).encode('utf-8')
        
        # 6. Сохраняем (UPSERT)
        self.db_cursor.execute('''
        INSERT INTO robot_ticker_results 
        (robot_id, ticker_id, timestamp, results_with_fee, results_without_fee)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(robot_id, ticker_id) DO UPDATE SET
            timestamp = excluded.timestamp,
            results_with_fee = excluded.results_with_fee,
            results_without_fee = excluded.results_without_fee
        ''', (
            self.robot_id, 
            self.ticker_id,
            current_time,
            results_with_fee_blob,
            results_without_fee_blob
        ))
        self.upsert_position(new_direction,price)

    def trade_next(self,action,row):
        if not action:
            return
        price = float(row['close'])  # Явное преобразование к float
        
        if 'close_long' in action and self.pos == 1:
            self.process_single_position(0, price)
        elif 'close_short' in action and self.pos == -1:
            self.process_single_position(0, price)
        elif 'long' in action and self.pos != 1:
            self.process_single_position(1, price)
        elif 'short' in action and self.pos != -1:
            self.process_single_position(-1, price)
        elif 'close_all' in action and self.pos != 0:
            self.process_single_position(0, price)

    def cancel_trade(self,df):
        try:
            price = df.iloc[-1]['close']
            self.process_single_position(0,price)
        except Exception as err:
            traceback.print_exc()

    def run(self,df):
        try:
            row = self.strategy.get_test_row(df)
            action = self.strategy(row)
            # print("+++++++++++++++++")
            # print(row)
            # print(action)
            # print("+++++++++++++++++")
            self.trade_next(action,row)
        except Exception as err:
            traceback.print_exc()