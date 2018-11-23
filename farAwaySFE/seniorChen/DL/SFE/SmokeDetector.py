# uncompyle6 version 3.2.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: .\SFE\SmokeDetector.py
# Compiled at: 2018-11-02 11:51:19
# Size of source mod 2**32: 9686 bytes
from queue import Queue
import numpy as np, cv2
from collections import defaultdict, Counter
from os import path
from .Tools import segment
from .FrameDetector import DetectResult
from .Video import VideoReader
from .FrameDetector import FrameDetector
from .Tools import getPlate
from .DL.VehicleModel import VehicleModel
from .getColor import getForegroundColor
from .thirdparty import getRingelmann

class TrackObject:

    @property
    def last_result(self):
        if self.list:
            return self.list[-1]

    def __init__(self):
        self.id = None
        self.plate = None
        self.plate_color = None
        self.car_color = None
        self.check_time = None
        self.timestamp = None
        self.car_rect = None
        self.lane_no = 0
        self.Ringelmann = 0
        self.plate_image = None
        self.smoke_image = None
        self.list = []
        self.smoke_count = 0
        self.last_index = 0

    @property
    def car_type(self):
        """ 车辆类型 """
        l = [i.is_car for i in self.list]
        counter = Counter(l)
        return VehicleModel[max(counter, key=lambda i: counter[i])]


class SmokeDetector:

    def __init__(self, video_source, border=None, module_path=None, fix=True, only_car=True, auth_code=None):
        """
        - video_source str: 视频源
        - model_path str: 模型所在目录
        - border list: 各车道边界
        - fix bool[True]: 在黑烟判断错误时 该对象是否继续重新判定
        - only_car bool[True]: 是否只获取被判定为车辆的结果
        - auth_code str[None]: 授权码
        """
        self._SmokeDetector__verifyAuth(auth_code)
        self._SmokeDetector__reader = VideoReader()
        self._SmokeDetector__detector = None
        self._SmokeDetector__index = 0
        self._SmokeDetector__save_list = []
        self._SmokeDetector__frame_queue = None
        self.size = None
        self.fps = None
        self.max_track_interval = 0
        self.tracking_list = []
        self.only_car = only_car
        self._SmokeDetector__fix = fix
        if module_path is None:
            module_path = path.join(path.dirname(__file__), 'resource')
        if video_source.count('||') == 5:
            user, pwd, ip, port, channel, open_type = video_source.split('||')
            port, channel = int(port), int(channel)
            if open_type == '0':
                self._SmokeDetector__reader.openStream(user, pwd, ip, port, channel)
            else:
                if open_type == '1':
                    self._SmokeDetector__reader.openHKRTSP(user, pwd, ip, port, channel)
                else:
                    self._SmokeDetector__reader.openVideo(video_source)
                if not self._SmokeDetector__reader.is_opened:
                    raise AssertionError('视频打开失败')
                self.fps = self._SmokeDetector__reader.fps
                self.size = self._SmokeDetector__reader.size
                self._SmokeDetector__frame_queue = Queue(self.fps * 10)
                self.max_track_interval = int(self.fps / 3)
                self.max_save_interval = self._SmokeDetector__frame_queue.maxsize
                self._SmokeDetector__detector = FrameDetector(self._SmokeDetector__reader.size, module_path, border)

    def nextFrame(self, recognize_smoke=True, only_frame=False):
        """ 获取下一帧结果
        - recognize_smoke bool: 是否进行黑烟识别
        - only_frame bool[False]: 是否只读取帧 不做其他处理
        
        - return: frame, tracks, save_list
        """
        ret, frame = self._SmokeDetector__reader.read()
        if ret is False:
            if only_frame:
                return (None, [], [])
            save_list = [i['track'] for i in self._SmokeDetector__save_list]
            self._SmokeDetector__save_list = []
            return (
             None, [], save_list)
        else:
            if self._SmokeDetector__frame_queue.full():
                self._SmokeDetector__frame_queue.get()
            self._SmokeDetector__frame_queue.put(frame)
            self._SmokeDetector__index += 1
            if only_frame:
                return (frame, [], [])
            results = self._SmokeDetector__detector.detect(frame, recognize_smoke)
            tracks = self._SmokeDetector__updateTrackList(results)
            for track in tracks:
                if track.smoke_count == 3:
                    if track.id not in (i['id'] for i in self._SmokeDetector__save_list):
                        self._SmokeDetector__save_list.append({'save_index':self._SmokeDetector__index + self.fps * 5, 
                         'track':track, 
                         'id':track.id})

            save_objs = []
            for obj in self._SmokeDetector__save_list:
                if obj['save_index'] <= self._SmokeDetector__index:
                    track = obj['track']
                    save_objs.append(track)
                    self._SmokeDetector__updateCarInfo(track)
                    self._SmokeDetector__save_list.remove(obj)

            return (frame, tracks, save_objs)

    def getSaveFrames(self):
        """ 返回帧队列中的所有帧 """
        return list(self._SmokeDetector__frame_queue.queue)

    @property
    def index(self):
        return self._SmokeDetector__index

    def __updateTrackList(self, results):
        """ 更新跟踪列表 """
        tracks = []
        if self.only_car:
            results = [i for i in results if i.is_car]
        car_rect_list = {i.car_rect for i in results if i.is_car}
        for result in results:
            for track in self.tracking_list:
                if self._SmokeDetector__index - track.last_index <= self.max_track_interval:
                    if track.last_result.inR(result):
                        break
            else:
                track = TrackObject()
                track.id = str(int(result.check_time.timestamp() * 1000000))
                self.tracking_list.append(track)

            tracks.append(track)
            track.list.append(result)
            track.last_index = self._SmokeDetector__index
            self._SmokeDetector__updateSmokeInfo(track, car_rect_list)

        for track in self.tracking_list:
            if self._SmokeDetector__index - track.last_index > self.max_track_interval:
                self.tracking_list.remove(track)

        return tracks

    def __updateCarInfo(self, track):
        """ 更新车辆信息 """
        first = track.list[0]
        car_result = first
        for result in track.list:
            if not result.is_recognize_plate:
                continue
            if car_result is first:
                car_result = result
            plate, color = getPlate(result.car_img)
            color = color.replace('牌', '')
            if plate:
                track.plate = plate
            if color:
                track.plate_color = color
            if all([track.plate, track.plate_color]):
                break

        car_img = car_result.frame.copy()
        cv2.rectangle(car_img, *car_result.car_rect, *((0, 0, 255), 2))
        track.plate_image = car_img
        track.car_color = getForegroundColor(car_result.car_img)

    def __updateSmokeInfo(self, track, rect_list):
        """ 更新黑烟信息 """
        result = track.last_result
        if not result.is_smoke:
            return
        track.smoke_count += 1
        if track.smoke_count == 3:
            l = getRingelmann(result.frame, result.car_rect, result.smoke_rect, self._SmokeDetector__detector.bg_frame)
            if l <= 0:
                if l == -1:
                    if self._SmokeDetector__fix:
                        track.smoke_count = -self.fps
                track.smoke_count -= 1
            else:
                img = result.frame.copy()
                cv2.rectangle(img, *result.car_rect, *((0, 0, 255), 2))
                track.smoke_image = img
                track.Ringelmann = l
                track.check_time = result.check_time.strftime('%Y-%m-%d %H:%M:%S.%f')
                track.timestamp = result.check_time.timestamp()
                track.lane_no = result.lane_no
                track.car_rect = result.car_rect

    @staticmethod
    def __verifyAuth(auth_code):
        from hashlib import md5
        from . import getAuthID
        code = 1
        for c in getAuthID().replace('f', '').replace('e', '').split('-'):
            if c:
                code *= int(c, 16)

        if not md5(bin(code).encode()).hexdigest() == auth_code:
            raise AssertionError('授权码校验失败')
# okay decompiling SFE\SmokeDetector.pyc
