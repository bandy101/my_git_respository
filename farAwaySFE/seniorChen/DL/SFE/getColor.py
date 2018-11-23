# uncompyle6 version 3.2.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: .\SFE\getColor.py
# Compiled at: 2018-11-02 11:51:19
# Size of source mod 2**32: 3638 bytes
import os
from os import path
from collections import defaultdict
import math
from enum import Enum
import gc, cv2, numpy as np

class COLOR_RANGE(Enum):
    �� = (((0, 0, 0), (180, 255, 46)), )
    �� = (((0, 0, 46), (180, 43, 220)), )
    �� = (((0, 0, 221), (180, 30, 255)), )
    �� = (((0, 43, 46), (10, 255, 255)), ((156, 43, 46), (180, 255, 255)))
    �� = (((11, 43, 46), (25, 255, 255)), )
    �� = (((26, 43, 46), (34, 255, 255)), )
    �� = (((35, 43, 46), (77, 255, 255)), ((78, 43, 46), (99, 255, 255)))
    �� = (((100, 43, 46), (124, 255, 255)), )
    �� = (((125, 43, 46), (155, 255, 255)), )
    ���� = tuple()


color_weight = defaultdict(lambda : 1)
color_weight[COLOR_RANGE.��] = 0.7
color_weight[COLOR_RANGE.��] = 0.8
color_weight[COLOR_RANGE.��] = 0.9

def getColor(img, filter_zero=True):
    """ ��ȡͼƬ����Ҫ��ɫ
    - img: BGR��ʽ��ͼ��
    - filter_zero bool[True]: �Ƿ��ų�ͼƬ�е���ֵ
    
    - return COLOR_RANGE
    """
    if filter_zero:
        img = img[np.all(img != 0, 2)]
    if len(img) == 0:
        return COLOR_RANGE.����
    else:
        img = img.reshape(-1, 1, 3)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        result = defaultdict(int)
        for color in COLOR_RANGE:
            for hsv_min, hsv_max in color.value:
                r = cv2.inRange(img, hsv_min, hsv_max).reshape(-1)
                result[color] += len(r[r > 0]) * color_weight[color]

        ret = (max(result, key=lambda x: result[x])).name
        return ret


def grabForeground(img, size=(100, 100)):
    """ ץȥǰ��ͼ��
    - img: BGR��ʽ��ͼ��
    - size tuple[(100, 100)]: ��ͼƬ���ŵ�ָ����С Ϊ`None`ʱ������
    
    - return: ����BGR��ʽ��ͼ�� �����ᱻ����Ϊ0
    """
    h, w = map(lambda x: math.ceil(x / 10), img.shape[:2])
    img = img[h:-h, w:-w]
    if size:
        img = cv2.resize(img, size)
    return img


def getForegroundColor(img):
    """ ��ȡͼ���ǰ����ɫ
    - img: BGR��ʽ��ͼ��
    
    - return COLOR_RANGE
    """
    return getColor(grabForeground(img))


if __name__ == '__main__':
    img_path = 'E:/workspace/SmokeDetector/SFE/resource/car/source/train_data/yes/'
    for img in os.listdir(img_path):
        img = path.join(img_path, img)
        img = cv2.imread(img)
        cv2.imshow('src', img)
        fg = grabForeground(img)
        cv2.imshow('fg', fg)
        print('fg:', getColor(fg))
        cv2.waitKey()
        cv2.destroyAllWindows()
# okay decompiling SFE\getColor.pyc
