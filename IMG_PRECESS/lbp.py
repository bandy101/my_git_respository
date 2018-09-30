import cv2
import numpy as np 

from thirdparty.PyEsegment import segment

def get_neighbor(mat,i,j):
    center = mat[i,j][-1]
    x1,y1= i+1,j+1
    result = 0
    for k in range(8):
        result = result + (mat[x1,y1][-1]>center)*(1<<k)
        if y1-j>=0:
            y1 =y1-1
        else:
            x1,y1 = x1 -1,j+1
        if (x1,y1) in [(i,j)]:y1 = y1-1
    return result

def LBP(img):
    dst = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    mat = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    h,w = dst.shape
    for i in range(1,h-1):
        for j in range(1,w-1):
            dst[i,j] =get_neighbor(mat,i,j)
    return dst


if __name__ == '__main__':
    im = cv2.imread('g0.jpg')
    r = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    mask1 = segment(r.tobytes(), r.shape, 0.35, 200, 10)
    mask1 = np.frombuffer(r, np.uint8)
    dst = LBP(im)
    frame = cv2.threshold(r, 180, 255, cv2.THRESH_BINARY)[1]
    cv2.imshow('src',im)
    cv2.imshow('lbp',dst)
    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask1)
    cv2.waitKey()