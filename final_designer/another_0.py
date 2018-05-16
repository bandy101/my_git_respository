#coding utf-8
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from another_ui import Ui_MainWindow
import os
import cv2
from os import path
import numpy as np 
class Gui_(QMainWindow,Ui_MainWindow):
    i = 0
    def __init__(self):
        super(Gui_,self).__init__()
        self.setupUi(self)
        self.table_set()
        self.bt_files.clicked.connect(self.recognize)
        
    # @property
    def opFile(self):
        try:
            # path = QFileDialog.getOpenFileName(self,'打开测试文件夹','')[0]
            path = QFileDialog.getExistingDirectory(self,'打开测试文件夹','.')
            print(path)
        except:
            return
        return path
    
    def table_set(self):
        self.model_t= QStandardItemModel()
        self.model_t.setColumnCount(1)
        self.tableView.horizontalHeader().setStretchLastSection(True)    
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.model_t.setHorizontalHeaderLabels(['车牌识别'])
        self.tableView.setModel(self.model_t)

    #读取中文路径
    def cv_imread_0(self,file_path = ""):
        file_path_gbk = file_path.encode('gbk')        # unicode转gbk，字符串变为字节数组
        print(file_path_gbk)
        img_mat = cv2.imread(file_path_gbk)  # 字节数组直接转字符串，不解码
        return img_mat

    def cv_imread(self,f_path):
        img = cv2.imdecode(np.fromfile(f_path,dtype=np.uint8),-1)
        return img

    def recognize(self):
        self.path = self.opFile()
        from hyperlpr import pipline as pp 
        print(len(self.img_L())) 
        for _ in self.img_L():
            path_im = path.join(self.path,_)
            im = self.cv_imread(path_im)
            img,res = pp.SimpleRecognizePlate(im)
            self.frame = img
            if not len(res):
                res.append('无效的图片')
            for n in res:
                item = QStandardItem(n)
                self.model_t.setItem(self.i,0,item)
                self.i += 1

        self.frame = cv2.cvtColor(self.frame,cv2.COLOR_BGR2RGB)           
        self.frame = QImage(self.frame.tobytes(), self.frame.shape[1],self.frame.shape[0], QImage.Format_RGB888)
        # self.label.resize(self.frame.width(),self.frame.height())
        self.label.setPixmap(QPixmap.fromImage(self.frame))

    def img_L(self):
        # path_ = self.opFile()
        names = [i for i in os.listdir(self.path)]
        return names
        # for _ in len(names):
        #     
            
