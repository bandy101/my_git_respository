# coding: utf-8
from os import path

import cv2
from datetime import datetime
import numpy as np
import tensorflow as tf

from .GrabObject import GrabObject
from .DL.Net import Net
from .DL.VehicleModel import VehicleModel


class DetectResult():

    def __init__(self):
        self.check_time = datetime.now()    # datetime, 检测时间

        self.is_car = 0                     # int, 车辆类别 0为非车
        self.__car_rect = None              # ((x, y), (x2, y2)), 车辆坐标
        self.lane_no = 0                    # int, 车道号

        self.is_smoke = False               # bool, 是否有黑烟
        self.smoke_rect = None              # ((x, y), (x2, y2)), 黑烟坐标

        self.r = 0                          # 有效跟踪半径 用于物体跟踪
        self.point = None                   # 车辆中心坐标 用于物体跟踪

        self.is_recognize_plate = False     # bool, 是否在车牌识别范围内

        self.frame = None                   # 该对象对应的图片

    @property
    def car_rect(self):
        return self.__car_rect

    @car_rect.setter
    def car_rect(self, value):
        self.__car_rect = value

        (x, y), (x2, y2) = self.car_rect

        # 计算黑烟坐标
        w = int((x2 - x) / 2)
        h = int((y2 - y) / 2)
        x3 = max(x - w, 0)
        x4 = x2 + w
        y3 = max(y - h, 0)
        y4 = y2 + h
        self.smoke_rect = (x3, y3), (x4, y4)

        # 计算中心点
        self.point = np.array([(x + x2) / 2, (y + y2) / 2])

        # 计算跟踪半径
        xd, yd = self.point - (x, y)
        self.r = min(xd, yd) ** 2

    @property
    def car_img(self):
        """ 获取该对象的车辆ROI """
        if self.car_rect is None or self.frame is None:
            return None
        (x, y), (x2, y2) = self.car_rect
        return self.frame[y:y2, x:x2]

    @property
    def smoke_img(self):
        """ 返回该对象的黑烟ROI """
        if self.car_rect is None or self.frame is None:
            return None
        (x, y), (x2, y2) = self.car_rect
        (x3, y3), (x4, y4) = self.smoke_rect

        x, x2 = x - x3, x2 - x3
        y, y2 = y - y3, y2 - y3
        img = self.frame[y3:y4, x3:x4].copy()
        img[y:y2, x:x2] = 0
        return img

    def inR(self, value):
        ''' 判断指定对象的中心点是否位于自身`r`范围内
        - value DetectResult: 要判断的对象

        - return bool: 返回是否在范围之内
        '''
        distance = np.sum((value.point - self.point) ** 2)
        return self.r >= distance


class FrameDetector():
    __plate_line_up = 0.5        # 车牌识别上边界
    __plate_line_down = 0.9      # 车牌识别下边界
    __recognize_top_board = 0.4  # 物体识别上边界，位于上边界的物体即判定为无效物体，值取`-1, 0~1`，为`-1`时表示无边界
    __recognize_bottom_board = 0.9  # 物体识别上边界，位于上边界的物体即判定为无效物体，值取`-1, 0~1`，为`-1`时表示无边界

    def __init__(self, size: (int, int), model_path: str, border: list):
        """
        - size tuple: 帧大小
        - model_path str: 模型所在目录
        - border list: 有两个元素 分别存放上边界坐标、下边界坐标
        """

        w, h = size

        self.__recognize_top_board *= h
        self.__recognize_bottom_board *= h
        self.__plate_line_up *= h
        self.__plate_line_down *= h

        # 获取边界计算方法
        if not border or all(border) is False:
            border = [
                [[0, 0], [100, 0]],
                [[0, 100], [100, 100]]
            ]
        up_border, down_border = border
        if len(up_border) != len(down_border):
            raise Exception('上下边界成员数必须相同')

        self.__xfun_list = []
        for (x1, y1), (x2, y2) in zip(up_border, down_border):
            x1, y1, x2, y2 = map(lambda x: x / 100, (x1, y1, x2, y2))
            x1, x2 = x1 * w, x2 * w
            y1, y2 = y1 * h, y2 * h
            self.__xfun_list.append(self.__getXFunc(x1, y1, x2, y2))

        # 定义session
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        self.__sess = tf.Session(config=config)

        # 创建、加载模型
        self.__car_model = VehicleModel(self.__sess)
        self.__smoke_model = Net(self.__sess)

        if not self.__car_model.load(path.join(model_path, "vehicle.h5")):
            raise Exception("初始化汽车识别模型失败")
        if not self.__smoke_model.load(path.join(model_path, "smoke.h5")):
            raise Exception("初始化黑烟识别模型失败")

        self.__bg = GrabObject(size)    # 抓取动态物体
        self.bg_frame = None            # 背景帧

    def __del__(self):
        self.__sess.close()

    def inRegion(self, rect) -> bool:
        ''' 判断指定矩形是否处于识别范围 '''
        (x, y), (x2, y2) = rect

        if not (self.__recognize_top_board <= y2 <= self.__recognize_bottom_board):
            return False

        cx, cy = np.array([(x + x2) / 2, (y + y2) / 2])
        return self.__xfun_list[0](cy) <= cx <= self.__xfun_list[-1](cy)

    def getLaneNo(self, cx, cy) -> int:
        ''' 判断指定点所在的车道 '''
        min_x = self.__xfun_list[0](cy)
        for idx, max_f in enumerate(self.__xfun_list[1:]):
            max_x = max_f(cy)
            if min_x <= cx <= max_x:
                return idx + 1
            else:
                min_x = max_x
        else:
            raise ValueError('坐标点不在识别区域内')

    def __getXFunc(self, x1, y1, x2, y2):
        if y1 == y2:
            raise Exception('y1, y2不能相等')

        if x1 == x2:
            def func(y):
                return x1
        else:
            # y = k * x + b
            k = (x2 - x1) / (y2 - y1)
            b = x1 - k * y1

            def func(y):
                return k * y + b

        return func

    def detect(self, frame, recognize_smoke) -> [DetectResult]:
        ''' 抓取帧中的动态物体 并将结果格式化为`DetectResult`返回 '''
        rois = self.__bg.grab(frame)
        rois = [i for i in rois if self.inRegion(i)]
        if len(rois) == 0:
            self.bg_frame = frame
            return []
        ret = self.__recognize(frame, rois, recognize_smoke)
        return ret

    def __recognize(self, frame, rois, recognize_smoke):
        ''' 识别图像ROI '''
        # 初始化
        results = []
        for roi in rois:
            dr = DetectResult()
            dr.frame = frame
            dr.car_rect = roi
            results.append(dr)

        # 进行车辆分类
        for dr, is_car in zip(results, self.__car_model.predict([i.car_img for i in results])):
            dr.is_car = is_car

            if is_car:
                # 车道号
                dr.lane_no = self.getLaneNo(*dr.point)

                # 是否进行车牌识别
                dr.is_recognize_plate = self.__plate_line_up <= dr.car_rect[1][1] <= self.__plate_line_down

                # 是否进行黑烟识别
                if is_car > 2 and recognize_smoke:
                    dr.is_smoke = True
                else:
                    dr.is_smoke = False

        # 进行黑烟识别
        is_smoke = list(self.__smoke_model.predict([i.smoke_img for i in results if i.is_smoke]))
        for dr in results:
            if dr.is_smoke is True:
                dr.is_smoke = is_smoke.pop(0) > 0

        return results
