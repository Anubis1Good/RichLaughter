import sqlite3
import pandas as pd
from datetime import datetime,timedelta

def get_top5_alltime_tickers_by_granularity(db_path,granularity):
    conn = sqlite3.connect(db_path)
    query = """
        WITH ranked_results AS (
            SELECT 
                r.name AS bot,
                t.name AS ticker,
                r.granularity AS granularity,
                AVG(hp.close_price) AS avg_close_price,
                SUM(hp.fee) AS total_fee,
                SUM(hp.result) AS total_result,
                COUNT(*) AS total_trades,
                SUM(hp.result_fee) AS total_result_fee,
                ROW_NUMBER() OVER (PARTITION BY t.name ORDER BY SUM(hp.result_fee) DESC) AS rank
            FROM 
                history_positions hp
            JOIN 
                robots r ON hp.robot_id = r.id
            JOIN 
                tickers t ON hp.ticker_id = t.id
            WHERE 
                r.granularity = ?
            GROUP BY 
                r.name, t.name, r.granularity
        )
        SELECT 
            bot,
            ticker,
            granularity,
            avg_close_price,
            total_fee,
            total_result,
            total_trades,
            total_result_fee
        FROM 
            ranked_results
        WHERE 
            rank <= 5
        ORDER BY 
            ticker, rank;
        """
    result = pd.read_sql_query(query, conn,params=(granularity,))
    conn.close()

    return result


def get_top5_today_tickers_by_granularity(db_path,granularity):
    # Получаем сегодняшнюю дату в UTC
    today = datetime.now().date()
    conn = sqlite3.connect(db_path)
    query = """
    WITH ranked_results AS (
        SELECT 
            r.name AS bot,
            t.name AS ticker,
            r.granularity,
            AVG(hp.close_price) AS avg_close_price,
            SUM(hp.fee) AS total_fee,
            SUM(hp.result) AS total_result,
            COUNT(*) AS total_trades,
            SUM(hp.result_fee) AS total_result_fee,
            ROW_NUMBER() OVER (PARTITION BY t.name ORDER BY SUM(hp.result_fee) DESC) AS rank
        FROM history_positions hp
        JOIN robots r ON hp.robot_id = r.id
        JOIN tickers t ON hp.ticker_id = t.id
        WHERE r.granularity = ?
          AND date(hp.close_timestamp) = ?
        GROUP BY r.name, t.name, r.granularity
    )
    SELECT 
        bot, ticker, granularity, avg_close_price,
        total_fee, total_result, total_trades, total_result_fee
    FROM ranked_results
    WHERE rank <= 5
    ORDER BY ticker, rank;
    """
    
    result = pd.read_sql(query, conn, params=(granularity, today))
    conn.close()

    return result


def get_top5_hour_tickers_by_granularity(db_path,granularity):
    # Получаем сегодняшнюю дату в UTC
    conn = sqlite3.connect(db_path)
    now = datetime.now()
    one_hour_ago = now - timedelta(hours=1)
    
    query = """
    WITH ranked_results AS (
        SELECT 
            r.name AS bot,
            t.name AS ticker,
            r.granularity,
            AVG(hp.close_price) AS avg_close_price,
            SUM(hp.fee) AS total_fee,
            SUM(hp.result) AS total_result,
            COUNT(*) AS total_trades,
            SUM(hp.result_fee) AS total_result_fee,
            ROW_NUMBER() OVER (PARTITION BY t.name ORDER BY SUM(hp.result_fee) DESC) AS rank
        FROM history_positions hp
        JOIN robots r ON hp.robot_id = r.id
        JOIN tickers t ON hp.ticker_id = t.id
        WHERE r.granularity = ?
          AND hp.close_timestamp >= ?
        GROUP BY r.name, t.name, r.granularity
    )
    SELECT 
        bot, ticker, granularity, avg_close_price,
        total_fee, total_result, total_trades, total_result_fee
    FROM ranked_results
    WHERE rank <= 5
    ORDER BY ticker, rank;
    """
    result = pd.read_sql(query, conn, params=(granularity, one_hour_ago))
    conn.close()

    return result

def get_best_strategies(db_path, granularity='1h', lookback_hours=1):
    """
    Возвращает лучшие стратегии с интеллектуальным рейтингом:
    - Исключает роботов с отрицательной прибылью
    - Баланс между прибылью, количеством сделок и стабильностью
    - Учитывает среднюю прибыль на сделку
    
    Параметры:
        db_path: путь к БД SQLite
        granularity: таймфрейм стратегии
        lookback_hours: за сколько часов анализировать
        
    Возвращает:
        DataFrame с лучшими стратегиями и метриками
    """
    time_threshold = datetime.now() - timedelta(hours=lookback_hours)
    
    # Запрос для получения базовых статистик
    # query = """
    # SELECT 
    #     r.name AS bot,
    #     t.name AS ticker,
    #     r.granularity,
    #     SUM(hp.result_fee) AS total_result_fee,
    #     COUNT(*) AS total_trades,
    #     AVG(hp.result_fee) AS avg_result_per_trade
    # FROM history_positions hp
    # JOIN robots r ON hp.robot_id = r.id
    # JOIN tickers t ON hp.ticker_id = t.id
    # WHERE r.granularity = ?
    #   AND hp.close_timestamp >= ?
    # GROUP BY r.name, t.name, r.granularity
    # HAVING COUNT(*) >= 3  -- Минимум 3 сделки
    # """
    query = """
    SELECT 
        r.name AS bot,
        t.name AS ticker,
        r.granularity,
        SUM(hp.result_fee) AS total_result_fee,
        COUNT(*) AS total_trades,
        AVG(hp.result_fee) AS avg_result_per_trade
    FROM history_positions hp
    JOIN robots r ON hp.robot_id = r.id
    JOIN tickers t ON hp.ticker_id = t.id
    WHERE r.granularity = ?
      AND hp.close_timestamp >= ?
      AND r.name NOT LIKE '%SKYNET%'
    GROUP BY r.name, t.name, r.granularity
    HAVING COUNT(*) >= 3
    ORDER BY total_result_fee DESC
    """
    with sqlite3.connect(db_path) as conn:
        df = pd.read_sql(query, conn, params=(granularity, time_threshold))
    
    if df.empty:
        return pd.DataFrame()
    
    # 1. Исключаем роботов с отрицательным результатом
    df = df[df['total_result_fee'] > 0]
    
    if df.empty:
        return pd.DataFrame()
    
    # 2. Рассчитываем дополнительные метрики
    # df['profit_per_trade'] = df['total_result_fee'] / df['total_trades']
    
    # # 3. Нормализуем метрики (приводим к шкале 0-1)
    # metrics = {
    #     'total_result_fee': 0.6,    # Общая прибыль (важна, но не главное)
    #     'profit_per_trade': 0.4,    # Прибыль на сделку (важнее общей)
    #     'total_trades': 0         # Количество сделок (менее важно)
    # }
    
    # for col in metrics:
    #     df[f'norm_{col}'] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())
    
    # # 4. Композитный рейтинг с приоритетом на качество сделок
    # df['composite_score'] = sum(
    #     weight * df[f'norm_{col}'] 
    #     for col, weight in metrics.items()
    # )
    
    # 5. Выбираем лучшего робота для каждого тикера
    try:
        best_strategies = df.dropna(subset=['total_result_fee'])\
                    .loc[df.groupby('ticker')['total_result_fee'].idxmax()]
        
        return best_strategies.sort_values('total_result_fee', ascending=False)
        # best_strategies = df.dropna(subset=['composite_score'])\
        #             .loc[df.groupby('ticker')['composite_score'].idxmax()]
        
        # return best_strategies.sort_values('composite_score', ascending=False)
    except:
        return pd.DataFrame()