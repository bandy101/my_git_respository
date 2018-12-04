# coding: utf-8
import os
from os import path
from collections import defaultdict
import math
from enum import Enum
import gc

import cv2
import numpy as np


class COLOR_RANGE(Enum):
    # http://blog.csdn.net/taily_duan/article/details/51506776
    黑 = (
        ((0, 0, 0), (180, 255, 46)),
    )
    灰 = (
        ((0, 0, 46), (180, 43, 220)),
    )
    白 = (
        ((0, 0, 221), (180, 30, 255)),
    )
    红 = (
        ((0, 43, 46), (10, 255, 255)),
        ((156, 43, 46), (180, 255, 255)),
    )
    橙 = (
        ((11, 43, 46), (25, 255, 255)),
    )
    黄 = (
        ((26, 43, 46), (34, 255, 255)),
    )
    绿 = (
        ((35, 43, 46), (77, 255, 255)),
        ((78, 43, 46), (99, 255, 255)),
    )
    蓝 = (
        ((100, 43, 46), (124, 255, 255)),
    )
    紫 = (
        ((125, 43, 46), (155, 255, 255)),
    )
    其他 = tuple()


color_weight = defaultdict(lambda: 1)
color_weight[COLOR_RANGE.灰] = 0.7
color_weight[COLOR_RANGE.黑] = 0.8
color_weight[COLOR_RANGE.蓝] = 0.9


def getColor(img, filter_zero=True) -> COLOR_RANGE:
    """ 获取图片的主要颜色
    - img: BGR格式的图像
    - filter_zero bool[True]: 是否排除图片中的零值

    - return COLOR_RANGE
    """

    if filter_zero:
        img = img[np.all(img != 0, 2)]
    if len(img) == 0:
        return COLOR_RANGE.其他
    img = img.reshape(-1, 1, 3)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    result = defaultdict(int)
    for color in COLOR_RANGE:
        for hsv_min, hsv_max in color.value:
            r = cv2.inRange(img, hsv_min, hsv_max).reshape(-1)
            result[color] += len(r[r > 0]) * color_weight[color]

    ret = max(result, key=lambda x: result[x]).name
    return ret


def grabForeground(img, size=(100, 100)):
    """ 抓去前景图像
    - img: BGR格式的图像
    - size tuple[(100, 100)]: 将图片缩放到指定大小 为`None`时不缩放

    - return: 返回BGR格式的图像 背景会被设置为0
    """

    h, w = map(lambda x: math.ceil(x / 10), img.shape[:2])
    img = img[h:-h, w:-w]
    if size:
        img = cv2.resize(img, size)
    return img

    # if size:
    #     img = cv2.resize(img, size)
    # else:
    #     img = img.copy()

    # h, w = map(lambda x: math.ceil(x / 100), img.shape[:2])

    # # 生成掩码
    # # 所有区域初始化为背景区域
    # mask = np.full(img.shape[:2], cv2.GC_BGD, np.uint8)
    # for segment, value in (
    #     (1, cv2.GC_PR_BGD),     # 1%~99% 设置为可能背景区域
    #     (10, cv2.GC_PR_FGD),    # 10~90% 设置为可能前景区域
    # ):
    #     hv, wv = segment * h, segment * w
    #     mask[hv:-hv, wv:-wv] = value

    # # 抓取前景物体
    # mask, fg, bg = cv2.grabCut(img,  mask, (0, 0, *mask.shape[::-1]), np.zeros((1, 65)), np.zeros((1, 65)), 1, cv2.GC_INIT_WITH_MASK)

    # # 将背景、可能背景区域置为0
    # img[mask == cv2.GC_BGD] = 0
    # img[mask == cv2.GC_PR_BGD] = 0

    # return img


def getForegroundColor(img) -> COLOR_RANGE:
    """ 获取图像的前景颜色
    - img: BGR格式的图像

    - return COLOR_RANGE
    """
    return getColor(grabForeground(img))


if __name__ == "__main__":
    # testColor()
    img_path = "E:/workspace/SmokeDetector/SFE/resource/car/source/train_data/yes/"

    for img in os.listdir(img_path):
        img = path.join(img_path, img)

        # 读取图片
        img = cv2.imread(img)
        cv2.imshow("src", img)
        # 获取前景图
        fg = grabForeground(img)
        cv2.imshow("fg", fg)

        print("fg:", getColor(fg))

        cv2.waitKey()
        cv2.destroyAllWindows()
