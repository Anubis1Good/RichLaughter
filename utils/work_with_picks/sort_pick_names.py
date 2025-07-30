import os
import json

main_folder = 'Screening/strat_picks'

for filename in os.listdir(main_folder):
    file_path = os.path.join(main_folder, filename)
    
    if not os.path.isfile(file_path):
        continue  # Пропускаем подпапки
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Если есть 'Other' - ставим его первым, остальные сортируем
        if 'Other' in data:
            other_item = ('Other', data.pop('Other'))
            sorted_items = sorted(data.items())
            sorted_data = dict([other_item] + sorted_items)
        else:
            # Если 'Other' нет - просто сортируем всё
            sorted_data = dict(sorted(data.items()))
        
        # Записываем обратно
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(sorted_data, f, indent=4, ensure_ascii=False)
        
        print(f"Файл {filename} успешно обработан.")
    
    except json.JSONDecodeError:
        print(f"Ошибка: файл {filename} не является валидным JSON. Пропускаем.")
    except Exception as e:
        print(f"Ошибка при обработке файла {filename}: {str(e)}")
    