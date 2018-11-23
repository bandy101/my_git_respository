# uncompyle6 version 3.2.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: .\SFE\Video.py
# Compiled at: 2018-11-02 11:51:19
# Size of source mod 2**32: 2541 bytes
import cv2, numpy as np
from urllib.parse import quote
from .Tools import vs

class VideoReader:
    _VideoReader__is_stream = None
    _VideoReader__video = None
    _VideoReader__default_fps = 25
    is_opened = False
    fps = None
    size = None

    def openVideo(self, source):
        """ ����Ƶ�ļ�������ͷ """
        if not not self.is_opened:
            raise AssertionError('��Ƶ�Ѿ���')
        self._VideoReader__is_stream = False
        if isinstance(source, str):
            if source.isnumeric():
                source = int(source)
        self._VideoReader__video = cv2.VideoCapture(source)
        if self._VideoReader__video.isOpened() is False:
            return False
        else:
            self.fps = self._VideoReader__video.get(cv2.CAP_PROP_FPS)
            if np.isinf(self.fps) or np.isnan(self.fps):
                self.fps = self._VideoReader__default_fps
            else:
                self.fps = int(self.fps)
            self.size = (int(self._VideoReader__video.get(cv2.CAP_PROP_FRAME_WIDTH)),
             int(self._VideoReader__video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            self.is_opened = True
            return True

    def openStream(self, user, pwd, ip, port, channels):
        """ �򿪺���������Ƶ�� ͨ��SDK """
        if not not self.is_opened:
            raise AssertionError('��Ƶ�Ѿ���')
        self._VideoReader__is_stream = True
        if vs.init(ip, port, user, pwd, channels) is False:
            return False
        elif vs.nextFrame() is None:
            return False
        else:
            self.fps = self._VideoReader__default_fps
            self.size = vs.getFrameSize()
            self.is_opened = True
            return True

    def openHKRTSP(self, user, pwd, ip, port, channels):
        """ �򿪺���������Ƶ�� ͨ��RTSP """
        safe = ';/?&=+$,'
        data = dict(user=quote(user, safe=safe),
          pwd=quote(pwd, safe=safe),
          ip=ip,
          port=port,
          channels=channels)
        url = ('rtsp://{user}:{pwd}@{ip}:{port}/Streaming/Channels/{channels}01').format_map(data)
        return self.openVideo(url)

    def read(self):
        if self._VideoReader__is_stream:
            data = vs.nextFrame()
            if data is None:
                return (False, None)
            return (
             True, np.frombuffer(data, np.uint8).reshape(((3, ) + self.size)[::-1]))
        else:
            return self._VideoReader__video.read()

    def __del__(self):
        if not self.is_opened:
            return
        if self._VideoReader__is_stream:
            vs.destroy()
        else:
            self._VideoReader__video.release()
# okay decompiling SFE\Video.pyc
