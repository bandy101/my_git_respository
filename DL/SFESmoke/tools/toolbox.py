import os
from os import path
import sys
from typing import Tuple

import cv2
import numpy as np

try:
    from SFE.DL.Net import Net
except:
    Net = None


class Toolbox:
    """ 工具箱 """

    def __init__(self, model_path="smoke.h5"):
        """
        - model_path str["smoke.h5"]: 要加载的模型路径
        """
        self._net = None
        self._model_path = model_path

    def _loadModel(self):
        if self._net is not None:
            return self._net

        self._net = Net()
        self._net.load(self._model_path)
        return self._net

    def _getSmokeROI(self, img: np.ndarray, x: int, y: int, w: int, h: int) -> np.ndarray:
        """ 获取黑烟图片
        - img np.ndarray: 原图
        - x int: 车辆左上角x坐标
        - y int: 车辆左上角y坐标
        - w int: 车辆宽度
        - h int: 车辆高度
        - return np.ndarray: 返回黑烟图片
        """
        img = img.copy()
        x2, y2 = x + w, y + h
        width, height = w // 2, h // 2
        img[y:y2, x:x2] = 0

        x, x2 = max(x - width, 0), x2 + width
        y, y2 = max(y - height, 0), y2 + height

        img = img[y:y2, x:x2]
        return img

    def _roi(self, img: np.ndarray) -> Tuple[int, int, int, int] or None:
        """ 选择ROI
        - img np.ndarray: 图片
        - return tuple: 如果选择有效区域大于1*1, 则返回选中box(x, y, w, h), 否则返回None
        """
        box = cv2.selectROI("ROI", img, False, False)
        # cv2.destroyWindow("ROI")
        if box[:2] == (0, 0):
            return None
        return box

    def _predict(self, img: np.ndarray, box: tuple=None) -> int:
        """ 识别指定图片 如果box为None, 将直接识别图片, 否则为提取box的黑烟图片再进行识别
        - img np.ndarray: 图片
        - box tuple[None]: 车辆位置
        """
        if box is not None:
            img = self._getSmokeROI(img, *box)
        return self._loadModel().predict(img)[0]

    def predictImage(self, img_path: str, box: tuple=None, roi: bool = False, scale: float = None, show=False):
        """ 识别指定图片
        - img_path str: 图片路径
        - box tuple[None]: 车辆位置, 如果为None则原图识别
        - roi bool[False]: 是否手动选择车辆位置
        - scale float[None]: 图片缩放比例
        - show bool[False]: 是否显示用于识别的图像
        - return int: 返回识别结果
        """
        img = cv2.imread(img_path)
        if scale:
            img = cv2.resize(img, None, fx=scale, fy=scale)
        if roi is True:
            box = self._roi(img)

        print(box, self._predict(img, box))
        if show:
            cv2.imshow("SHOW", img)
            cv2.waitKey()

    def predictImages(self, dir_path: str, box: tuple=None, roi: bool = False, scale: float = None, show=False):
        """ 识别指定图片目录
        - dir_path str: 图片目录
        - box tuple[None]: 车辆位置, 如果为None则原图识别
        - roi bool[False]: 是否手动选择车辆位置
        - scale float[None]: 图片缩放比例
        - show bool[False]: 是否显示用于识别的图像
        - return int: 返回识别结果
        """
        for i in os.listdir(dir_path):
            self.predictImage(path.join(dir_path, i), box, roi, scale, show)

    def predictHKImage(self, img_path: str, scale: float=None):
        """ 识别海康图片 图片命名格式为 x-y-w-h.jpg
        - img_path str: 图片路径
        - scale float[None]: 图片缩放比例
        """
        x, y, w, h = map(int, path.basename(img_path)[:-4].split("-"))
        x, w = x * 4096 // 1000, w * 4096 // 1000
        y, h = y * 2160 // 1000, h * 2160 // 1000
        box = (x, y, w, h)
        img = cv2.imread(img_path)
        img = img[:2160, :4096]
        roi = self._getSmokeROI(img, *box)

        print(box, self._predict(img, box))
        if isinstance(scale, float):
            roi = cv2.resize(roi, None, fx=scale, fy=scale)
        cv2.imshow("roi", roi)
        cv2.waitKey()

    def predictHKImages(self, img_dir: str, scale: float=None):
        """ 批量识别海康图片 图片命名格式为 x-y-w-h.jpg
        - img_dir str: 图片目录路径
        - scale float[None]: 图片缩放比例
        """
        for i in os.listdir(img_dir):
            self.predictHKImage(path.join(img_dir, i), scale)

    def predictVideo(self, video_path, scale=None):
        """ 识别视频
        - video_path str: 视频路径
        - scale float[None]: 图片缩放比例
        """
        cap = cv2.VideoCapture(video_path)
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            if scale:
                frame = cv2.resize(frame, None, fx=scale, fy=scale)
            box = self._roi(frame)
            if box is not None:
                print(self._predict(frame, box))

    def grabVideo(self,
                  video_path: str,
                  save_dir: str,
                  name: str,
                  msg: str,
                  category: str,
                  scale: float=None,
                  start_idx: int=0,
                  cycle: int = 5
                  ):
        """ 截取视频素材
        - video_path str: 视频路径
        - save_dir str: 保存目录
        - name str: 名称（推荐格式为：日期_地点）
        - msg str: 文件名附加信息
        - category: 保存图片的类别
        - scale float[None]: 图片缩放比例
        - start_idx int[0]: 起始编号
        - cycle int[5]: 周期, 如：`5`表示每5帧显示1次图片

        最终文件保存结构为：
        save_dir/src/name/category/name_msg_idx.jpg
        save_dir/dst/name/category/name_msg_idx.jpg
        """
        # 初始化目录
        src_dir = path.join(save_dir, "src", str(name), str(category))
        dst_dir = path.join(save_dir, "dst", str(name), str(category))
        os.makedirs(src_dir, exist_ok=True)
        os.makedirs(dst_dir, exist_ok=True)

        cap = cv2.VideoCapture(video_path)
        c = start_idx
        while True:
            ret, frame = cap.read()
            for _ in range(cycle - 1):
                cap.read()
            if not ret:
                break
            if scale:
                frame = cv2.resize(frame, None, fx=scale, fy=scale)

            box = self._roi(frame)
            if box is not None:
                fn = f"{name}_{msg}_{c:04}.jpg"
                roi = self._getSmokeROI(frame, *box)
                cv2.imwrite(path.join(src_dir, fn), frame)
                cv2.imwrite(path.join(dst_dir, fn), roi)
                print(c)
                c += 1

    def grabImages(self,
                   dir_path: str,
                   save_dir: str,
                   name: str,
                   msg: str,
                   category: str,
                   scale: float=None,
                   start_idx: int=0
                   ):
        """ 截取图片
        - dir_path str: 图片目录路径
        - save_dir str: 保存目录
        - name str: 名称（推荐格式为：日期_地点）
        - msg str: 文件名附加信息
        - category: 保存图片的类别
        - scale float[None]: 图片缩放比例
        - start_idx int[0]: 起始编号

        最终文件保存结构为：
        save_dir/src/name/category/name_msg_idx.jpg
        save_dir/dst/name/category/name_msg_idx.jpg
        """
        src_dir = path.join(save_dir, "src", str(name), str(category))
        dst_dir = path.join(save_dir, "dst", str(name), str(category))
        os.makedirs(src_dir, exist_ok=True)
        os.makedirs(dst_dir, exist_ok=True)

        c = start_idx
        for i in os.listdir(dir_path):
            img = cv2.imread(path.join(dir_path, i))
            if scale:
                frame = cv2.resize(frame, None, fx=scale, fy=scale)
            box = self._roi(img)
            if box is not None:
                fn = f"{name}_{msg}_{c:04}.jpg"
                roi = self._getSmokeROI(img, *box)
                cv2.imwrite(path.join(src_dir, fn), frame)
                cv2.imwrite(path.join(dst_dir, fn), roi)
                print(c)
                c += 1


if __name__ == "__main__":
    from fire import Fire
    Fire(Toolbox)
