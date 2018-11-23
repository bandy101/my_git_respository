# uncompyle6 version 3.2.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: .\SFE\GrabObject.py
# Compiled at: 2018-11-02 11:51:19
# Size of source mod 2**32: 1842 bytes
import cv2, numpy as np

class GrabObject:

    def __init__(self, size, base_size=(400, 400), filter_size=(20, 20)):
        """
        - size tuple: 图片的实际大小
        - base_size tuple[(400, 400)]: 在进行背景建模时，图片将被缩放到该大小
        - filter_size tuple[(20, 20)]: 小于该大小的物体将被忽略，该大小是居于base_size，而不是原大小
        """
        self._GrabObject__base_size = base_size
        self._GrabObject__scale = np.array(size) / np.array(self._GrabObject__base_size)
        self._GrabObject__module = cv2.createBackgroundSubtractorMOG2(detectShadows=True)
        self._GrabObject__filter_size = np.array(filter_size)

    def grab(self, frame):
        """ 抓取动态物体
        - frame: 图片帧
        
        - return: [((x, y), (x2, y2)), ...]
        """
        frame = cv2.resize(frame, self._GrabObject__base_size)
        if frame.shape[-1] != 1:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = self._GrabObject__module.apply(frame)
        frame = cv2.threshold(frame, 200, 255, cv2.THRESH_BINARY)[1]
        frame = cv2.morphologyEx(frame, cv2.MORPH_CLOSE, None, iterations=3)
        rois = []
        cnts = cv2.findContours(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        for cnt in cnts:
            x, y, w, h = cv2.boundingRect(cnt)
            x2, y2 = x + w, y + h
            if any([w, h] < self._GrabObject__filter_size):
                continue
            x, y = [
             x, y] * self._GrabObject__scale
            x2, y2 = [x2, y2] * self._GrabObject__scale
            x, y, x2, y2 = map(int, [x, y, x2, y2])
            rois.append(((x, y), (x2, y2)))

        return rois
# okay decompiling SFE\GrabObject.pyc
