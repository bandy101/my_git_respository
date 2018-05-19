from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import time
import cv2
import numpy as np
class thred(QThread):
    signal =pyqtSignal()
    def __init__(self):
        super(thred,self).__init__()
        # self.frame =frame
        # self.mog = cv2.createBackgroundSubtractorMOG2(detectShadows=True)
    def run(self):
        pass
        # self.signal.emit(self.frame)
        # print('im:')
        # self.signal.emit()
        #     if self.frame is None: return
            
def slot(frame):
    frame_ = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    frame_ = self.mog.apply(frame_)
    _,frame_ = cv2.threshold(frame_,244,255,cv2.THRESH_BINARY)
    frame_ = cv2.morphologyEx(frame_,cv2.MORPH_CLOSE,None,iterations=3)
    area = []
    x= cv2.findContours(frame_,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[1]
    for _1 in x:
        area_ = cv2.contourArea(_1)
        if area_<0 and area_<1000:
            continue
        x,y,w,h = cv2.boundingRect(_1)
        x1,y1 = x+w,y+h 
        if any([w,h]<np.array((20,20))):
            continue
        # print(w,h)
        x,y,x1,y1 = map(int,[x,y,x1,y1])
        # area.append((x,y,x1,y1))
        # return area
    # for _ in ims:
        # x,y,x1,y1 = _
        # im = frame[y:y1,x:x1]
        # is_car = self.model.predict(im)[0]
        # if  is_car:
            # cv2.imshow('im',im)
            # cv2.waitKey()
        # self.recognize_0()
        cv2.rectangle(frame,(x,y),(x1,y1),(0,255,0),2)
    # return frame
class video_op(QThread):
    def __init__(self,device,label):
        super(video_op,self).__init__()
        self.device = device
        self.label = label
        # self.frame = frame
        self.mog = cv2.createBackgroundSubtractorMOG2(detectShadows=True)
    def run(self):
        ret,self.frame = self.device.read()
        self.frame = cv2.resize(self.frame,(800,600))
        print('singal rect')
        th = thred()
        th.signal.connect(self.slot)
        # # cv2.imshow('s',frame)
        while ret:
            # frame = self.frame
            try:
                if  self.frame is not None: 
                    # th.start()
                    # th = thred(self.frame)
                    # th.signal.connect(self.slot)
                    # print(frame)
                    # self.slot(self.frame)
                    th.signal.emit()
                    frame = cv2.cvtColor(self.frame,cv2.COLOR_BGR2RGB)           
                    frame = QImage(frame.tobytes(), frame.shape[1],frame.shape[0], QImage.Format_RGB888)
                    self.label.resize(frame.width(),frame.height())
                    self.label.setPixmap(QPixmap.fromImage(frame))
                    time.sleep(0.08)
                    ret,frame =  self.device.read()
                    self.frame = cv2.resize(frame,(800,600))
            except:
                pass
            # ret,frame =  self.device.read()

    def slot(self):
        frame_ = cv2.cvtColor(self.frame,cv2.COLOR_BGR2GRAY)
        frame_ = self.mog.apply(frame_)
        _,frame_ = cv2.threshold(frame_,244,255,cv2.THRESH_BINARY)
        frame_ = cv2.morphologyEx(frame_,cv2.MORPH_CLOSE,None,iterations=3)
        area = []
        x_= cv2.findContours(frame_,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[1]
        for _1 in x_:
            area_ = cv2.contourArea(_1)
            if area_<0 and area_<1000:
                continue
            x,y,w,h = cv2.boundingRect(_1)
            x1,y1 = x+w,y+h 
            if any([w,h]<np.array((20,20))):
                continue
            # print(w,h)
            x,y,x1,y1 = map(int,[x,y,x1,y1])
            # area.append((x,y,x1,y1))
            # return area
        # for _ in ims:
            # x,y,x1,y1 = _
            # im = frame[y:y1,x:x1]
            # is_car = self.model.predict(im)[0]
            # if  is_car:
                # cv2.imshow('im',im)
                # cv2.waitKey()
            # self.recognize_0()
            cv2.rectangle(self.frame,(x,y),(x1,y1),(0,255,0),2)

                    