import numpy as np 
import matplotlib.pyplot as plt 
import cv2

def normlize(a):
    r = max(a)-min(a)
    a = a-min(a)
    a = a/r
    return a
if __name__ == '__main__':
    t0 = cv2.imread('1.jpg',0)
    t1 = cv2.imread('2.jpg',0)
    hist = cv2.calcHist([t0],[0],None,[256],[0,256])
    print('shape:',t0.shape)
    print(len(hist))
    # print(hist)
    print(len(t0.ravel()))
    # cv2.imshow('t0',t0)
    # cv2.imshow('t1',t1)
    plt.subplot(221)  
    plt.hist(t0.ravel(),256,[0,256])
    plt.subplot(222)  
    # plt.hist(t0.ravel(),256,[0,256])
    hist0,_ = np.histogram(t0.ravel(),256,[0,256])
    ax = hist0/len(t0.ravel())
    print('len(t0.ravel()):',len(t0.ravel()))
    hist1,_ = np.histogram(t1.ravel(),256,[0,256])
    bx = hist1/len(t1.ravel())
    print('probility:',sum(np.sqrt(ax*bx)))
    # print('probility:', 1+np.log(sum(np.sqrt(ax*bx))))]

    hist_0 = cv2.calcHist([t0],[0],None,[256],[0,256])
    hist_1 = cv2.calcHist([t1],[0],None,[256],[0,256])
    a = normlize(hist0)
    b = normlize(hist1)


    # print ('hist:',a,b)
    # print(a,b)
    BC = sum(np.sqrt(a*b))  
    print('bc:',BC,1-BC)
    print(-np.log(BC))
    print(1-np.sqrt(1-(BC/np.sqrt(sum(a)*sum(b)))))
    # print('hist',hist.shape)
    # print(hist)
    # bins=np.bincount(t1.ravel(),minlength=256)
    plt.hist(t1.ravel(),256,[0,256])
    # plt.subplot(223)  
    # plt.plot(bins)  
    plt.show()
    cv2.waitKey()