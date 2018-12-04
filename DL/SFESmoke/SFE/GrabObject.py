# coding: utf-8
import cv2
import numpy as np

'''
动态物体抓取模块
'''


class GrabObject():

    def __init__(self, size: (int, int), base_size=(400, 400), filter_size=(20, 20)):
        '''
        - size tuple: 图片的实际大小
        - base_size tuple[(400, 400)]: 在进行背景建模时，图片将被缩放到该大小
        - filter_size tuple[(20, 20)]: 小于该大小的物体将被忽略，该大小是居于base_size，而不是原大小
        '''

        self.__base_size = base_size
        self.__scale = np.array(size) / np.array(self.__base_size)
        self.__module = cv2.createBackgroundSubtractorMOG2(detectShadows=True)

        self.__filter_size = np.array(filter_size)

    def grab(self, frame: np.ndarray):
        ''' 抓取动态物体
        - frame: 图片帧

        - return: [((x, y), (x2, y2)), ...]
        '''

        frame = cv2.resize(frame, self.__base_size)
        if frame.shape[-1] != 1:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        frame = self.__module.apply(frame)
        # 二值化 去除阴影
        frame = cv2.threshold(frame, 200, 255, cv2.THRESH_BINARY)[1]
        # 闭运算 消除空洞
        frame = cv2.morphologyEx(frame, cv2.MORPH_CLOSE, None, iterations=3)

        rois = []
        cnts = cv2.findContours(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        for cnt in cnts:
            x, y, w, h = cv2.boundingRect(cnt)
            x2, y2 = x + w, y + h
            # 过滤较小轮廓
            if any([w, h] < self.__filter_size):
                continue
            # 计算轮廓在原图的位置
            x, y = [x, y] * self.__scale
            x2, y2 = [x2, y2] * self.__scale
            x, y, x2, y2 = map(int, [x, y, x2, y2])

            rois.append(((x, y), (x2, y2)))

        return rois
