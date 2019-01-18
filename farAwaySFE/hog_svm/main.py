import numpy as np
import cv2 as cv
from _op import py_cpu_nms 
from imutils.object_detection import non_max_suppression
import cv2

from demo import get_hog_object
# hog = get_hog_object((128*128))
hog =  cv2.HOGDescriptor()
hog.load('myHogDector1.bin')
 

# img = cv.imread('../mine/0.jpg')

cam = cv2.VideoCapture('../mine/video/qd_04.mp4')
ret = cam.isOpened()
width, height= cam.get(3), cam.get(4)
_height = 600
_width =int(width*_height/height)
while ret:
    ret, img = cam.read()
    img = cv2.resize(img,(_width,_height))

# cv.imshow('src',img)
# cv.waitKey(10)
 


    rects,scores = hog.detectMultiScale(img,winStride = (8,8),padding = (0,0),scale = 1.05)
    
    sc = [score[0] for score in scores]
    sc = np.array(sc)
    
    #转换下输出格式(x,y,w,h) -> (x1,y1,x2,y2)
    for i in range(len(rects)):
        r = rects[i]
        rects[i][2] = r[0] + r[2]
        rects[i][3] = r[1] + r[3]
    
    
    pick = []
    #非极大值移植  
    print('rects_len',len(rects))
    pick = non_max_suppression(rects, probs = sc, overlapThresh = 0.3)
    print('pick_len = ',len(pick))
    
    #画出矩形框
    for (x,y,xx,yy) in pick:
        cv.rectangle(img, (x, y), (xx, yy), (0, 0, 255), 2)    
    
    cv.imshow('a', img)  
    if cv2.waitKey() == ord('q'):
        break