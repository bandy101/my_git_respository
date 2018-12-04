import os
from os import path
import sys
import shutil


__root_path = path.dirname(path.abspath(__file__))

# 设置环境变量
if sys.platform == "win32":
    __sep = ";"
    __ENV_KEY = "PATH"

    # 添加动态库搜索路径
    __ENV_PATH = os.environ.get(__ENV_KEY, "")
    os.environ[__ENV_KEY] = __sep.join([
        __ENV_PATH,
        __root_path,
    ])


# 图片分割
from .PyEsegment import segment

# 视频流读取
from . import pyvideostream

# 车牌识别
from .pythplateid import plateRecognize

def getRingelmann(img, car_roi, smoke_roi, background=None):
    import cv2
    import numpy as np
    ''' 计算林格曼黑度等级
    - img image: 完整图片
    - car_roi: 车辆在图片中的绝对位置 `((left, top), (right, bottom))`
    - smoke_roi: 黑烟在图片中的绝对位置 同`car_roi`
    - background: 背景图片
    - return int: 0~5
    '''
    # 常量
    resize = 64
    roi_threshold = int(resize * (1/2 + 1/3))
    lv = [212.5, 170, 127.5, 85, 42.5, 0]

    # 初始化坐标
    (x1, y1), (x2, y2) = car_roi
    (x3, y3), (x4, y4) = smoke_roi
    x1, x2 = x3 - x1, x3 - x2
    y1, y2 = y3 - y1, y3 - y2

    # 转为灰度图
    gray = cv2.resize(img[y3:y4, x3:x4], (resize, resize))
    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)

    # 获取前景
    mask_fg = segment(gray.tobytes(), gray.shape, 0.35, 1100, 50)
    mask_fg = np.frombuffer(mask_fg, np.uint8)
    mask_fg = mask_fg.reshape(gray.shape)
    # 清除前景值
    gray[mask_fg == 0] = 0
    del mask_fg

    # 获取背景
    if background is not None:
        mask_bg = cv2.resize(background[y3:y4, x3:x4], (resize, resize))
        mask_bg = cv2.cvtColor(mask_bg, cv2.COLOR_BGR2GRAY)
        mask_bg = cv2.absdiff(gray, mask_bg)
        # 清除背景值
        gray[mask_bg < 10] = 0
        del mask_bg

    # 清除车辆位置
    gray[y1:y2, x1:x2] = 0

    level = []
    for roi in [
        gray[-roi_threshold:, ...],  # 下
        gray[..., :roi_threshold],  # 左
        gray[..., -roi_threshold:],  # 右
    ]:
        total = roi.size
        roi = roi[roi > 0]
        if roi.size / total < 0.01:
            continue

        i = np.median(roi)
        for k, v in enumerate(lv):
            if i >= v:
                level.append(k)
                break
    del roi

    return max(level, default=0)
