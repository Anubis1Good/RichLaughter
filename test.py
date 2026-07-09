import cv2
import numpy as np

def find_colored_regions(image, color_bgr,region_img=None, y_min=None, y_max=None, reverse_sort=False):


    mask = cv2.inRange(image, color_bgr, color_bgr)
    cv2.imshow('mask',mask)
    # 2. Находим контуры областей
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # 3. Фильтруем и собираем информацию
    regions = []
    used_y_positions = []
    for contour in contours:
        area = cv2.contourArea(contour)
        # Фильтр по площади
        if area < 1:
            continue
        # Вычисляем bounding box
        x, y, w, h = cv2.boundingRect(contour)
        # Центр области
        cx = x + w // 2
        cy = y + h // 2
        if region_img is not None and region_img[0] is not None:
            if not region_img[0] < cx < region_img[2]:
                continue
        if y_max is not None:
            if cy > y_max:
                continue
        if y_min is not None:
            if cy < y_min:
                continue
        # Сохраняем информацию
        is_duplicate = False
        for used_y in used_y_positions:
            if abs(cy - used_y) <= 10:
                is_duplicate = True
                break
        
        if is_duplicate:
            continue  # Пропускаем дубликат
        
        # Добавляем новую уникальную область
        used_y_positions.append(cy)
        regions.append({
            'center_x': cx,
            'center_y': cy,
        })
    
    # 4. Сортируем
    regions.sort(key=lambda r: r['center_y'],reverse=reverse_sort)
    
    return regions

def find_and_highlight_regions(image, color_bgr,region_img=None, y_min=None, y_max=None, min_area=50, max_area=None,reverse_sort=False):
    """
    Находит области и возвращает изображение с выделенными областями
    """
    
    # Создаем копию для отрисовки
    result = image.copy()
    
    # Находим области
    regions = find_colored_regions(image, color_bgr,region_img=region_img,y_min=y_min,y_max=y_max,reverse_sort=reverse_sort)
    
    # Отрисовываем каждую область

    for i, region in enumerate(regions):

        
        # Рисуем центр
        cv2.circle(result, (region['center_x'], region['center_y']), 3, (0, 0, 255), -1)
        
        # Подписываем номер и площадь
        label = f"#{i+1} ()"
        cv2.putText(result, label, (region['center_x'], region['center_y'] - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    
    return result, regions

# Использование
img = cv2.imread(".\logs\debug_VT5\ETLN11783619207555.png")
color = (135,103,96)

# Найти области с минимальной площадью 50 пикселей
# result_img, regions = find_and_highlight_regions(img, color,region_img=(838,57,957,517),y_min=304,y_max=None,reverse_sort=False)
result_img, regions = find_and_highlight_regions(img, color,region_img=None,y_min=None,y_max=None,reverse_sort=False)

# Вывести информацию

# Показать результат
# cv2.imshow('Found Regions', result_img)
cv2.waitKey(0)
cv2.destroyAllWindows()