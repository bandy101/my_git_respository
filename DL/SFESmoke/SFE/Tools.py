# coding: utf-8
import os
from os import path
import sys
import shutil

import cv2
import numpy as np

from .thirdparty import pyvideostream as vs
from .thirdparty.PyEsegment import segment
from .thirdparty.pythplateid import plateRecognize


PLATE_TYPE = {
    "0": "其他",  # 99 其他
    "1": "小型汽车",  # 02 小型汽车号牌 （蓝牌）
    "2": "外籍汽车",  # 06 黑牌，涉外机构车牌
    "3": "大型汽车",  # 01 大型汽车号牌（前号牌）和教练车牌
    "4": "大型汽车",  # 01/15 大型汽车号牌 （后号牌）和挂车号牌
    "5": "警用汽车",  # 23 警用汽车前后号牌
    "6": "警用汽车",  # ? 23 单层武警车号牌和双层武警车号牌
    "7": "小型汽车",  # ? 02 式个性化车牌
    "8": "警用汽车",  # ? 23 单层军车号牌
    "9": "警用汽车",  # ? 23 双层军车号牌
    "10": "使馆汽车",  # 03 使馆牌
    "11": "境外汽车",  # ? 05 香港入出境车号牌
    "12": "拖拉机",  # 14 拖拉机号牌（农用车）
    "13": "境外汽车",  # ? 05澳门入出境车号牌
    "14": "小型汽车",  # ? 02 厂内牌
    "15": "小型汽车",  # ? 02 民航牌
    "16": "领馆汽车",  # 04 领馆牌
    "17": "小型新能源汽车",  # ? 52 新能源牌
}


def getPlate(image: np.ndarray):
    ''' 获取车牌、车牌颜色、车牌类型
    return: plate, plate_color, plate_type
    '''

    plate = plateRecognize(*image.shape, image.tobytes())
    if not plate:
        return "", "", ""
    plate, color, _type = plate[0].split(":")
    _type = PLATE_TYPE.get(_type, "其他")
    return plate, color, _type


def drawLabel(image, lt, rb, color, label=None):
    ''' 在图片中用指定颜色画出矩形 并在左上角添加标签 '''
    cv2.rectangle(image, lt, rb, color, 2)

    if label:
        label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, 1)[0]
        cv2.rectangle(image, lt, (lt[0] + label_size[0] + 3, lt[1] + label_size[1] + 5), color, -1)
        cv2.putText(image, label, (lt[0], lt[1] + label_size[1]), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 0), 1)
