import cv2
import numpy as np
import pandas as pd
class TemplateCandle:
    candle_top = np.array([
        [0,0,0],
        [0,255,0]
    ],dtype=np.uint8)

    candle_bottom = np.array([
        [0,255,0],
        [0,0,0]
    ],dtype=np.uint8)

    candle_close = np.array([
        [0,0],
        [255,0],
        [0,0],
    ],dtype=np.uint8)

    candle_open = np.array([
        [0,0],
        [0,255],
        [0,0],
    ],dtype=np.uint8)

    volume_top = np.array([
        [0,0,0,0],
        [0,255,255,0]
    ],dtype=np.uint8)
# Использование
img = cv2.imread("DataForTests\ImgCs\Screenshot_35.png")
candle_color_1 = (111,111,111)
candle_color_2 = (200,200,200)

mask1 = cv2.inRange(img,candle_color_1,candle_color_1)
mask2 = cv2.inRange(img,candle_color_2,candle_color_2)
mask = cv2.add(mask1,mask2)
candle_cords = np.argwhere(mask == 255)

volume_color_1 = (92,107,61)
volume_color_2 = (89,89,128)
mask1 = cv2.inRange(img,volume_color_1,volume_color_1)
mask2 = cv2.inRange(img,volume_color_2,volume_color_2)
mask_v = cv2.add(mask1,mask2)
kernel = np.ones((1, 2), np.uint8)  # 1 строка x 3 столбца
mask_v2 = cv2.dilate(mask_v, kernel, iterations=1)
volume_cords = np.argwhere(mask_v2 == 255)

res_top = cv2.matchTemplate(mask,TemplateCandle.candle_top,cv2.TM_CCOEFF_NORMED)
res_top = np.argwhere(res_top >= 0.9)
# res_top = res_top[res_top[:, 1].argsort()]
# sorted_data = res_top[np.lexsort((res_top[:, 0], res_top[:, 1]))]
# _, unique_indices = np.unique(sorted_data[:, 1], return_index=True)
# res_top = sorted_data[unique_indices]

res_bot = cv2.matchTemplate(mask,TemplateCandle.candle_bottom,cv2.TM_CCOEFF_NORMED)
res_bot = np.argwhere(res_bot >= 0.9)
# res_bot = res_bot[res_bot[:, 1].argsort()]
# sorted_data = res_bot[np.lexsort((-res_bot[:, 0], res_bot[:, 1]))]
# _, unique_indices = np.unique(sorted_data[:, 1], return_index=True)
# res_bot = sorted_data[unique_indices]

# res_open = cv2.matchTemplate(mask,TemplateCandle.candle_open,cv2.TM_CCOEFF_NORMED)
# res_open = np.argwhere(res_open >= 0.9)
# res_open = res_open[res_open[:, 1].argsort()]

# res_close = cv2.matchTemplate(mask,TemplateCandle.candle_close,cv2.TM_CCOEFF_NORMED)
# res_close = np.argwhere(res_close >= 0.9)
# res_close = res_close[res_close[:, 1].argsort()]

res_x = np.concatenate((res_top,res_bot))
unique_x = np.unique(res_x[:, 1])
unique_x = np.sort(unique_x)
distances = np.diff(unique_x)
step = int(np.median(distances))
print(f"Шаг сетки: {step}")
good_start = None
for i in range(len(unique_x) - 1):
    if abs(unique_x[i+1] - unique_x[i]) == step:
        good_start = unique_x[i]
        break

# Находим "правильный" последний X
good_end = None
for i in range(len(unique_x) - 1, 0, -1):
    if abs(unique_x[i] - unique_x[i-1]) == step:
        good_end = unique_x[i]
        break

# Если нашли хорошие границы - используем их, иначе берем крайние точки
if good_start is None:
    good_start = unique_x[0]
if good_end is None:
    good_end = unique_x[-1]

# Генерируем сетку
filtered_x = np.arange(good_start, good_end + 1, step) + 1

# for i in unique_x:
#     cv2.line(img,(i,0),(i,500),(150,150,255))
# for i in filtered_x:
#     cv2.line(img,(i,0),(i,500),(255,250,55))
# for i in res_x:
#     cv2.circle(img,i[::-1],1,(0,255,255))
# for i in res_top:
#     cv2.circle(img,i[::-1],1,(0,255,255))
# for i in res_bot:
#     cv2.circle(img,i[::-1],1,(255,255,0))
# for i in res_open:
#     cv2.circle(img,i[::-1],1,(255,200,255))
# for i in res_close:
#     cv2.circle(img,i[::-1],1,(255,100,100))
print(res_top[0])
print(res_bot[0])
print(filtered_x)
bars = []
for x in filtered_x:
    vertical_line = candle_cords[np.where(candle_cords[:,1] == x)]
    if vertical_line.size == 0:
        continue
    high_bar = vertical_line[:,0].min()
    low_bar = vertical_line[:,0].max()
    volume = volume_cords[np.where(volume_cords[:,1] == x)]
    if volume.size > 0:
        volume_bar = volume[:,0].min()
    else:
        volume_bar = None
    close_line = candle_cords[np.where(candle_cords[:,1] == x+1)]
    if close_line.size == 0:
        close_bar = None
    else:
        close_bar = close_line[:,0].max()
    open_line = candle_cords[np.where(candle_cords[:,1] == x-1)]
    if open_line.size == 0:
        open_bar = None
    else:
        open_bar = open_line[:,0].max()
    bars.append([x,high_bar,low_bar,open_bar,close_bar,volume_bar])

bars = pd.DataFrame(bars,columns=['x','high','low','open','close','volume'])
bars['middle'] = (bars['low'] +bars['high']) // 2
bars['open'] = bars['open'].fillna(bars['close'].shift(1))
bars['close'] = bars['close'].fillna(bars['open'].shift(-1))
bars['volume'] = bars['volume'].fillna(bars['volume'].max())
bars['open'] = bars['open'].fillna(bars['middle'])
bars['close'] = bars['close'].fillna(bars['middle'])
bars['direction'] = np.where(bars['open'] >= bars['close'],1,-1)
numeric_cols = bars.select_dtypes(include=['float', 'int']).columns
bars[numeric_cols] = bars[numeric_cols].astype(int)

bars.info()
print(bars.head())
print(bars.tail())

for _, bar in bars.iterrows():
    x = int(bar['x'])
    high = int(bar['high'])
    low = int(bar['low'])
    open_y = int(bar['open'])
    close_y = int(bar['close'])
    close_y = int(bar['close'])
    volume = int(bar['volume'])
    direction = bar['direction']
    if direction == 1:
        cv2.line(img,(x,high),(x,low),(0,255,0))
    else:
        cv2.line(img,(x,high),(x,low),(0,0,255))
    # cv2.circle(img,(x,high),1,(255,0,255))
    # cv2.circle(img,(x,low),1,(255,255,0))
    cv2.circle(img,(x,open_y),1,(200,200,0))
    cv2.circle(img,(x,close_y),2,(200,200,255),-1)
    cv2.circle(img,(x,volume),1,(250,100,155))

# for i in range(res_top.shape[0]):
#     point_b = candle_cords[np.where(candle_cords[:,1] == res_top[i][1])]
#     point_v = volume_cords[np.where(volume_cords[:,1] == res_top[i][1])]
#     y_b = point_b[:,0].max()
#     y_v = point_v[:,0].min()
#     print(point_b)
#     cv2.circle(img,point_b[0][::-1],1,(0,255,255))
#     cv2.circle(img,point_v[0][::-1],1,(255,0,255))
    
is_sorted = bars['x'].is_monotonic_increasing
print(f"X отсортирован: {is_sorted}")
# cv2.imshow('mask',mask)
cv2.imshow('img',img)
# cv2.imshow('mask_v',mask_v)
# cv2.imshow('mask_v2',mask_v2)
# cv2.imshow('mask_cv',cv2.add(mask,mask_v))
cv2.waitKey(0)
cv2.destroyAllWindows()