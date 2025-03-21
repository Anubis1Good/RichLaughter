import sqlite3
from datetime import datetime

# Создание базы данных и таблиц
conn = sqlite3.connect('trading_data.db')
cursor = conn.cursor()

# Таблица роботов
cursor.execute('''
CREATE TABLE IF NOT EXISTS robots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    strategy TEXT
)
''')

# Таблица сделок
cursor.execute('''
CREATE TABLE IF NOT EXISTS trades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    robot_id INTEGER,
    timestamp DATETIME,
    action TEXT,
    price REAL,
    volume REAL,
    instrument TEXT,
    commission REAL,
    indicators TEXT,
    FOREIGN KEY (robot_id) REFERENCES robots (id)
)
''')

# Таблица результатов (опционально, можно рассчитывать на лету)
cursor.execute('''
CREATE TABLE IF NOT EXISTS results (
    robot_id INTEGER PRIMARY KEY,
    total_profit REAL,
    total_commission REAL,
    net_profit REAL,
    FOREIGN KEY (robot_id) REFERENCES robots (id)
)
''')

conn.commit()

# Добавление робота
def add_robot(name, strategy):
    cursor.execute('''
    INSERT INTO robots (name, strategy) VALUES (?, ?)
    ''', (name, strategy))
    conn.commit()

# Добавление сделки
def add_trade(robot_id, action, price, volume, instrument, commission, indicators):
    cursor.execute('''
    INSERT INTO trades (robot_id, timestamp, action, price, volume, instrument, commission, indicators)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (robot_id, datetime.now(), action, price, volume, instrument, commission, str(indicators)))
    conn.commit()

# Расчет результатов для робота
def calculate_results(robot_id):
    # Считаем общую прибыль и комиссию
    cursor.execute('''
    SELECT 
        SUM(CASE WHEN action = 'sell' THEN price * volume ELSE -price * volume END) AS total_profit,
        SUM(commission) AS total_commission
    FROM trades
    WHERE robot_id = ?
    ''', (robot_id,))
    result = cursor.fetchone()
    total_profit = result[0] or 0
    total_commission = result[1] or 0
    net_profit = total_profit - total_commission

    # Обновляем или добавляем результаты
    cursor.execute('''
    INSERT OR REPLACE INTO results (robot_id, total_profit, total_commission, net_profit)
    VALUES (?, ?, ?, ?)
    ''', (robot_id, total_profit, total_commission, net_profit))
    conn.commit()

# Получение лучшего робота
def get_best_robot():
    cursor.execute('''
    SELECT robots.name, results.net_profit
    FROM results
    JOIN robots ON results.robot_id = robots.id
    ORDER BY results.net_profit DESC
    LIMIT 1
    ''')
    return cursor.fetchone()

# Пример использования
add_robot('Robot1', 'Strategy1')
add_robot('Robot2', 'Strategy2')

# Добавляем сделки для Robot1
add_trade(1, 'buy', 100, 10, 'BTC/USD', 0.1, {'rsi': 30, 'macd': 0.5})
add_trade(1, 'sell', 110, 10, 'BTC/USD', 0.1, {'rsi': 70, 'macd': 0.2})

# Добавляем сделки для Robot2
add_trade(2, 'buy', 200, 5, 'AAPL', 0.2, {'rsi': 40, 'macd': 0.3})
add_trade(2, 'sell', 210, 5, 'AAPL', 0.2, {'rsi': 60, 'macd': 0.1})

# Рассчитываем результаты
calculate_results(1)
calculate_results(2)

# Получаем лучшего робота
best_robot = get_best_robot()
print(f"Лучший робот: {best_robot[0]} с чистой прибылью: {best_robot[1]}")

# Закрытие соединения
conn.close()