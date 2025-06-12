from strategies.work_strategies.MTA_KING import MTA_KING

ws = MTA_KING(symbol='MXM5',granularity='1',pick_file='KING_1_MOEX_FUT',alias='RIM5')

# ws.choice_ws_king()
try:
    ws.preprocessing(1)
except:
    pass
print(ws.symbol)
print(ws.work_symbol)
print(ws.name_bot_king)
print(ws.tas_king)
print(ws.strategy_king.tas)
print(ws.strategy_king.symbol)
print(ws.strategy_king.work_symbol)
try:
    ws.strategy_king.preprocessing(1)
except:
    pass
print(ws.strategy_king.strategy)