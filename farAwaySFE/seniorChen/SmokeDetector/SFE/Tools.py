# coding: utf-8
import os
from os import path

import cv2
from PyQt5.QtGui import QPixmap, QImage
import numpy as np

from .thirdparty import pyvideostream as vs
from .thirdparty.PyEsegment import segment
from .thirdparty.pyeasypr import plateRecognize


def getPlate(image: np.ndarray):
    ''' 获取车牌、车牌颜色
    return: plate, plate_color
    '''

    plate = plateRecognize(*image.shape, image.tobytes())
    if not plate:
        return "", ""

    plate = plate[0]
    plate = plate.replace("\r", "")
    return [*plate.split(":"), ""][:2][::-1]


def cv2pixmap(img):
    ''' 将 opencv 图片 转为 QPixmap '''
    size = img.shape[1::-1]
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    qi = QImage(rgb.tobytes(), *size, QImage.Format_RGB888)
    return QPixmap.fromImage(qi)


def drawLabel(image, lt, rb, color, label):
    ''' 在图片中用指定颜色画出矩形 并在左上角添加标签 '''
    label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, 1)[0]
    cv2.rectangle(image, lt, rb, color, 2)

    cv2.rectangle(image, lt, (lt[0] + label_size[0] + 3, lt[1] + label_size[1] + 5), color, -1)
    cv2.putText(image, label, (lt[0], lt[1] + label_size[1]), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 0), 1)
