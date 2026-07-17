import cv2
import os

folder = 'DataForTests\ImgCs'
ld = os.listdir(folder)
for i in ld:
    img = cv2.imread(os.path.join(folder,i))
# img = cv2.imread('DataForTests\ImgCs\Z_problem.png')

    color = (118,118,118)
    mask = cv2.inRange(img,color,color)

    cv2.imshow(i,mask)
    cv2.waitKey(0)