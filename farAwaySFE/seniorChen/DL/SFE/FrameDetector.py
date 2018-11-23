# uncompyle6 version 3.2.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: .\SFE\FrameDetector.py
# Compiled at: 2018-11-02 11:51:19
# Size of source mod 2**32: 7344 bytes
from os import path
import cv2
from datetime import datetime
import numpy as np, tensorflow as tf
from .GrabObject import GrabObject
from .DL.Net import Net
from .DL.VehicleModel import VehicleModel

class DetectResult:

    def __init__(self):
        self.check_time = datetime.now()
        self.is_car = 0
        self._DetectResult__car_rect = None
        self.lane_no = 0
        self.is_smoke = False
        self.smoke_rect = None
        self.r = 0
        self.point = None
        self.is_recognize_plate = False
        self.frame = None

    @property
    def car_rect(self):
        return self._DetectResult__car_rect

    @car_rect.setter
    def car_rect(self, value):
        self._DetectResult__car_rect = value
        (x, y), (x2, y2) = self.car_rect
        w = int((x2 - x) / 2)
        h = int((y2 - y) / 2)
        x3 = max(x - w, 0)
        x4 = x2 + w
        y3 = max(y - h, 0)
        y4 = y2 + h
        self.smoke_rect = ((x3, y3), (x4, y4))
        self.point = np.array([(x + x2) / 2, (y + y2) / 2])
        xd, yd = self.point - (x, y)
        self.r = min(xd, yd) ** 2

    @property
    def car_img(self):
        """ 获取该对象的车辆ROI """
        if self.car_rect is None or self.frame is None:
            return
        else:
            (x, y), (x2, y2) = self.car_rect
            return self.frame[y:y2, x:x2]

    @property
    def smoke_img(self):
        """ 返回该对象的黑烟ROI """
        if self.car_rect is None or self.frame is None:
            return
        else:
            (x, y), (x2, y2) = self.car_rect
            (x3, y3), (x4, y4) = self.smoke_rect
            x, x2 = x - x3, x2 - x3
            y, y2 = y - y3, y2 - y3
            img = self.frame[y3:y4, x3:x4].copy()
            img[y:y2, x:x2] = 0
            return img

    def inR(self, value):
        """ 判断指定对象的中心点是否位于自身`r`范围内
        - value DetectResult: 要判断的对象
        
        - return bool: 返回是否在范围之内
        """
        distance = np.sum((value.point - self.point) ** 2)
        return self.r >= distance


class FrameDetector:
    _FrameDetector__plate_line_up = 0.2
    _FrameDetector__plate_line_down = 0.9
    _FrameDetector__recognize_top_board = 0.2

    def __init__(self, size, model_path, border):
        """
        - size tuple: 帧大小
        - model_path str: 模型所在目录
        - border list: 有两个元素 分别存放上边界坐标、下边界坐标
        """
        w, h = size
        if 0 <= self._FrameDetector__recognize_top_board <= 1:
            self._FrameDetector__recognize_top_board *= h
        self._FrameDetector__plate_line_up *= h
        self._FrameDetector__plate_line_down *= h
        if not border or all(border) is False:
            border = [[[0, 0], [100, 0]],
             [
              [
               0, 100], [100, 100]]]
        up_border, down_border = border
        if not len(up_border) == len(down_border):
            raise AssertionError('上下边界成员数必须相同')
        up_border.sort()
        down_border.sort()
        self._FrameDetector__xfun_list = []
        for (x1, y1), (x2, y2) in zip(up_border, down_border):
            x1, y1, x2, y2 = map(lambda x: x / 100, (x1, y1, x2, y2))
            x1, x2 = x1 * w, x2 * w
            y1, y2 = y1 * h, y2 * h
            self._FrameDetector__xfun_list.append(self._FrameDetector__getXFunc(x1, y1, x2, y2))

        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        self._FrameDetector__sess = tf.Session(config=config)
        self._FrameDetector__car_model = VehicleModel(self._FrameDetector__sess)
        self._FrameDetector__smoke_model = Net(self._FrameDetector__sess)
        if not self._FrameDetector__car_model.load(path.join(model_path, 'vehicle.h5')):
            raise AssertionError('初始化汽车识别模型失败')
        if not self._FrameDetector__smoke_model.load(path.join(model_path, 'smoke.h5')):
            raise AssertionError('初始化黑烟识别模型失败')
        self._FrameDetector__bg = GrabObject(size)
        self.bg_frame = None

    def __del__(self):
        self._FrameDetector__sess.close()

    def inRegion(self, rect):
        """ 判断指定矩形是否处于识别范围 """
        (x, y), (x2, y2) = rect
        if y2 <= self._FrameDetector__recognize_top_board:
            return False
        else:
            cx, cy = np.array([(x + x2) / 2, (y + y2) / 2])
            return self._FrameDetector__xfun_list[0](cy) <= cx <= self._FrameDetector__xfun_list[-1](cy)

    def getLaneNo(self, cx, cy):
        """ 判断指定点所在的车道 """
        min_x = self._FrameDetector__xfun_list[0](cy)
        for idx, max_f in enumerate(self._FrameDetector__xfun_list[1:]):
            max_x = max_f(cy)
            if min_x <= cx <= max_x:
                return idx + 1
            min_x = max_x
        else:
            raise ValueError('坐标点不在识别区域内')

    def __getXFunc(self, x1, y1, x2, y2):
        if not y1 != y2:
            raise AssertionError('y1, y2不能相等')
        if x1 == x2:

            def func(y):
                return x1

        else:
            k = (x2 - x1) / (y2 - y1)
            b = x1 - k * y1

            def func(y):
                return k * y + b

        return func

    def detect(self, frame, recognize_smoke):
        """ 抓取帧中的动态物体 并将结果格式化为`DetectResult`返回 """
        rois = self._FrameDetector__bg.grab(frame)
        rois = [i for i in rois if self.inRegion(i)]
        if len(rois) == 0:
            self.bg_frame = frame
            return []
        else:
            ret = self._FrameDetector__recognize(frame, rois, recognize_smoke)
            return ret

    def __recognize(self, frame, rois, recognize_smoke):
        """ 识别图像ROI """
        results = []
        for roi in rois:
            dr = DetectResult()
            dr.frame = frame
            dr.car_rect = roi
            results.append(dr)

        for dr, is_car in zip(results, self._FrameDetector__car_model.predict([i.car_img for i in results])):
            dr.is_car = is_car
            if is_car:
                dr.lane_no = self.getLaneNo(*dr.point)
                dr.is_recognize_plate = self._FrameDetector__plate_line_up <= dr.car_rect[1][1] <= self._FrameDetector__plate_line_down
                dr.is_smoke = is_car > 1 and recognize_smoke and True
            else:
                dr.is_smoke = False

        is_smoke = list(self._FrameDetector__smoke_model.predict([i.smoke_img for i in results if i.is_smoke]))
        for dr in results:
            if dr.is_smoke is True:
                dr.is_smoke = is_smoke.pop(0) > 0

        return results
# okay decompiling SFE\FrameDetector.pyc
