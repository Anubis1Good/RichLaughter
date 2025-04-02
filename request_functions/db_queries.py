# сделки получить
query = '''
    SELECT 
        hp.id,
        r.name AS bot,
        r.granularity AS bot_g,
        t.name AS ticker,  
        hp.fee,
        hp.result,
        hp.result_fee
    FROM 
        history_positions hp
    JOIN 
        robots r ON hp.robot_id = r.id
    JOIN 
        tickers t ON hp.ticker_id = t.id
    '''