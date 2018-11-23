# uncompyle6 version 3.2.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: .\SFE\Tools.py
# Compiled at: 2018-11-02 11:51:19
# Size of source mod 2**32: 1039 bytes
import os
from os import path
import sys, shutil, cv2, numpy as np
from .thirdparty import pyvideostream as vs
from .thirdparty.PyEsegment import segment
from .thirdparty.pyeasypr import plateRecognize

def getPlate(image):
    """ 获取车牌、车牌颜色
    return: plate, plate_color
    """
    plate = plateRecognize(*image.shape, *(image.tobytes(),))
    if not plate:
        return ('', '')
    else:
        plate = plate[0]
        plate = plate.replace('\r', '')
        return [
         plate.split(':'), ('', )][:2][::-1]


def drawLabel(image, lt, rb, color, label=None):
    """ 在图片中用指定颜色画出矩形 并在左上角添加标签 """
    cv2.rectangle(image, lt, rb, color, 2)
    if label:
        label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, 1)[0]
        cv2.rectangle(image, lt, (lt[0] + label_size[0] + 3, lt[1] + label_size[1] + 5), color, -1)
        cv2.putText(image, label, (lt[0], lt[1] + label_size[1]), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,
                                                                                                      0,
                                                                                                      0), 1)
# okay decompiling SFE\Tools.pyc
