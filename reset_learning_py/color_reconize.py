import numpy as np 
import functools
import itertools as I
import cv2

def rgb_to_hsv():
    im = cv2.imread('010.png')
    im =cv2.resize(im,(800,600))
    
    # b,g,r = cv2.split(im)
    # cv2.imshow('SOURCE',im)
    print('im:',im.shape)
    imgHSV = np.zeros(im.shape,dtype=np.uint8)
    cv2.cvtColor(im, cv2.COLOR_BGR2HSV,imgHSV)
    # cv2.imshow('HSV',imgHSV)
    print('hsv:',imgHSV[-1,-1])


    #--蓝色0
    lower_blue = np.array([100,43,46])
    upper_blue = np.array([130,255,255])  

    #---红色2
    lower_red = np.array([0,43,46])
    upper_red = np.array([10,255,255])
    ##灰白色----3
    lower_white =np.array([0,0,200])
    upper_white =np.array([180,43,255])
    #--黄色4
    lower_yellow = np.array([26,43,46])
    upper_yellow = np.array([34,255,255])
    #--绿色1
    lower_green = np.array([35,43,46])
    upper_green = np.array([77,255,255])

    mask_white = cv2.inRange(imgHSV,lower_white,upper_white)
    mask_blue = cv2.inRange(imgHSV,lower_blue,upper_blue)
    mask_red = cv2.inRange(imgHSV,lower_red,upper_red)
    mask_yellow = cv2.inRange(imgHSV,lower_yellow,upper_yellow)
    mask_green = cv2.inRange(imgHSV,lower_green,upper_green)

    res_blue = cv2.bitwise_and(im,im,mask=mask_blue)
    res_white = cv2.bitwise_and(im,im,mask=mask_white)
    res_red = cv2.bitwise_and(im,im,mask=mask_red)
    res_yellow = cv2.bitwise_and(im,im,mask=mask_yellow)
    res_green = cv2.bitwise_and(im,im,mask=mask_green)


    result =res_blue.copy()
    giff = res_white > res_blue 
    result[giff] = res_white[giff]
    giff = res_red > result
    result[giff] = res_red[giff]
    giff = res_yellow > result
    result[giff] = res_yellow[giff]
    giff = res_green > result
    result[giff] = res_green[giff]
    print('result:',result[-1,-1])
    cv2.imshow('blue',res_blue)
    cv2.imshow('white',res_white)
    cv2.imshow('red',res_red)
    cv2.imshow('yellow',res_yellow)
    cv2.imshow('green',res_green)
    cv2.imshow('result',result)
    cv2.waitKey()
    lists_low ,lists_up= [], []
    lists_low.extend((lower_blue,lower_green,lower_red,lower_white,lower_yellow))
    lists_up.extend((upper_blue,upper_green,upper_red,upper_white,upper_yellow))

    #//测试输出
    pre = np.zeros((5,),int)
    for index,(a,b) in enumerate(zip(lists_low,lists_up)):
        mask = cv2.inRange(imgHSV,a,b)
        result = cv2.bitwise_and(im,im,mask=mask)
        for i in range(result.shape[0]):
            for j in range(result.shape[1]):
               if any(list(result(i,j))>np.array(0,0,0)):
                   pre[index] +=1
    print(pre)
    # pre = np.zeros((5,),int)
    # yes =False
    # print('low:',lists_low[1])
    # print('up:',lists_up[1])
    # color_nums = len(lists_up)
    # for i in range(result.shape[0]):
    #     for j in range(result.shape[1]):
    #         for color in range(color_nums):
    #             yes =False
    #             for (a,b,c) in zip(lists_low[color],lists_up[color],result[i,j]): 
    #                 if (color==1):
    #                     print(a,b,c)
    #                 if c<a or c >b:
    #                     yes = True
    #             if yes!=True:
    #                 pre[color] +=1
    # print('a:',pre)
if __name__ == '__main__':
    # a =[1,2,3]
    # b =[0,4,2]
    # c = [2,3,4]
    rgb_to_hsv()
    # print(list(I.starmap(lambda x,y,z:z>a and z<y,zip(a,b,c))))