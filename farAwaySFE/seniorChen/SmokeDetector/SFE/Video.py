# coding: utf-8
import cv2
import numpy as np
from urllib.parse import quote

from .Tools import vs


class VideoReader():
    __is_stream = None
    __video = None
    __default_fps = 25

    is_opened = False
    fps = None
    size = None

    def openVideo(self, source) -> bool:
        ''' 打开视频文件或摄像头 '''

        assert not self.is_opened, "视频已经打开"

        self.__is_stream = False
        # 打开的视频捕获设备id ，如果只有一个摄像头可以填0，表示打开默认的摄像头。
        if isinstance(source, str) and source.isnumeric():
            source = int(source)
        self.__video = cv2.VideoCapture(source)

        if self.__video.isOpened() is False:
            self.is_opened = False
            return False

        self.fps = self.__video.get(cv2.CAP_PROP_FPS)
        if np.isinf(self.fps) or np.isnan(self.fps):
            self.fps = self.__default_fps
        else:
            self.fps = int(self.fps)
        self.size = (
            int(self.__video.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(self.__video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        )
        self.is_opened = True

        return True

    def openStream(self, user: str, pwd: str, ip: str, port: int, channels: int) -> bool:
        ''' 打开海康威视视频流 通过SDK '''

        assert not self.is_opened, "视频已经打开"

        self.__is_stream = True

        if vs.init(ip, port, user, pwd, channels) is False:
            return False
        if vs.nextFrame() is None:
            return False

        self.fps = self.__default_fps
        self.size = vs.getFrameSize()
        self.is_opened = True
        return True

    def openHKRTSP(self, user: str, pwd: str, ip: str, port: int, channels: int) -> bool:
        ''' 打开海康威视视频流 通过RTSP '''
        safe = ';/?&=+$,'  # 只排除 @:
        user = quote(user, safe=safe)
        pwd = quote(user, safe=safe)
        url = f'rtsp://{user}:{pwd}@{ip}:{port}/Streaming/Channels/{channels}01'

        return self.openVideo(url)

    def read(self):
        if self.__is_stream:
            data = vs.nextFrame()
            if data is None:
                return False, None
            else:
                return True, np.frombuffer(data, np.uint8).reshape(((3, ) + self.size)[::-1])
        else:
            return self.__video.read()

    def __del__(self):
        if not self.is_opened:
            return
        if self.__is_stream:
            vs.destroy()
        else:
            self.__video.release()
