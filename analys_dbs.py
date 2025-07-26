import os
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import shutil
import traceback
from datetime import datetime
from utils.processing_results.add_vtb_fee_fut import get_func_vtb_fee


def process_history_position(result:pd.DataFrame,suffix,db_path):
    result['tf'] = result['bot'].str.split('_').str[0]
    tf = result.pop('tf')
    result.insert(2,'tf',tf)
    result['total_with_average_fee'] = result['total_result'] - result['total_fee'] * 2
    result['total_with_max_fee'] = result['total_result'] - result['total_fee'] * 3
    result['total_per'] = ((result['total_result']/result['avg_close_price'])*100).round(2)
    result['t_min_fp'] = ((result['total_result_fee']/result['avg_close_price'])*100).round(2)
    result['t_avg_fp'] = ((result['total_with_average_fee']/result['avg_close_price'])*100).round(2)
    result['t_max_fp'] = ((result['total_with_max_fee']/result['avg_close_price'])*100).round(2)
    result = result.drop(['avg_close_price','total_fee','total_result_fee','total_with_average_fee','total_with_max_fee'],axis=1)
# Самый надёжный вариант - использовать list comprehension
    result['vtbf_res'] = [
        float(get_func_vtb_fee(row['ticker'])(float(row['total_result']), int(row['total_trades'])))
        for _, row in result.iterrows()
    ]
    result['p'] = result['t_min_fp'] > 0
    has_days = 'days' in result.columns.tolist()

    if has_days:
        result['cd'] = round(result['total_trades'] / result['days'],2)
        result['pred'] = result['avgt'] * result['cd']
        result['trd'] = result['total_result'] / result['days']
        result['trd_vtb'] = result['vtbf_res'] / result['days']
    result = result.sort_values(by=['ticker','avgt'],axis=0,ascending=[True,False])
    result = result.reset_index(drop=True)

    ranks = ['total_trades','total_per','t_min_fp','t_avg_fp','t_max_fp','avgdd','maxdd','avgt','maxp','win_rate','p']
    if has_days:
        ranks += ['cd','pred','trd','trd_vtb','days']
    data_sum = result.groupby('bot')[ranks].mean().sort_values('t_avg_fp',ascending=False).round(2)
    rank_names = ["r_"+r for r in ranks]
    for r in ranks:
        # print(r)
        result["r_"+r] = result.groupby("ticker")[r].rank(ascending=False, method="min")
    avg_rank = result.groupby("bot")[rank_names].mean().sort_values('r_t_avg_fp').round(2)

    result_old = result.copy()
    result_old = result_old.sort_values(by=['ticker','t_min_fp'],axis=0,ascending=[True,False])
    result_old = result_old.reset_index(drop=True)
    if has_days:
        result_pred = result.copy()
        result_pred = result_pred.sort_values(by=['ticker','pred'],axis=0,ascending=[True,False])
        result_pred = result_pred.reset_index(drop=True)

    result2 = pd.concat([avg_rank, data_sum], axis=1)
    result2['tf'] = result2.index.str.split('_').str[0]
    tf = result2.pop('tf')
    result2.insert(0,'tf',tf)
    to_end = ('r_total_per','r_t_min_fp','r_t_avg_fp','r_t_max_fp')
    # Все остальные колонки (кроме тех, что в to_end)
    other_columns = [col for col in result2.columns if col not in to_end]

    # Новый порядок: сначала остальные, потом to_end
    new_order = other_columns + list(to_end)

    # Переупорядочиваем DataFrame
    result2 = result2[new_order]
    result2_old = result2.copy()
    result2_old = result2_old.sort_values('r_t_min_fp')
    result2_old = result2.reset_index()
    if has_days:
        result2_pred = result2.copy()
        result2_pred = result2_pred.sort_values('r_pred')
        result2_pred = result2_pred.reset_index()
    result2 = result2.sort_values('r_avgt')
    result2 = result2.reset_index()
    # print(result2)
    # print(avg_rank)
    prefix = "_".join(db_path.split('_')[1:]).replace('.db','')
    file_name = f'TestOtTrades/Total_{suffix}_Test_Result_{prefix}.xlsx'

    with pd.ExcelWriter(file_name, engine='xlsxwriter') as writer:  
        results = [result,result_old]
        if has_days:
            results += [result_pred]
        for idx,result in enumerate(results):
            name_sheet = 'total_' + str(idx)
            result.to_excel(writer,sheet_name=name_sheet)
            workbook = writer.book
            worksheet = writer.sheets[name_sheet]
            for i, col in enumerate(result.columns,start=1):
                width = max(result[col].apply(lambda x: len(str(x))).max(), len(col))
                worksheet.set_column(i, i, width)
                worksheet.conditional_format(1, i, len(result), i, {
                    'type': 'cell',
                    'criteria': 'less than',
                    'value': 0,
                    'format': workbook.add_format({'bg_color': '#FFC7CE', 'font_color': '#9C0006'})
                })
                worksheet.conditional_format(1, i, len(result), i, {
                    'type': '3_color_scale',
                    'min_color': '#DA9694',
                    'mid_color': '#FFFFFF',
                    'max_color': '#00B0F0'
                })
                # worksheet.conditional_format(1, i, len(result), i, {
                #     'type': 'text',
                #     'criteria': 'containing',
                #     'value': 'MTA',
                #     'format': workbook.add_format({'bg_color': '#FFC7CE', 'font_color': '#9C0006'})
                # })
        results2 = [result2,result2_old]
        if has_days:
            results2 += [result2_pred]
        for idx,result2 in enumerate(results2):
            name_sheet = 'bots_info_' + str(idx)
            result2.to_excel(writer,sheet_name=name_sheet)
            workbook = writer.book
            worksheet = writer.sheets[name_sheet]
            for i, col in enumerate(result2.columns,start=1):
                width = max(result2[col].apply(lambda x: len(str(x))).max(), len(col))
                worksheet.set_column(i, i, width)
                worksheet.conditional_format(1, i, len(result2), i, {
                    'type': 'cell',
                    'criteria': 'less than',
                    'value': 0,
                    'format': workbook.add_format({'bg_color': '#FFC7CE', 'font_color': '#9C0006'})
                })
                # worksheet.conditional_format(1, i, len(result2), i, {
                #     'type': 'text',
                #     'criteria': 'containing',
                #     'value': 'MTA',
                #     'format': workbook.add_format({'bg_color': '#FFC7CE', 'font_color': '#9C0006'})
                # })
                # print(col)
                if col in rank_names and not 'dd' in col:
                    worksheet.conditional_format(1, i, len(result2), i, {
                        'type': '3_color_scale',
                        'max_color': '#DA9694',
                        'mid_color': '#FFFFFF',
                        'min_color': '#00B0F0'
                    })
                else:
                    worksheet.conditional_format(1, i, len(result2), i, {
                        'type': '3_color_scale',
                        'min_color': '#DA9694',
                        'mid_color': '#FFFFFF',
                        'max_color': '#00B0F0'
                    })


def add_days(df):
    df['last_trade_date'] = pd.to_datetime(df['last_trade_date'])
    df['start_trade_date'] = pd.to_datetime(df['start_trade_date'])
    df['days'] = (df['last_trade_date'] - df['start_trade_date']).dt.days + 1
    df['days'] = df['days'] - ((df['days']//7)*2)
    # Получаем список всех столбцов
    cols = df.columns.tolist()

    # Находим индекс 'last_trade_date'
    idx = cols.index('last_trade_date')
    cols.remove('days')  # (если он был где-то ещё)


    # Вставляем 'days' после 'last_trade_date'
    cols.insert(idx + 1, 'days')

    # Удаляем старый 'days' (если он уже был в другом месте)

    # Переупорядочиваем DataFrame
    df = df[cols]
    return df

def analisys_db(db_path:str):
    conn = sqlite3.connect(db_path)
    query = '''
        SELECT 
            r.id AS bot_id,
            r.name AS bot,
            t.name AS ticker,
            MIN(hp.open_timestamp) AS start_trade_date,
            MAX(hp.close_timestamp) AS last_trade_date,
            AVG(hp.close_price) AS avg_close_price,
            SUM(hp.fee) AS total_fee,
            SUM(hp.result) AS total_result,
            COUNT(*) AS total_trades,
            SUM(hp.result_fee) AS total_result_fee,
            -- Расчет просадок на лету
            ROUND(AVG(CASE 
                    WHEN hp.result_fee < 0 
                    THEN ABS(hp.result_fee) * 100.0 / NULLIF(hp.open_price, 0) 
                    ELSE 0 
                    END), 2) AS avgdd,
            ROUND(MAX(CASE 
                    WHEN hp.result_fee < 0 
                    THEN ABS(hp.result_fee) * 100.0 / NULLIF(hp.open_price, 0) 
                    ELSE 0 
                    END), 2) AS maxdd,
            ROUND(AVG(hp.result_fee * 100.0 / NULLIF(hp.open_price, 0)), 2) AS avgt,
            ROUND(MAX(hp.result_fee * 100.0 / NULLIF(hp.open_price, 0)), 2) AS maxp,
            ROUND(AVG(CASE WHEN hp.result_fee >= 0 THEN 1.0 ELSE 0.0 END) * 100, 2) AS win_rate
        FROM 
            history_positions hp
        JOIN 
            robots r ON hp.robot_id = r.id
        JOIN 
            tickers t ON hp.ticker_id = t.id
        GROUP BY 
            r.id, r.name, t.name
        ORDER BY 
            r.name, t.name
        '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    df = add_days(df)
    process_history_position(df,'All',db_path)

def analisys_db_n_days(db_path: str, n_days: int):
    conn = sqlite3.connect(db_path)
    query = '''
    SELECT 
        r.id AS bot_id,
        r.name AS bot,
        t.name AS ticker,
        MIN(hp.open_timestamp) AS start_trade_date,
        MAX(hp.close_timestamp) AS last_trade_date,
        AVG(hp.close_price) AS avg_close_price,
        SUM(hp.fee) AS total_fee,
        SUM(hp.result) AS total_result,
        COUNT(*) AS total_trades,
        SUM(hp.result_fee) AS total_result_fee,
        ROUND(AVG(CASE 
                WHEN hp.result_fee < 0 
                THEN ABS(hp.result_fee) * 100.0 / NULLIF(hp.open_price, 0) 
                ELSE 0 
                END), 2) AS avgdd,
        ROUND(MAX(CASE 
                WHEN hp.result_fee < 0 
                THEN ABS(hp.result_fee) * 100.0 / NULLIF(hp.open_price, 0) 
                ELSE 0 
                END), 2) AS maxdd,
        ROUND(AVG(hp.result_fee * 100.0 / NULLIF(hp.open_price, 0)), 2) AS avgt,
        ROUND(MAX(hp.result_fee * 100.0 / NULLIF(hp.open_price, 0)), 2) AS maxp,
        ROUND(AVG(CASE WHEN hp.result_fee >= 0 THEN 1.0 ELSE 0.0 END) * 100, 2) AS win_rate
    FROM 
        history_positions hp
    JOIN 
        robots r ON hp.robot_id = r.id
    JOIN 
        tickers t ON hp.ticker_id = t.id
    WHERE 
        hp.close_timestamp >= datetime('now', '-' || ? || ' days')
    GROUP BY 
        r.id, r.name, t.name
    ORDER BY 
        r.name, t.name
    '''
    df = pd.read_sql_query(query, conn, params=(str(n_days),))  # Преобразуем n_days в строку
    conn.close()
    df = add_days(df)
    process_history_position(df, f'{n_days}Days', db_path)
    return df

def analisys_db_last(db_path:str):
    conn = sqlite3.connect(db_path)
    query = '''
    SELECT 
        r.id AS bot_id,
        r.name AS bot,
        t.name AS ticker,
        MAX(hp.close_timestamp) AS last_trade_date,
        AVG(hp.close_price) AS avg_close_price,
        SUM(hp.fee) AS total_fee,
        SUM(hp.result) AS total_result,
        COUNT(*) AS total_trades,
        SUM(hp.result_fee) AS total_result_fee,
        -- Расчет метрик просадки и прибыли
        -- Расчет просадок на лету
        ROUND(AVG(CASE 
                WHEN hp.result_fee < 0 
                THEN ABS(hp.result_fee) * 100.0 / NULLIF(hp.open_price, 0) 
                ELSE 0 
                END), 2) AS avgdd,
        ROUND(MAX(CASE 
                WHEN hp.result_fee < 0 
                THEN ABS(hp.result_fee) * 100.0 / NULLIF(hp.open_price, 0) 
                ELSE 0 
                END), 2) AS maxdd,
        ROUND(AVG(hp.result_fee * 100.0 / NULLIF(hp.open_price, 0)), 2) AS avgt,
        ROUND(MAX(hp.result_fee * 100.0 / NULLIF(hp.open_price, 0)), 2) AS maxp,
        ROUND(AVG(CASE WHEN hp.result_fee >= 0 THEN 1.0 ELSE 0.0 END) * 100, 2) AS win_rate
    FROM 
        history_positions hp
    JOIN 
        robots r ON hp.robot_id = r.id
    JOIN 
        tickers t ON hp.ticker_id = t.id
    WHERE 
        DATE(hp.close_timestamp) = CURRENT_DATE
    GROUP BY 
        r.id, r.name, t.name
    ORDER BY 
        r.name, t.name
    '''
    result = pd.read_sql_query(query, conn)
    conn.close()
    process_history_position(result,'Last',db_path)


def get_equity_charts_db(db_path,query,folder):
    conn = sqlite3.connect(db_path)
    prefix = "_".join(db_path.split('_')[1:]).replace('.db','')
    image_path = 'TestOtTrades/cumulative_results_plots/'+ folder + '/' + prefix
    if os.path.exists(image_path):
        shutil.rmtree(image_path)
    os.makedirs(image_path, exist_ok=True)

    # Создаем список для хранения данных о доходности
    performance_records = []

    # Получаем список всех тикеров
    tickers_query = "SELECT id, name FROM tickers"
    tickers_df = pd.read_sql_query(tickers_query, conn)

    # Для каждого тикера строим графики
    for ticker_id, ticker_name in tickers_df.values:
        create_chart(image_path,ticker_name,ticker_id,conn,performance_records,query)

    conn.close()
    print("Обработка завершена!")

queryAllChart = '''
    SELECT 
        r.name AS bot_name,
        hp.open_timestamp,
        hp.result,
        hp.result_fee,
        SUM(hp.result) OVER (PARTITION BY r.name ORDER BY hp.open_timestamp) AS cumulative_result,
        SUM(hp.result_fee) OVER (PARTITION BY r.name ORDER BY hp.open_timestamp) AS cumulative_result_fee
    FROM 
        history_positions hp
    JOIN 
        robots r ON hp.robot_id = r.id
    WHERE 
        hp.ticker_id = (?)
    ORDER BY 
        r.name, hp.open_timestamp
    '''

queryDayChart = '''
    SELECT 
        r.name AS bot_name,
        hp.open_timestamp,
        hp.result,
        hp.result_fee,
        SUM(hp.result) OVER (PARTITION BY r.name ORDER BY hp.open_timestamp) AS cumulative_result,
        SUM(hp.result_fee) OVER (PARTITION BY r.name ORDER BY hp.open_timestamp) AS cumulative_result_fee
    FROM 
        history_positions hp
    JOIN 
        robots r ON hp.robot_id = r.id
    WHERE 
        hp.ticker_id = (?) AND DATE(hp.open_timestamp) = CURRENT_DATE
    ORDER BY 
        r.name, hp.open_timestamp
    '''

def create_chart(image_path,ticker_name,ticker_id,conn,performance_records,query):
    ticker_path = os.path.join(image_path, ticker_name)
    os.makedirs(ticker_path, exist_ok=True)
    df = pd.read_sql_query(query, conn,params=(ticker_id,))
    
    if df.empty:
        print(f"Нет данных для тикера: {ticker_name}")
        return
    
    for bot_name, group in df.groupby('bot_name'):
        # Получаем конечную доходность (с комиссиями)
        final_result = group['cumulative_result_fee'].iloc[-1]
        
        # Добавляем информацию для отчета
        performance_records.append({
            'ticker': ticker_name,
            'bot': bot_name,
            'result': final_result,
            'filepath': os.path.join(ticker_name, f'{ticker_name}_{bot_name}_{final_result:+.3f}_result.png')
        })
        
        plt.figure(figsize=(12, 6))
        
        # Линия 1: Доходность БЕЗ учета комиссий
        plt.plot(
            pd.to_datetime(group['open_timestamp']),
            group['cumulative_result'],
            label=f'{bot_name} (Без комиссий)',
            color='green',
            linestyle='--',
            linewidth=2
        )
        
        # Линия 2: Доходность С учетом комиссий
        plt.plot(
            pd.to_datetime(group['open_timestamp']),
            group['cumulative_result_fee'],
            label=f'{bot_name} (С комиссиями: {final_result:+.3f})',
            color='blue',
            linestyle='-',
            linewidth=2
        )
        
        plt.title(f'Кумулятивная доходность: {bot_name} ({ticker_name})')
        plt.xlabel('Дата')
        plt.ylabel('Доходность')
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Сохраняем с доходностью в имени файла
        plot_filename = os.path.join(ticker_path, f'{ticker_name}_{final_result:+.3f}_{bot_name}_result.png')
        plt.savefig(plot_filename, dpi=300)
        plt.close()
        
        print(f"График сохранен: {plot_filename}")

need_equity_chart = False
# need_equity_chart = True
need_equity_last_chart = False
# need_equity_last_chart = True
need_analisys = False
need_analisys = True
need_last = False
# need_last = True
need_n_days = False
need_n_days = True

if __name__ == '__main__':
    print('analys start...')
    folder = 'dbs'
    files = os.listdir(folder)
    for file in files:
        if file.endswith('.db'):
            try:
                file_path = os.path.join(folder,file)
                if need_analisys:
                    analisys_db(file_path)
                if need_last:
                    analisys_db_last(file_path)
                if need_n_days:
                    analisys_db_n_days(file_path,14)
                if need_equity_chart:
                    get_equity_charts_db(file_path,queryAllChart,'AllTime')
            except Exception as e:
                traceback.print_exc()
                print(file,'have problems...')
    print('analys end!')
    # get_equity_charts_db('dbs/test_MOEX_FUT.db',queryDayChart,'LastDay')
    # get_equity_charts_db('dbs/test_MOEX_STOCK.db',queryDayChart,'LastDay')
    # get_equity_charts_db('dbs/test_offline.db',queryDayChart,'LastDay')
