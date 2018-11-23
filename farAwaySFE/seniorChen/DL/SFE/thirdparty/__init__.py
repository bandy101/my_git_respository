# uncompyle6 version 3.2.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: SFE\thirdparty\__init__.py
# Compiled at: 2018-11-02 11:51:19
# Size of source mod 2**32: 2801 bytes
import os
from os import path
import sys, shutil
__root_path = path.dirname(path.abspath(__file__))
if sys.platform == 'win32':
    __sep = ';'
    __ENV_KEY = 'PATH'
    __ENV_PATH = os.environ.get(__ENV_KEY, '')
    os.environ[__ENV_KEY] = __sep.join([
     __ENV_PATH,
     __root_path])

class __Exception:

    def __init__(self, *args, **kwargs):
        raise NotImplementedError()

    def __getattr__(self, name):
        raise NotImplementedError()


try:
    from .PyEsegment import segment
except:
    segment = __Exception

try:
    from . import pyvideostream
except:
    pyvideostream = __Exception

try:
    from .pyeasypr import plateRecognize
    if not path.isdir('model'):
        shutil.copytree(path.join(__root_path, 'model'), 'model')
except:
    plateRecognize = __Exception

def getRingelmann(img, car_roi, smoke_roi, background=None):
    import cv2, numpy as np
    resize = 64
    roi_threshold = int(resize * 0.8333333333333333)
    lv = [212.5, 170, 127.5, 85, 42.5, 0]
    (x1, y1), (x2, y2) = car_roi
    (x3, y3), (x4, y4) = smoke_roi
    x1, x2 = x3 - x1, x3 - x2
    y1, y2 = y3 - y1, y3 - y2
    gray = cv2.resize(img[y3:y4, x3:x4], (resize, resize))
    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    mask_fg = segment(gray.tobytes(), gray.shape, 0.35, 1100, 50)
    mask_fg = np.frombuffer(mask_fg, np.uint8)
    mask_fg = mask_fg.reshape(gray.shape)
    gray[mask_fg == 0] = 0
    del mask_fg
    if background is not None:
        mask_bg = cv2.resize(background[y3:y4, x3:x4], (resize, resize))
        mask_bg = cv2.cvtColor(mask_bg, cv2.COLOR_BGR2GRAY)
        mask_bg = cv2.absdiff(gray, mask_bg)
        gray[mask_bg < 10] = 0
        del mask_bg
    gray[y1:y2, x1:x2] = 0
    level = []
    for roi in [
     gray[-roi_threshold:, ...],
     gray[..., :roi_threshold],
     gray[..., -roi_threshold:]]:
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
# okay decompiling SFE\thirdparty\__init__.pyc
