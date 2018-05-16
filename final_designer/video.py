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
from video_0 import Gui
from time import sleep
from threading import Thread
from another_0 import Gui_

app = QApplication(sys.argv)

class another(Gui_):
    def __init__(self):
        super(another,self).__init__()
        
class Video(Gui):

    def __init__(self,parent=None):
        super(Video,self).__init__()
        
        self.one_recognize.clicked.connect(self.show_ant)
        # self.x.bt_files.clicked.connect(self.slot)
    def show_ant(self):
        self.x = another()
        self.x.show()
        # app.exec_()
    


def main():
    x = Video()
    x.show()
    sys.exit(app.exec_())
if __name__=='__main__':
    main()