import cv2 as cv
import random
import glob
import os
import numpy as np
import cv2
#加载负样本
def get_neg_samples(foldername,savePath):
    count = 0
    imgs = []
    labels = []
    f = open('neg.txt')
    filenames = glob.iglob(os.path.join(foldername,'*'))
    for filename in filenames:
        print('filename = ',filename)
        src = cv.imread(filename,1)
        
        if((src.cols >= 64) & (src.rows >= 128)):
            x = random.uniform(0,src.cols - 64)
            y = random.uniform(0,src.rows - 128)
            
            imgRoi = src(cv.Rect(x,y,64,128))
            imgs.append(imgRoi)
            saveName = savePath + 'neg' + str(count) + '.jpg'
            cv.imwrite(saveName,imgRoi)
            
            label = 'neg' + str(count) + '.jpg'
            labels.append(label)
            label = label + '\n'
            f.write(label)
            count += 1
    return imgs,labels
 
 
#读取负样本
def read_neg_samples(foldername):
    imgs = []
    labels = []
    neg_count = 0
    filenames = glob.iglob(os.path.join(foldername,'*'))
    for filename in filenames:
       # print('filename = ',filename)
        src = cv_imread(filename)
       # cv.imshow("src",src)
       # cv.waitKey(5)
        imgs.append(src)
        labels.append(-1)
        neg_count += 1
   
    #print ('neg_count = ',neg_count)     
    return imgs,labels
        
        
 
#加载正样本
def get_pos_samples(foldername,savePath):
    count = 0
    imgs = []
    labels = []
    f = open('pos.txt')
    filenames = glob.iglob(os.path.join(foldername,'*'))
    for filename in filenames:
        print('filename = ',filename)
        src = cv.imread(filename)
        imgRoi = src(cv.Rect(16,16,64,128))
        imgs.append(imgRoi)
        saveName = savePath + 'neg' + str(count) + '.jpg'
        cv.imwrite(saveName,imgRoi)
        
        label = 'neg' + str(count) + '.jpg'
        labels.append(label)
        f.write(label)
        count += 1
        
    return imgs,labels
def cv_imread(f_path):
    img = cv2.imdecode(np.fromfile(f_path,dtype=np.uint8),-1)
    return img
 
#读取正样本
def read_pos_samples(foldername):
    imgs = []
    labels = []
    pos_count = 0
    filenames = glob.iglob(os.path.join(foldername,'*'))
    
    for filename in filenames:
        src = cv_imread(filename)
        imgs.append(src)
        labels.append(1)
        pos_count += 1
     
    return imgs,labels



def svm_config():
    svm = cv.ml.SVM_create()
    svm.setCoef0(0)
    svm.setCoef0(0.0)
    svm.setDegree(3)
    criteria = (cv.TERM_CRITERIA_MAX_ITER + cv.TERM_CRITERIA_EPS, 1000, 1e-3)
    svm.setTermCriteria(criteria)
    svm.setGamma(0)
    svm.setKernel(cv.ml.SVM_LINEAR)
    svm.setNu(0.5)
    svm.setP(0.1)
    svm.setC(0.01)
    svm.setType(cv.ml.SVM_EPS_SVR)
 
    return svm
 
#svm训练
def svm_train(svm,features,labels):
    svm.train(np.array(features),cv.ml.ROW_SAMPLE,np.array(labels))
    
#svm参数保存
def svm_save(svm,name):
    svm.save(name)
        
#svm加载参数 
def svm_load(name):
    svm = cv.ml.SVM_load(name)
    
    return svm
