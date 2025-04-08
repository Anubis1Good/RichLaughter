import sqlite3
import pandas as pd
from datetime import datetime,timedelta
import numpy as np
from sklearn.preprocessing import RobustScaler

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
    time_threshold = datetime.now() - timedelta(hours=lookback_hours)
    
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

    # 5. Выбираем лучшего робота для каждого тикера
    try:
        best_strategies = df.dropna(subset=['total_result_fee'])\
                    .loc[df.groupby('ticker')['total_result_fee'].idxmax()]
        
        return best_strategies.sort_values('total_result_fee', ascending=False)
    except:
        return pd.DataFrame()
    

def get_best_strategies_v2(db_path, granularity='1h', lookback_hours=24):
    time_threshold = datetime.now() - timedelta(hours=lookback_hours)
    
    query = """
    SELECT 
        r.name AS bot,
        t.name AS ticker,
        r.granularity,
        SUM(hp.result_fee) AS total_result_fee,
        COUNT(*) AS total_trades,
        AVG(hp.result_fee) AS avg_result_per_trade,
        JULIANDAY(NOW()) - JULIANDAY(MAX(hp.close_timestamp)) AS last_trade_recency
    FROM history_positions hp
    JOIN robots r ON hp.robot_id = r.id
    JOIN tickers t ON hp.ticker_id = t.id
    WHERE r.granularity = ?
      AND hp.close_timestamp >= ?
      AND r.name NOT LIKE '%SKYNET%'
    GROUP BY r.name, t.name, r.granularity
    HAVING total_trades >= 5 AND avg_result_per_trade > 0
    ORDER BY total_result_fee DESC
    """
    
    with sqlite3.connect(db_path) as conn:
        df = pd.read_sql(query, conn, params=(granularity, time_threshold))
    
    if df.empty:
        return pd.DataFrame()

    # Расчет комплексного показателя эффективности
    df['recent_weight'] = 1 / (1 + df['last_trade_recency'])  # Вес для свежих сделок
    df['activity_score'] = np.log1p(df['total_trades'])      # Логарифмирование для нормализации
    
    # Нормализация показателей
    metrics = ['total_result_fee', 'avg_result_per_trade', 'activity_score', 'recent_weight']
    df[metrics] = df[metrics].apply(lambda x: (x - x.min()) / (x.max() - x.min()))
    
    # Итоговый score с весами: 40% прибыль, 30% стабильность, 20% активность, 10% свежесть
    df['score'] = (0.4 * df['total_result_fee'] +
                   0.3 * df['avg_result_per_trade'] +
                   0.2 * df['activity_score'] +
                   0.1 * df['recent_weight'])
    
    try:
        # Выбираем по 2 лучших стратегии на тикер для резервирования
        best_strategies = df.groupby('ticker').apply(
            lambda x: x.nlargest(2, 'score')
        ).reset_index(drop=True)
        
        return best_strategies.sort_values(['ticker', 'score'], ascending=[True, False])
    except Exception as e:
        print(f"Error in strategy selection: {e}")
        return pd.DataFrame()
    
def get_best_strategies_v3(db_path, granularity='1h', lookback_hours=24):
    try:
        time_threshold = datetime.now() - timedelta(hours=lookback_hours)
        time_threshold_str = time_threshold.strftime('%Y-%m-%d %H:%M:%S')
        
        query = """
        SELECT 
            r.name AS bot,
            t.name AS ticker,
            r.granularity,
            SUM(hp.result_fee) AS total_result_fee,
            COUNT(*) AS total_trades,
            AVG(hp.result_fee) AS avg_result_per_trade,
            JULIANDAY(datetime('now')) - JULIANDAY(MAX(hp.close_timestamp)) AS last_trade_recency,
            MAX(hp.close_timestamp) AS last_trade_time
        FROM history_positions hp
        JOIN robots r ON hp.robot_id = r.id
        JOIN tickers t ON hp.ticker_id = t.id
        WHERE r.granularity = ?
          AND hp.close_timestamp >= ?
          AND r.name NOT LIKE '%SKYNET%'
        GROUP BY r.name, t.name, r.granularity
        HAVING total_trades >= 5 AND avg_result_per_trade > 0
        """
        
        with sqlite3.connect(db_path) as conn:
            df = pd.read_sql(query, conn, params=(granularity, time_threshold_str))
            
        # Всегда возвращаем DataFrame, даже при ошибках расчета
        if df.empty:
            return pd.DataFrame()

        try:
            df['recent_weight'] = 1 / (1 + df['last_trade_recency'])
            df['activity_score'] = np.log1p(df['total_trades'])
            metrics = ['total_result_fee', 'avg_result_per_trade', 'activity_score', 'recent_weight']
            df[metrics] = df[metrics].apply(lambda x: (x - x.min()) / (x.max() - x.min() + 1e-6))
            df['score'] = 0.4*df['total_result_fee'] + 0.3*df['avg_result_per_trade'] + 0.2*df['activity_score'] + 0.1*df['recent_weight']
            
            best_strategies = df.loc[df.groupby('ticker')['score'].idxmax()].reset_index(drop=True)
            return best_strategies.sort_values('score', ascending=False)
            
        except Exception as e:
            print(f"Metric calculation failed: {e}")
            return pd.DataFrame([], columns=['bot', 'ticker'])  # Возвращаем DataFrame с ожидаемыми колонками
            
    except Exception as e:
        print(f"Critical error in get_best_strategies_v3: {e}")
        return pd.DataFrame()
    
def get_best_strategies_v4(db_path, granularity='1h', lookback_hours=24):
    try:
        time_threshold = datetime.now() - timedelta(hours=lookback_hours)
        time_threshold_str = time_threshold.strftime('%Y-%m-%d %H:%M:%S')
        
        query = """
        WITH strategy_stats AS (
            SELECT 
                r.name AS bot,
                t.name AS ticker,
                r.granularity,
                SUM(hp.result_fee) AS total_result_fee,
                COUNT(*) AS total_trades,
                AVG(hp.result_fee) AS avg_result_per_trade,
                JULIANDAY(datetime('now')) - JULIANDAY(MAX(hp.close_timestamp)) AS last_trade_recency,
                MAX(hp.close_timestamp) AS last_trade_time,
                -- Ручной расчет стандартного отклонения
                SQRT(
                    AVG(hp.result_fee * hp.result_fee) - 
                    AVG(hp.result_fee) * AVG(hp.result_fee)
                ) AS result_stddev
            FROM history_positions hp
            JOIN robots r ON hp.robot_id = r.id
            JOIN tickers t ON hp.ticker_id = t.id
            WHERE r.granularity = ?
              AND hp.close_timestamp >= ?
              AND r.name NOT LIKE '%SKYNET%'
            GROUP BY r.name, t.name, r.granularity
            HAVING total_trades >= 5 AND avg_result_per_trade > 0
        )
        SELECT *,
            -- Защита от деления на ноль
            CASE 
                WHEN result_stddev < 1e-6 THEN total_result_fee 
                ELSE total_result_fee / result_stddev 
            END AS risk_adjusted_return,
            -- Новый балансированный score
            (avg_result_per_trade * 0.7 + 
             total_result_fee * 0.1 + 
             (1.0 / (1.0 + last_trade_recency)) * 0.2) AS balanced_score
        FROM strategy_stats
        ORDER BY balanced_score DESC
        """
        
        with sqlite3.connect(db_path) as conn:
            df = pd.read_sql(query, conn, params=(granularity, time_threshold_str))
            
        if df.empty:
            return pd.DataFrame()

        try:
            # Фильтр для исключения аномалий
            df = df[
                (df['total_trades'] <= df['total_trades'].quantile(0.9)) &
                (df['result_stddev'] > 1e-6)
            ]
            
            # Нормализация с использованием логарифма для сделок
            df['trade_count_norm'] = np.log1p(df['total_trades']) / np.log(2)
            df['recency_norm'] = 1 / (1 + df['last_trade_recency'])
            
            # Итоговый score
            df['score'] = (
                0.6 * df['avg_result_per_trade'] +
                0.2 * df['risk_adjusted_return'] +
                0.1 * df['trade_count_norm'] +
                0.1 * df['recency_norm']
            )
            
            best_strategies = df.loc[df.groupby('ticker')['score'].idxmax()]
            return best_strategies.sort_values('score', ascending=False)
            
        except Exception as e:
            print(f"Metric calculation error: {e}")
            return pd.DataFrame(columns=['bot', 'ticker'])
            
    except Exception as e:
        print(f"Critical error: {e}")
        return pd.DataFrame()
    
def get_best_strategies_v5(db_path, granularity='1h', lookback_deals=30):
    """
    Выбирает стратегии на основе последних N сделок
    :param lookback_deals: количество последних сделок для анализа (по умолчанию 30)
    """
    # lookback_deals *= 5
    try:
        query = f"""
        WITH ranked_trades AS (
            SELECT 
                r.name AS bot,
                t.name AS ticker,
                hp.result_fee,
                hp.close_timestamp,
                ROW_NUMBER() OVER (
                    PARTITION BY r.name, t.name 
                    ORDER BY hp.close_timestamp DESC
                ) AS trade_num
            FROM history_positions hp
            JOIN robots r ON hp.robot_id = r.id
            JOIN tickers t ON hp.ticker_id = t.id
            WHERE r.granularity = ?
              AND r.name NOT LIKE '%SKYNET%'
        ),
        last_n_trades AS (
            SELECT *
            FROM ranked_trades
            WHERE trade_num <= ?
        )
        SELECT
            bot,
            ticker,
            COUNT() AS total_trades,
            AVG(result_fee) AS avg_result_per_trade,
            SUM(result_fee) AS total_result_fee,
            MAX(close_timestamp) AS last_trade_time,
            -- Ручной расчет стандартного отклонения
            SQRT(AVG(result_fee*result_fee) - AVG(result_fee)*AVG(result_fee)) AS result_stddev
        FROM last_n_trades
        GROUP BY bot, ticker
        HAVING total_trades >= ? * 0.7  -- Минимум 70% от требуемого количества сделок
           AND avg_result_per_trade > 0
        """
        
        with sqlite3.connect(db_path) as conn:
            df = pd.read_sql(query, conn, params=(granularity, lookback_deals, lookback_deals))
            
        if df.empty:
            return pd.DataFrame()

        try:
            # Расчет ключевых метрик
            df['risk_adjusted_return'] = df['total_result_fee'] / (df['result_stddev'] + 1e-6)
            df['recency_norm'] = 1 / (1 + (datetime.now() - pd.to_datetime(df['last_trade_time'])).dt.total_seconds()/86400)
            
            # Нормализация через Z-score (исключаем влияние абсолютных значений)
            metrics = ['avg_result_per_trade', 'risk_adjusted_return', 'recency_norm']
            df[metrics] = df[metrics].apply(lambda x: (x - x.mean()) / x.std())
            
            # Итоговый score (только стабильность и риск)
            df['score'] = (
                0.6 * df['avg_result_per_trade'] + 
                0.3 * df['risk_adjusted_return'] + 
                0.1 * df['recency_norm']
            )
            
            best_strategies = df.loc[df.groupby('ticker')['score'].idxmax()]
            return best_strategies.sort_values('score', ascending=False)
            
        except Exception as e:
            # print(f"Metric calculation error: {e}")
            return pd.DataFrame(columns=['bot', 'ticker'])
            
    except Exception as e:
        print(f"Critical error: {e}")
        return pd.DataFrame()

def get_best_strategies_v6(db_path, granularity='1h', lookback_deals=30):
    """
    Выбирает стратегии с высоким процентом выигрышей и часовой доходностью
    :param lookback_deals: количество последних сделок для анализа
    """
    try:
        query = f"""
        WITH ranked_trades AS (
            SELECT 
                r.name AS bot,
                t.name AS ticker,
                hp.result_fee,
                hp.close_timestamp,
                ROW_NUMBER() OVER (
                    PARTITION BY r.name, t.name 
                    ORDER BY hp.close_timestamp DESC
                ) AS trade_num
            FROM history_positions hp
            JOIN robots r ON hp.robot_id = r.id
            JOIN tickers t ON hp.ticker_id = t.id
            WHERE r.granularity = ?
              AND r.name NOT LIKE '%SKYNET%'
        ),
        last_n_trades AS (
            SELECT *,
                CASE WHEN result_fee > 0 THEN 1 ELSE 0 END AS is_win
            FROM ranked_trades
            WHERE trade_num <= ?
        )
        SELECT
            bot,
            ticker,
            COUNT() AS total_trades,
            AVG(result_fee) AS avg_result,
            SUM(result_fee) AS total_result,
            MAX(close_timestamp) AS last_trade_time,
            -- Исправленные метрики
            AVG(is_win) * 100 AS win_rate,
            SUM(result_fee) / (
                (JULIANDAY(MAX(close_timestamp)) - JULIANDAY(MIN(close_timestamp))) * 24
            ) AS hourly_return,
            SQRT(AVG(result_fee*result_fee) - AVG(result_fee)*AVG(result_fee)) AS variance
        FROM last_n_trades
        GROUP BY bot, ticker
        HAVING total_trades >= ? * 0.7
        AND hourly_return > 0
        AND win_rate >= 50
        """
        
        with sqlite3.connect(db_path) as conn:
            df = pd.read_sql(query, conn, 
                            params=(granularity, lookback_deals, lookback_deals))
            
        if df.empty:
            return pd.DataFrame()

        # Нормализация метрик
        metrics = ['win_rate', 'hourly_return', 'avg_result']
        df[metrics] = df[metrics].apply(lambda x: (x - x.mean()) / x.std())
        
        # Итоговый score с приоритетом на win rate и часовую доходность
        df['score'] = (
            0.5 * df['win_rate'] + 
            0.3 * df['hourly_return'] +
            0.2 * df['avg_result']
        )
        
        
        best_strategies = df.loc[df.groupby('ticker')['score'].idxmax()]
        
        return best_strategies.sort_values(['ticker', 'score'], ascending=[True, False])

    except Exception as e:
        print(f"Error: {str(e)}")
        return pd.DataFrame()

def get_best_strategies_stable(db_path, granularity='1h', lookback_hours=24):
    try:
        time_threshold = datetime.now() - timedelta(hours=lookback_hours)
        time_threshold_str = time_threshold.strftime('%Y-%m-%d %H:%M:%S')
        
        query = """
        WITH strategy_data AS (
            SELECT 
                r.name AS bot,
                t.name AS ticker,
                r.granularity,
                AVG(COALESCE(hp.result_fee, 0)) AS avg_profit,  -- Защита от NULL
                COUNT(*) AS total_trades,
                MAX(hp.close_timestamp) AS last_trade_time,
                SQRT(ABS(AVG(hp.result_fee * hp.result_fee) - POWER(AVG(hp.result_fee), 2))) AS profit_stddev,
                AVG(CASE WHEN hp.result_fee > 0 THEN 1.0 ELSE 0.0 END) AS win_rate
            FROM history_positions hp
            JOIN robots r ON hp.robot_id = r.id
            JOIN tickers t ON hp.ticker_id = t.id
            WHERE r.granularity = ?
            AND hp.close_timestamp >= ?
            AND r.name NOT LIKE '%SKYNET%'
            GROUP BY r.name, t.name, r.granularity
            HAVING total_trades >= 3
            AND profit_stddev > 0
            AND win_rate > 0.3
        )
        SELECT *,
            (avg_profit / (CASE WHEN profit_stddev < 1e-6 THEN 1e-6 ELSE profit_stddev END)) * win_rate AS stability_index
        FROM strategy_data
        WHERE avg_profit > 0
        ORDER BY stability_index DESC
        """
        
        with sqlite3.connect(db_path) as conn:
            df = pd.read_sql(query, conn, params=(granularity, time_threshold_str))

            
        if df.empty:
            return pd.DataFrame()

        try:
            # Рассчет свежести данных
            df['last_trade_hours'] = (datetime.now() - pd.to_datetime(df['last_trade_time'])).dt.total_seconds() / 3600
            df['recency_score'] = np.exp(-df['last_trade_hours'] / 24)  # Вес свежести
            
            # Нормализация метрик
            metrics = ['stability_index', 'win_rate', 'recency_score']
            scaler = RobustScaler()
            df[metrics] = scaler.fit_transform(df[metrics])
            
            # Итоговый score (только стабильность и свежесть)
            df['score'] = 0.7 * df['stability_index'] + 0.3 * df['recency_score']
            
            # Выбор лучшей стратегии для каждого тикера
            best_strategies = df.loc[df.groupby('ticker')['score'].idxmax()]
            
            return best_strategies[['ticker', 'bot', 'score', 'avg_profit', 'win_rate']]\
                     .sort_values('score', ascending=False)
            
        except Exception as e:
            print(f"Metric calculation error: {e}")
            return pd.DataFrame(columns=['ticker', 'bot'])
            
    except Exception as e:
        print(f"Critical error: {e}")
        return pd.DataFrame()
    

def get_top5_strategies(db_path, granularity='1h', lookback_deals=30):
    """
    Выбирает топ-5 стратегий с высоким процентом выигрышей и часовой доходностью для каждого тикера
    :param lookback_deals: количество последних сделок для анализа
    :return: DataFrame с топ-5 стратегиями для каждого тикера
    """
    try:
        query = f"""
        WITH ranked_trades AS (
            SELECT 
                r.name AS bot,
                t.name AS ticker,
                hp.result_fee,
                hp.close_timestamp,
                ROW_NUMBER() OVER (
                    PARTITION BY r.name, t.name 
                    ORDER BY hp.close_timestamp DESC
                ) AS trade_num
            FROM history_positions hp
            JOIN robots r ON hp.robot_id = r.id
            JOIN tickers t ON hp.ticker_id = t.id
            WHERE r.granularity = ?
              AND r.name NOT LIKE '%SKYNET%'
        ),
        last_n_trades AS (
            SELECT *,
                CASE WHEN result_fee > 0 THEN 1 ELSE 0 END AS is_win
            FROM ranked_trades
            WHERE trade_num <= ?
        )
        SELECT
            bot,
            ticker,
            COUNT() AS total_trades,
            AVG(result_fee) AS avg_result,
            SUM(result_fee) AS total_result,
            MAX(close_timestamp) AS last_trade_time,
            AVG(is_win) * 100 AS win_rate,
            SUM(result_fee) / (
                (JULIANDAY(MAX(close_timestamp)) - JULIANDAY(MIN(close_timestamp))) * 24
            ) AS hourly_return,
            SQRT(AVG(result_fee*result_fee) - AVG(result_fee)*AVG(result_fee)) AS variance
        FROM last_n_trades
        GROUP BY bot, ticker
        HAVING total_trades >= ? * 0.7
        AND hourly_return > 0
        AND win_rate >= 50
        """
        
        with sqlite3.connect(db_path) as conn:
            df = pd.read_sql(query, conn, 
                            params=(granularity, lookback_deals, lookback_deals))
            
        if df.empty:
            return pd.DataFrame()
        # Нормализация метрик
        metrics = ['win_rate', 'hourly_return', 'avg_result']
        df[metrics] = df[metrics].apply(lambda x: (x - x.mean()) / (x.std()+1e-6))
        
        # Итоговый score с приоритетом на win rate и часовую доходность
        df['score'] = (
            0.5 * df['win_rate'] + 
            0.3 * df['hourly_return'] +
            0.2 * df['avg_result']
        )
        
        # Получаем топ-5 стратегий для каждого тикера
        top_strategies = df.groupby('ticker').apply(
            lambda x: x.nlargest(5, 'score')
        ).reset_index(drop=True)
        
        return top_strategies.sort_values(['ticker', 'score'], ascending=[True, False])

    except Exception as e:
        print(f"Error: {str(e)}")
        return pd.DataFrame()
    
def get_top5_best_strategies_stable(db_path, granularity='1h', lookback_hours=24):
    try:
        time_threshold = datetime.now() - timedelta(hours=lookback_hours)
        time_threshold_str = time_threshold.strftime('%Y-%m-%d %H:%M:%S')
        
        query = """
        WITH strategy_data AS (
            SELECT 
                r.name AS bot,
                t.name AS ticker,
                r.granularity,
                AVG(COALESCE(hp.result_fee, 0)) AS avg_profit,
                SUM(COALESCE(hp.result_fee, 0)) AS total_profit,  -- Добавляем суммарную прибыль
                COUNT(*) AS total_trades,
                MAX(hp.close_timestamp) AS last_trade_time,
                SQRT(ABS(AVG(hp.result_fee * hp.result_fee) - POWER(AVG(hp.result_fee), 2))) AS profit_stddev,
                AVG(CASE WHEN hp.result_fee > 0 THEN 1.0 ELSE 0.0 END) AS win_rate,
                AVG(hp.fee) AS avg_fee  -- Средняя комиссия
            FROM history_positions hp
            JOIN robots r ON hp.robot_id = r.id
            JOIN tickers t ON hp.ticker_id = t.id
            WHERE r.granularity = ?
            AND hp.close_timestamp >= ?
            AND r.name NOT LIKE '%SKYNET%'
            GROUP BY r.name, t.name, r.granularity
            HAVING total_trades >= 3
            AND profit_stddev > 0
            AND win_rate > 0.3
        )
        SELECT *,
            (avg_profit / (CASE WHEN profit_stddev < 1e-6 THEN 1e-6 ELSE profit_stddev END)) * win_rate AS stability_index,
            (total_profit - SUM(avg_fee * total_trades)) AS net_profit  -- Прибыль за вычетом комиссий
        FROM strategy_data
        WHERE avg_profit > 0
        GROUP BY bot, ticker, granularity
        ORDER BY net_profit DESC, stability_index DESC
        """
        
        with sqlite3.connect(db_path) as conn:
            df = pd.read_sql(query, conn, params=(granularity, time_threshold_str))

        if df.empty:
            return pd.DataFrame()

        try:
            # Рассчет свежести данных
            df['last_trade_hours'] = (datetime.now() - pd.to_datetime(df['last_trade_time'])).dt.total_seconds() / 3600
            df['recency_score'] = np.exp(-df['last_trade_hours'] / 24)
            
            # Рассчет частоты торговли
            df['trades_per_hour'] = df['total_trades'] / lookback_hours
            df['activity_score'] = 1 - np.exp(-df['trades_per_hour'] / 0.1)  # Нормализация частоты
            
            # Нормализация метрик
            metrics = ['stability_index', 'win_rate', 'recency_score', 'net_profit', 'activity_score']
            scaler = RobustScaler()
            df[metrics] = scaler.fit_transform(df[metrics])
            
            # Новый score с учетом прибыльности и активности
            df['score'] = (
                0.4 * df['net_profit'] +  # Основной вес у чистой прибыли
                0.3 * df['stability_index'] +
                0.1 * df['win_rate'] +
                0.1 * df['recency_score'] +
                0.1 * df['activity_score']  # Штрафуем редкие стратегии
            )
            
            # Получаем топ-5 стратегий для каждого тикера
            top_strategies = df.groupby('ticker').apply(
                lambda x: x.nlargest(5, 'score')
            ).reset_index(drop=True)
            
            return top_strategies.sort_values(['ticker', 'score'], ascending=[True, False])
            
        except Exception as e:
            print(f"Metric calculation error: {e}")
            return pd.DataFrame(columns=['ticker', 'bot'])
            
    except Exception as e:
        print(f"Critical error: {e}")
        return pd.DataFrame()