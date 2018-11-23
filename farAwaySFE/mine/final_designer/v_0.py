from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from DL import BaseModel
from DL import Dataset
from DL import Net
import numpy as np
import sys,os,time
import cv2
from os import path
from video_ui import Ui_MainWindow
from time import sleep
from threading import Thread
from hyperlpr import pipline as pp 
from queue import Queue as Q
from threading import Thread
from videothread import video_op as T_sings
from videothread import thred
app = QApplication(sys.argv)


class GUI(QMainWindow,Ui_MainWindow):
    '''
        继承video_ui UI
    '''
    def __init__(self):
        super(GUI,self).__init__()
        self.setupUi(self)
        self.bt1.clicked.connect(self.main)
        self.frame_fifo = Q()
 
    def slot(self):
        
        self.device =self.op_path()
        self.timer = QTimer()
        self.timer.timeout.connect(self.video)
        self.timer.start(20)
    def main(self):
        self.device =self.op_path()
        x = Thread(target=self.save_frame)
        x.setDaemon(True)
        x.start()
        x_1 = Thread(target=self.have_frame)    
        x_1.setDaemon(True)
        x_1.start()
        # x.join()
        # x_1.join()
    def save_frame(self):
        ret,frame = self.device.read()
        while ret:
            frame = cv2.resize(frame,(800,600))
            # self.bf_0 = T_sings(self.device,self.label,frame)
            # self.bf_0.start()
            self.frame_fifo.put(frame)
            ret,frame = self.device.read()
            frame = cv2.resize(frame,(800,600))
    def have_frame(self):
        while True:
            frame =self.frame_fifo.get()
            self.bf_0 = T_sings(self.device,self.label,frame)
            self.bf_0.start()
    def op_path(self):
        try:
            path = QFileDialog.getOpenFileNames(self,'打开视频文件','/')[0][0]
        except:
            return
        print(path)
        device = cv2.VideoCapture(path)
        return device

    
if __name__ == '__main__':
    mat =GUI()
    mat.show()
    sys.exit(app.exec_())