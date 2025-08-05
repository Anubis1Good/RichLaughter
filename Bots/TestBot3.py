import os
import shutil
import sqlite3
import traceback
from datetime import datetime
from functools import wraps

def with_db_cursor(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not hasattr(self, 'conn'):
            raise AttributeError("У класса должно быть соединение conn!")
            
        cursor = self.conn.cursor()
        try:
            result = func(self, cursor, *args, **kwargs)
            self.conn.commit()
            return result
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()
            
    return wrapper

# def backup_sqlite_db(db_path, backup_dir='dbs/backups'):
#     """Создает резервную копию файла базы данных"""
#     if not os.path.exists(backup_dir):
#         os.makedirs(backup_dir)
    
#     timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
#     backup_path = os.path.join(backup_dir, f'{os.path.basename(db_path)}.bak_{timestamp}')
    
#     # Убедимся, что нет активных соединений
#     try:
#         # Копируем файл
#         shutil.copy2(db_path, backup_path)
#         return backup_path
#     except Exception as e:
#         print(f"Ошибка при создании резервной копии: {e}")
#         return None

def backup_sqlite_db(db_path, backup_dir='dbs/backups'):
    """Создает резервную копию файла базы данных в подпапке с именем БД"""
    try:
        # Получаем имя базы данных (без расширения)
        db_name = os.path.splitext(os.path.basename(db_path))[0]
        
        # Создаем путь к подпапке для этой БД
        db_backup_dir = os.path.join(backup_dir, db_name)
        
        # Создаем директорию, если ее нет (включая все родительские)
        os.makedirs(db_backup_dir, exist_ok=True)
        
        # Генерируем имя файла бэкапа с временной меткой
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f"{db_name}.bak_{timestamp}.db"
        backup_path = os.path.join(db_backup_dir, backup_filename)
        
        # Копируем файл
        shutil.copy2(db_path, backup_path)
        return backup_path
    except Exception as e:
        print(f"Ошибка при создании резервной копии: {e}")
        return None

class TestBot3:
    def __init__(self,db_path,fee,ticker,granularity,strategy,conf):
        self.ticker = ticker
        self.strategy = strategy
        self.granularity = granularity
        self.name = str(granularity) + '_' + str(self.strategy).split(' ')[0].split('.')[-1] + "_" + "_".join(list(map(str,conf)))
        self.db_path = db_path
        self.fee = fee
        if not os.path.exists('dbs'):
            os.mkdir('dbs')
        # if os.path.exists(self.db_path):
        #     backup_sqlite_db(self.db_path)
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("PRAGMA synchronous=NORMAL")
        self.conn.execute("PRAGMA cache_size=-10000") 
        self.init_db()
        self.robot_id = self.get_or_create_robot()
        self.ticker_id = self.get_or_create_ticker()
        self.pos = self.get_start_pos()

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()
    @with_db_cursor
    def init_db(self,cursor:sqlite3.Cursor):
        # Таблица роботов
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS robots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            granularity TEXT NOT NULL DEFAULT 1
        )
        ''')

        # Таблица тикеров
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
        ''')

        # Таблица position
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            robot_id INTEGER NOT NULL,
            ticker_id INTEGER NOT NULL,
            open_timestamp DATETIME NOT NULL,
            direction INTEGER NOT NULL,
            open_price REAL NOT NULL,
            UNIQUE(robot_id, ticker_id),
            FOREIGN KEY (robot_id) REFERENCES robots(id),
            FOREIGN KEY (ticker_id) REFERENCES tickers(id)
        )
        ''')

        # Таблица для хранения результатов
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS history_positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            robot_id INTEGER NOT NULL,
            ticker_id INTEGER NOT NULL,
            open_timestamp DATETIME NOT NULL,
            direction INTEGER NOT NULL,
            open_price REAL NOT NULL,
            close_timestamp DATETIME NOT NULL,
            close_price REAL NOT NULL,
            fee REAL DEFAULT 0,
            result REAL GENERATED ALWAYS AS ((close_price - open_price) * direction) STORED,
            result_fee REAL GENERATED ALWAYS AS (result - fee) STORED,
            FOREIGN KEY (robot_id) REFERENCES robots(id),
            FOREIGN KEY (ticker_id) REFERENCES tickers(id)
        )
        ''')


        # Создание индексов для таблицы robots
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_robots_name_granularity ON robots(name,granularity)')

        # Создание индексов для таблицы tickers
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_tickers_name ON tickers(name)')

        # Создание индексов для таблицы positions
        cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_positions_robot_ticker 
        ON positions(robot_id, ticker_id)
        ''')


        # Создание индексов для таблицы history_positions

        cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_history_robot_ticker_time 
        ON history_positions(robot_id, ticker_id, open_timestamp)
        ''')



    @with_db_cursor
    def get_or_create_robot(self,cursor:sqlite3.Cursor):
        """Получаем или создаем робота (гарантия уникальности по name)"""
        try:
            cursor.execute(
                'INSERT INTO robots (name, granularity) VALUES (?,?)',
                (self.name,self.granularity)
            )
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            # Робот уже существует, просто возвращаем его ID
            cursor.execute(
                'SELECT id FROM robots WHERE name = ?', 
                (self.name,)
            )
            return cursor.fetchone()[0]

    @with_db_cursor
    def get_or_create_ticker(self,cursor:sqlite3.Cursor):
        """Получаем или создаем тикер (гарантия уникальности по name + fut)"""
        try:
            cursor.execute(
                'INSERT INTO tickers (name) VALUES (?)',
                (self.ticker,)
            )
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            # Тикер уже существует, возвращаем его ID
            cursor.execute(
                'SELECT id FROM tickers WHERE name = ?',
                (self.ticker,)
            )
            return cursor.fetchone()[0]
    
    
    # @with_db_cursor
    def upsert_position(self, cursor: sqlite3.Cursor, direction: int, open_price: float):
        if direction == 0:
            # Удаляем позицию, если direction == 0
            cursor.execute('''
            DELETE FROM positions 
            WHERE robot_id = ? AND ticker_id = ?
            ''', (self.robot_id, self.ticker_id))
        else:
            # Вставляем или обновляем позицию
            cursor.execute('''
            INSERT INTO positions 
            (robot_id, ticker_id, open_timestamp, direction, open_price)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(robot_id, ticker_id) DO UPDATE SET
                open_timestamp = excluded.open_timestamp,
                direction = excluded.direction,
                open_price = excluded.open_price
            ''', (self.robot_id, self.ticker_id, datetime.now(), direction, open_price))
        self.pos = direction

    @with_db_cursor
    def get_start_pos(self, cursor: sqlite3.Cursor):
        cursor.execute('''
        SELECT  direction
        FROM positions 
        WHERE robot_id = ? AND ticker_id = ?
        ''', (self.robot_id, self.ticker_id))
        
        pos = cursor.fetchone()
        if not pos:
            direction = 0
        else:
            direction = pos[0]
        return int(direction)

    @with_db_cursor
    def process_single_position(self,cursor: sqlite3.Cursor, new_direction, price):
        """Обрабатывает позицию и добавляет результаты к существующим"""
        # 1. Получаем данные позиции
        cursor.execute('''
        SELECT  open_timestamp, direction, open_price
        FROM positions 
        WHERE robot_id = ? AND ticker_id = ?
        ''', (self.robot_id, self.ticker_id))
        
        pos = cursor.fetchone()
        if not pos:
            open_timestamp,direction, open_price = 0,0,0
        else:
            open_timestamp,direction, open_price = pos
        
        if direction == new_direction:
            return
        # Пропускаем если direction = 0
        if direction == 0:
            self.upsert_position(cursor,new_direction,price)
            return

        # 2. Расчет новых результатов
        fee = self.fee *(price + open_price)

        current_time = datetime.now()

        
        # 6. Сохраняем (UPSERT)
        cursor.execute('''
        INSERT INTO history_positions 
        (robot_id, ticker_id, open_timestamp,direction,open_price,close_timestamp, close_price,fee)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            self.robot_id, 
            self.ticker_id,
            open_timestamp,
            direction,
            open_price,
            current_time,
            price,
            fee
        ))
        self.upsert_position(cursor,new_direction,price)

    def trade_next(self,action,row):
        if not action:
            return
        price = float(row['close'])  # Явное преобразование к float
        if 'close_long' in action:
            if self.pos == 1:
                self.process_single_position(0, price)
        elif 'close_short' in action:
            if self.pos == -1:
                self.process_single_position(0, price)
        elif 'long' in action:
            if self.pos != 1:
                self.process_single_position(1, price)
        elif 'short' in action:
            if self.pos != -1:
                self.process_single_position(-1, price)
        elif 'close_all' in action:
            if self.pos != 0:
                self.process_single_position(0, price)

    def cancel_trade(self,df):
        try:
            price = float(df.iloc[-1]['close'])
            self.process_single_position(0,price)
        except Exception as err:
            print(self.ticker,self.name)
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
            print(self.ticker,self.name)
            traceback.print_exc()

class TestBot4(TestBot3):
    def __init__(self, db_path, fee, ticker, granularity, strategy, conf):
        super().__init__(db_path, fee, ticker, granularity, strategy, conf)
        self.order = None
    def trade_next(self, action, row):
        # work order
        if self.order:
            price = self.order[1]
            if self.order[0] == 2: #long
                if row['low'] < price:
                    self.process_single_position(1, price)
                    self.order = None
            elif self.order[0] == -2: #short
                if row['high'] > price:
                    self.process_single_position(-1, price)
                    self.order = None
            elif self.order[0] == 1: #close_long
                if row['high'] > price:
                    self.process_single_position(0, price)
                    self.order = None
            elif self.order[0] == -1: #close_short
                if row['low'] < price:
                    self.process_single_position(0, price)
                    self.order = None
            else: #close_all
                if self.pos == 1:
                    if row['high'] > price:
                        self.process_single_position(0, price)
                        self.order = None
                elif self.pos == -1:
                    if row['low'] < price:
                        self.process_single_position(0, price)
                        self.order = None                   
        # work action
        if not action:
            return
        price = float(row['close'])  # Явное преобразование к float
        if 'close_long' in action:
            if self.pos == 1:
                self.order = (1,price)
        elif 'close_short' in action:
            if self.pos == -1:
                self.order = (-1,price)
        elif 'long' in action:
            if self.pos != 1:
                self.order = (2,price)
        elif 'short' in action:
            if self.pos != -1:
                self.order = (-2,price)
        elif 'close_all' in action:
            if self.pos != 0:
                self.order = (0,price)