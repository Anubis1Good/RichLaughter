import sqlite3
import os
from datetime import datetime, timedelta
import traceback
def delete_inactive_bots(db_path):
    # Рассчитываем пороговую дату (2 дня назад)
    threshold_date = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # Начинаем транзакцию
            cursor.execute("BEGIN TRANSACTION;")
            
            # 1. Удаляем связанные записи из history_positions
            delete_history_query = """
            DELETE FROM history_positions 
            WHERE robot_id IN (
                SELECT r.id 
                FROM robots r
                LEFT JOIN history_positions hp ON r.id = hp.robot_id
                GROUP BY r.id
                HAVING MAX(hp.close_timestamp) < ? 
                    OR MAX(hp.close_timestamp) IS NULL
            );
            """
            cursor.execute(delete_history_query, (threshold_date,))
            
            # 2. Удаляем связанные записи из positions
            delete_positions_query = """
            DELETE FROM positions 
            WHERE robot_id IN (
                SELECT r.id 
                FROM robots r
                LEFT JOIN history_positions hp ON r.id = hp.robot_id
                GROUP BY r.id
                HAVING MAX(hp.close_timestamp) < ? 
                    OR MAX(hp.close_timestamp) IS NULL
            );
            """
            cursor.execute(delete_positions_query, (threshold_date,))
            
            # 3. Удаляем самих ботов
            delete_robots_query = """
            DELETE FROM robots 
            WHERE id IN (
                SELECT r.id 
                FROM robots r
                LEFT JOIN history_positions hp ON r.id = hp.robot_id
                GROUP BY r.id
                HAVING MAX(hp.close_timestamp) < ? 
                    OR MAX(hp.close_timestamp) IS NULL
            );
            """
            cursor.execute(delete_robots_query, (threshold_date,))
            
            # Фиксируем изменения
            conn.commit()
            
            print(f"Удалено ботов: {cursor.rowcount}")
            
    except sqlite3.Error as e:
        print(f"Ошибка при удалении ботов: {str(e)}")
        conn.rollback()

# Использование
if __name__ == '__main__':
    folder = 'dbs'
    files = os.listdir(folder)
    for file in files:
        if file.endswith('.db'):
            try:
                file_path = os.path.join(folder,file)
                delete_inactive_bots(file_path)
            except Exception as e:
                traceback.print_exc()
                print(file,'have problems...')