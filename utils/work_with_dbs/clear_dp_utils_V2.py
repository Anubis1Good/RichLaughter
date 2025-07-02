import sqlite3
import os
import traceback
from Screening.utils.keys_strategies_with_MTA import allDCwithMTA

query_all_bots = '''
    SELECT id, name FROM robots
'''
delete_history_query = """
    DELETE FROM history_positions 
    WHERE robot_id IN (
"""
delete_positions_query = """
    DELETE FROM positions 
    WHERE robot_id IN (
    """
delete_robots_query = """
    DELETE FROM robots 
    WHERE id IN (
    """
queries_del = (delete_history_query,delete_positions_query,delete_robots_query)

def delete_inactive_bots(db_path,file:str):
    # pprint(allDC)
    name_exchange = "_".join(file.split('_')[1:]).split('.')[0]
    if name_exchange in allDCwithMTA:
        try:
            del_bots = []
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(query_all_bots)
                all_bots = cursor.fetchall()
                for id,name in all_bots:
                    if not name in allDCwithMTA[name_exchange]:
                        print(name)
                        del_bots.append(id)
                placeholders = ",".join(["?"] * len(del_bots))
                for q in queries_del:
                    q_n = q + placeholders + ');'
                    cursor.execute(q_n, del_bots)
                conn.commit()
                cursor.execute("VACUUM;")
                conn.commit()
                print(file,f"Удалено ботов:",len(del_bots))

        except sqlite3.Error as e:
            print(f"Ошибка при удалении ботов: {str(e)}")
            conn.rollback()    
    else:
        print('Биржи нет')

# Использование

folder = 'dbs/test'
folder = 'dbs'
files = os.listdir(folder)
for file in files:
    if file.endswith('.db'):
        try:
            file_path = os.path.join(folder,file)
            delete_inactive_bots(file_path,file)
        except Exception as e:
            traceback.print_exc()
            print(file,'have problems...')