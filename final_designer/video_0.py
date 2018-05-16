from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from DL import BaseModel
from DL import Dataset
from DL import Net
import numpy as np
import sys,os
import cv2
from os import path
from video_ui import Ui_MainWindow
from time import sleep
from threading import Thread
from hyperlpr import pipline as pp 
from queue import Queue as Q

class Gui(QMainWindow,Ui_MainWindow):
    '''
    继承designer UI
    '''
    num , i = -1 , 0
    mog = cv2.createBackgroundSubtractorMOG2(detectShadows=True)  #目标追踪
    def __init__(self):
        super(Gui,self).__init__()
        self.setupUi(self)
        self.table_set()
        self.bt1.clicked.connect(self.slot)
        self.bt2.clicked.connect(self.slot_2)
        self.bt_recognize.clicked.connect(self.recognize)
        # fourcc = cv2.CV_FOURCC(*'MPJG')  
        self.writer = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc('D', 'I', 'V', 'X'),20,(800,600))
        self.R_video = Q(maxsize=20*60)
        self.model = Net()
        assert self.model.load('car.h5'), '加载错误'

    def table_set(self):
        self.model_t= QStandardItemModel()
        self.model_t.setColumnCount(1)
        self.tableView.horizontalHeader().setStretchLastSection(True)    
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.model_t.setHorizontalHeaderLabels(['车牌识别'])
        self.tableView.setModel(self.model_t)
    
    def recognize_0(self):
        _,res = pp.SimpleRecognizePlate(self.frame_)
        if not len(res):
            # res.append('无效的图片')
            return
        value = self.model_t.data(self.model_t.index(self.i-1,0))
        if value == res[0]:
            return 
        item = QStandardItem(res[0])
        
        self.model_t.setItem(self.i,0,item)
        self.i +=1


    def recognize(self):
        self.timer.stop()
        from hyperlpr import pipline as pp 
        cv2.imshow('i',self.frame_)
        cv2.waitKey()
        _,res = pp.SimpleRecognizePlate(self.frame_)
        if not len(res):
            res.append('无效的图片')
        item = QStandardItem(res[0])
        self.model_t.setItem(self.i,0,item)
        self.i +=1
        # self.timer = QTimer()
        # self.timer.timeout.connect(self.videoplay)
        # self.timer.start(10)

    def slot(self):
        try:
            path = QFileDialog.getOpenFileNames(self,'打开视频文件','/')[0][0]
            self.num = 0
        except:
            self.num = -1
            return
        print(path)
        self.device = cv2.VideoCapture(path)
        self.timer = QTimer()
        self.timer.timeout.connect(self.videoplay)
        self.timer.start(10)
    
    def slot_2(self):
        if self.num == -1:
            return
        self.num+=1
        if self.num%2:
            self.timer.stop()
            while not self.R_video.empty():
                # print('write:',self.R_video.get(0))
                x = self.R_video.get()
                self.writer.write(x)
                
                # cv2.imshow('quenn',self.R_video.get())
                # cv2.waitKey()
            print('保存完毕')
            self.bt2.setText('播放')
        else:
            self.bt2.setText('暂停')
            self.timer = QTimer()
            self.timer.timeout.connect(self.videoplay)
            self.timer.start(10)

    def videoplay(self):

        ret,self.frame = self.device.read()
        
        self.frame = cv2.resize(self.frame,(800,600))
        self.frame_ =self.frame.copy()
        if self.R_video.full():
            self.R_video.get()
            self.R_video.put(self.frame)
        else:
            self.R_video.put(self.frame)
    
        # cv2.imshow('test', frame)
        # cv2.waitKey()
        # print(ret)  True/False
        ims = self.move_frame(self.frame,self.mog)   #返回的轮廓
        # print(ims.shape)
        for _ in ims:
            x,y,x1,y1 = _
            im = self.frame[y:y1,x:x1]
            is_car = self.model.predict(im)[0]
            if  is_car:
                # cv2.imshow('im',im)
                # cv2.waitKey()
                self.recognize_0()
                cv2.rectangle(self.frame,(x,y),(x1,y1),(0,255,0),2)
        self.frame = cv2.cvtColor(self.frame,cv2.COLOR_BGR2RGB)           
        self.frame = QImage(self.frame.tobytes(), self.frame.shape[1],self.frame.shape[0], QImage.Format_RGB888)
        self.label.resize(self.frame.width(),self.frame.height())
        self.label.setPixmap(QPixmap.fromImage(self.frame))

    def move_frame(self,frame,mog):
        frame_ = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        frame_ = mog.apply(frame_)
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
            area.append((x,y,x1,y1))
        return area