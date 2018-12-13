import requests
import traceback
import os,random,re
from os import path
import json
import datetime,time
import shutil
from concurrent.futures import ThreadPoolExecutor,ALL_COMPLETED,wait,FIRST_COMPLETED
import numpy as np
import cv2

def cv_imread(f_path):
    img = cv2.imdecode(np.fromfile(f_path,dtype=np.uint8),-1) # -1 彩色,0 灰度图
    return img

def cv_imwrite(f_path,im):
    cv2.imencode('.jpg',im)[1].tofile(f_path)#保存图片