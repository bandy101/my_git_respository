import numpy as np
import cv2 as cv

from get_data import *
# from svm_train import svm_config,svm_train,svm_save,svm_load
 
#计算hog特征
def get_hog_object(window_dims):
    blockSize = (8,8) 
    blockSize = (16,16) 
    blockStride = (8,8) 
    cellSize = (8,8) 
    nbins = 9 
    derivAperture = 1 
    winSigma = 4.
    histogramNormType = 0 # 
    # HOGDescriptor::L2Hys 
    L2HysThreshold = 2.0000000000000001e-01 
    gammaCorrection = 0 
    nlevels = 64 
    hog = cv2.HOGDescriptor(window_dims,blockSize,blockStride,cellSize,nbins,derivAperture,winSigma, histogramNormType,L2HysThreshold,gammaCorrection,nlevels) 
    return hog


def cv_imread(f_path):
    img = cv2.imdecode(np.fromfile(f_path,dtype=np.uint8),-1)
    return img
def computeHog(imgs,features,wsize = (128,128)):
    hog = get_hog_object((128,128))
    count = 0
    
    for i in range(len(imgs)):
        # print('imgs[i].shape[1]',imgs[i].shape[1])
        if imgs[i].shape[1] >= wsize[1] and imgs[i].shape[0] >= wsize[0]:
            y = imgs[i].shape[0] - wsize[0]
            x = imgs[i].shape[1] - wsize[1]
            h = imgs[i].shape[0]
            w = imgs[i].shape[1]
            roi = imgs[i][y : y + h, x : x + w]
            # print('hog.compute:',len(hog.compute(roi)))
            features.append(hog.compute(roi))
            count += 1
    print ('count = ',count)
    return features
 
#获取svm参数
def get_svm_detector(svm):
    sv = svm.getSupportVectors()
    rho, _, _ = svm.getDecisionFunction(0)
    sv = np.transpose(sv)
    return np.append(sv,[[-rho]],0)        

#加载hardexample
def get_hard_samples(svm,hog_features,labels):
    hog = get_hog_object((128,128))
    hard_examples = []
    hog.setSVMDetector(get_svm_detector(svm))
    negs,hardlabel= read_neg_samples('C:/Users/NHT/Desktop/car/neg')
    
    for i in range(len(negs)):
        rects,wei = hog.detectMultiScale(negs[i],0,winStride = (8,8),padding = (0,0),scale = 1.05)
        for (x,y,w,h) in rects:
            hardexample = negs[i][y : y + h, x : x + w]
            hard_examples.append(cv.resize(hardexample,(128,128)))
            #(64,128)
    computeHog(hard_examples,hog_features)
    [labels.append(-1) for _ in range(len(hard_examples))]
    svm_train(svm,hog_features,labels)
    hog.setSVMDetector(get_svm_detector(svm))
    hog.save('myHogDector1.bin')
    #svm.train(np.array(hog_features),cv.ml.ROW_SAMPLE,np.array(labels))
 
#获取所有的hog特征
def get_features(features,labels):
    pos_imgs,pos_labels = read_pos_samples('C:/Users/NHT/Desktop/car/pos')
    print('computer:Y',len(pos_labels))
    features = computeHog(pos_imgs,features)
    [labels.append(1) for _ in range(len(pos_imgs))]
    
    neg_imgs,neg_labels = read_neg_samples('C:/Users/NHT/Desktop/car/neg')
    print('neg_type:',len(neg_imgs))
    features = computeHog(neg_imgs,features)
    
    [labels.append(-1) for _ in range(len(neg_imgs))]
 
    #print('feature_shape = ',np.shape(features))
 
    return features,labels
 
#hog训练
def hog_train(svm):
    features = []
    labels = []
    
    # hog = cv.HOGDescriptor()
    hog = get_hog_object((128,128))
    
    #get hog features
    features,labels = get_features(features,labels)
    print('feature:',features[0],len(features[0]))
    print(np.array(features).shape)
    print ('svm training...')
    svm_train(svm,features,labels)
    print ('svm training complete...')
    
    hog.setSVMDetector(get_svm_detector(svm))
    hog.save('myHogDector.bin')
    
    print('hard samples training...')
    get_hard_samples(svm,features,labels)
    print('hard samples complete...')
    
    
if __name__ == '__main__':
    #svm config
    svm = svm_config()
    
    #hog training
    hog_train(svm)