import numpy as np 
import matplotlib.pyplot as plt 
import cv2
import os,shutil
from os import path

#归一化
def normlize(a):
    r = max(a)-min(a)
    a = a-min(a)
    a = a/r
    return a
def get_gray_img(paths,chenel=0):
    print(paths)
    return cv2.cv2.imdecode(np.fromfile(paths,dtype=np.uint8),0)

def get_probility(im1,im2):
    hist0,_ = np.histogram(im1.ravel(),256,[0,256])
    hist1,_ = np.histogram(im2.ravel(),256,[0,256])
    a ,b= normlize(hist0),normlize(hist1)
    BC = sum(np.sqrt(a*b))  
    prob_0 = BC/np.sqrt(sum(a)*sum(b))  #原始巴适距离
    prob_1 = 1-np.sqrt(1-(BC/np.sqrt(sum(a)*sum(b)))) #进行优化
    return prob_1

def start(paths):
    save_img =[ path.join(paths,_) for _ in os.listdir(paths)] #地址
    new_img = save_img.copy()
    k = 0
    while True:
        '''
            相似定义:
                @ONE:两张图片概率 >0.855(优化过的)
                @TWO:
        '''
        #删除相似的图片
        for _ in save_img:
            if _ not in new_img:os.remove(_)
        save_img = new_img.copy()   #深层复制
        im1 = get_gray_img(save_img[k]) #冒泡递增比较
        for i in range(k+1,len(new_img)):
            print('i:',i)
            im2 = get_gray_img(save_img[i])
            # cv2.imshow('im2',im1)
            # cv2.waitKey()
            prob = get_probility(im1,im2)
            print(prob)#概率
            if prob>0.855:             
                new_img.remove(save_img[i])
                # os.remove(save_img[i])
                # print(save_img[i])
        if k>=len(new_img)-1: 
            break
        k = k+1
                
if __name__ =='__main__':
    # kk = './G107好运饲料1号机_20180920131432_028672_1537495221835995_0.jpg'
    im1 = get_gray_img('a1.jpg')
    im2 = get_gray_img('./a2.jpg')
    prob= get_probility(im1,im2)
    print(prob)
    paths = 'H:/分类任务/result/三棵竹一桥(源潭)'
    start(paths)


# if __name__ == '__main__':
#     t0 = cv2.imread('g0.jpg',0)
#     t1 = cv2.imread('g2.jpg',0)
#     hist = cv2.calcHist([t0],[0],None,[256],[0,256])
#     print('shape:',t0.shape[-1],t1.shape[-1])
#     print(len(hist))
#     # print(hist)
#     print(len(t0.ravel()))
#     # cv2.imshow('t0',t0)
#     # cv2.imshow('t1',t1)
#     plt.subplot(221)  
#     plt.hist(t0.ravel(),256,[0,256])
#     plt.subplot(222)  
#     # plt.hist(t0.ravel(),256,[0,256])
#     hist0,_ = np.histogram(t0.ravel(),256,[0,256])
#     ax = hist0/len(t0.ravel())
#     ax = hist0/sum(hist0)
#     print('len(t0.ravel()):',len(t0.ravel()),sum(hist0))
#     hist1,_ = np.histogram(t1.ravel(),256,[0,256])
#     bx = hist1/len(t1.ravel())
#     bx = hist1/sum(hist1)
#     print('probility:',sum(np.sqrt(ax*bx)))
#     # print('probility:', 1+np.log(sum(np.sqrt(ax*bx))))]
    
#     hist_0 = cv2.calcHist([t0],[0],None,[256],[0,256])
#     hist_1 = cv2.calcHist([t1],[0],None,[256],[0,256])
#     a = normlize(hist0)
#     b = normlize(hist1)


#     # print ('hist:',a,b)
#     # print(a,b)
#     BC = sum(np.sqrt(a*b))  
#     print('bc:',BC,1-BC)
#     print(-np.log(BC))
#     print(BC/np.sqrt(sum(a)*sum(b)))
#     print(1-np.sqrt(1-(BC/np.sqrt(sum(a)*sum(b)))))
#     # print('hist',hist.shape)
#     # print(hist)
#     # bins=np.bincount(t1.ravel(),minlength=256)
#     plt.hist(t1.ravel(),256,[0,256])
#     # plt.subplot(223)  
#     # plt.plot(bins)  
#     plt.show()
#     cv2.waitKey()