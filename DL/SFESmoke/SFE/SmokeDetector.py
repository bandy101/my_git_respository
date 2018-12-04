# coding: utf-8
from queue import Queue
import numpy as np
import cv2
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


class TrackObject():

    @property
    def last_result(self):
        return self.list[-1] if self.list else None

    def __init__(self):
        self.id = None           # 追踪对象的ID

        self.plate = None        # 车牌
        self.plate_color = None  # 车牌颜色
        self.plate_type = None   # 车牌类型

        self.car_color = None    # 车身颜色
        # @property car_type 车辆类型

        self.check_time = None   # 被判定为黑烟车时的时间
        self.timestamp = None    # 被判定为黑烟车时的时间戳
        self.car_rect = None     # 被判定为黑烟车时车的位置
        self.lane_no = 0         # 被判定为黑烟车时车的车道号
        self.Ringelmann = 0      # 林格曼黑度

        self.plate_image = None  # 进行车牌识别时的帧
        self.smoke_image = None  # 被判定为黑烟车时的帧

        self.list = []           # 跟踪列表

        self.smoke_count = 0     # 判定为黑烟的次数 3次即被判定为黑烟

        self.last_index = 0

    @property
    def car_type(self):
        """ 车辆类型 """
        return VehicleModel[self.car_type_id]

    @property
    def car_type_id(self):
        """ 车辆类型ID """
        l = [i.is_car for i in self.list]
        counter = Counter(l)
        return max(counter, key=lambda i: counter[i])


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

        # 授权校验
        self.__verifyAuth(auth_code)

        # 变量初始化
        self.__reader = VideoReader()   # 视频读取
        self.__detector = None          # 帧匹配
        self.__index = 0                # 当前帧
        self.__save_list = []           # 追踪判定为黑烟的对象列表
        self.__frame_queue = None       # 保存十秒的帧队列
        self.size = None                # 视频帧的大小
        self.fps = None                 # 视频的FPS
        self.max_track_interval = 0     # 最大追踪间隔阈值
        self.tracking_list = []         # 存放所有未被删除的跟踪对象
        self.only_car = only_car        # 排除非车信息

        self.__fix = fix                # 是否排除计算林格曼的值等于-1的对象

        if module_path is None:
            module_path = path.join(path.dirname(__file__), "resource")

        # 打开视频
        if video_source.count("||") == 5:
            user, pwd, ip, port, channel, open_type = video_source.split("||")
            port, channel = int(port), int(channel)
            if open_type == "0":
                self.__reader.openStream(user, pwd, ip, port, channel)
            elif open_type == "1":
                self.__reader.openHKRTSP(user, pwd, ip, port, channel)
        else:
            self.__reader.openVideo(video_source)
        if not self.__reader.is_opened:
            raise Exception("视频打开失败")

        # 获取视频基本参数
        self.fps = self.__reader.fps
        self.size = self.__reader.size

        self.__frame_queue = Queue(self.fps * 10)
        self.max_track_interval = int(self.fps / 3)
        self.max_save_interval = self.__frame_queue.maxsize

        self.__detector = FrameDetector(self.__reader.size, module_path, border)

    def nextFrame(self, recognize_smoke=True, only_frame=False):
        ''' 获取下一帧结果
        - recognize_smoke bool: 是否进行黑烟识别
        - only_frame bool[False]: 是否只读取帧 不做其他处理

        - return: frame, tracks, save_list
        '''

        # 读取视频帧
        ret, frame = self.__reader.read()

        # 视频结束 返回所有未保存的对象
        if ret is False:
            if only_frame:
                return None, [], []
            else:
                save_list = [i["track"] for i in self.__save_list]
                self.__save_list = []
                return None, [], save_list

        # 更新视频帧队列
        if self.__frame_queue.full():
            self.__frame_queue.get()
        self.__frame_queue.put(frame)

        self.__index += 1

        if only_frame:
            return frame, [], []

        # 进行识别和结构化
        results = self.__detector.detect(frame, recognize_smoke)
        # 更新跟踪列表
        tracks = self.__updateTrackList(results)

        # 更新保存对象
        for track in tracks:
            if (
                track.smoke_count == 3
                and track.id not in (i["id"] for i in self.__save_list)
                and track.car_type_id > 2
            ):
                self.__save_list.append({
                    "save_index": self.__index + self.fps * 5,
                    "track": track,
                    "id": track.id
                })

        # 获取当前帧保存的对象
        save_objs = []
        for obj in self.__save_list:
            if obj['save_index'] <= self.__index:
                track = obj['track']
                save_objs.append(track)
                self.__updateCarInfo(track)

                self.__save_list.remove(obj)

        return frame, tracks, save_objs

    def getSaveFrames(self):
        ''' 返回帧队列中的所有帧 '''
        return list(self.__frame_queue.queue)

    @property
    def index(self):
        return self.__index

    def __updateTrackList(self, results: [DetectResult, ...]):
        """ 更新跟踪列表 """
        # 初始化
        tracks = []
        if self.only_car:
            results = [i for i in results if i.is_car > 1]

        for result in results:
            # 添加、更新物体
            for track in self.tracking_list:
                # 在跟踪间隔内 且两中心点距离的小于r则判定为同一物体
                if self.__index - track.last_index <= self.max_track_interval and track.last_result.inR(result):
                    break
            else:
                track = TrackObject()
                track.id = str(int(result.check_time.timestamp() * 1000000))
                self.tracking_list.append(track)
            tracks.append(track)

            # 更新最后信息
            track.list.append(result)
            track.last_index = self.__index
            self.__updateSmokeInfo(track)

        # 移除过期物
        for track in self.tracking_list:
            if self.__index - track.last_index > self.max_track_interval:
                self.tracking_list.remove(track)

        return tracks

    def __updateCarInfo(self, track: TrackObject):
        ''' 更新车辆信息 '''
        first = track.list[0]
        car_result = first

        # 车牌识别
        for result in track.list:
            if not result.is_recognize_plate:
                continue

            if car_result is first:
                car_result = result

            # 车牌识别
            plate, color, _type = getPlate(result.car_img)

            # 更新车牌信息
            if plate:
                track.plate = plate
            if color:
                track.plate_color = color
            track.plate_type = _type
            if all([track.plate, track.plate_color]):
                break

        car_img = car_result.frame.copy()
        cv2.rectangle(car_img, *car_result.car_rect, (0, 0, 255), 2)  # 标志位置
        track.plate_image = car_img  # 图片
        track.car_color = getForegroundColor(car_result.car_img)  # 车身颜色

    def __updateSmokeInfo(self, track: TrackObject):
        ''' 更新黑烟信息 '''
        result = track.last_result
        if not result.is_smoke:
            return

        # 更新判定为黑烟的次数
        track.smoke_count += 1
        if track.smoke_count == 3:
            # 计算林格曼黑度
            l = getRingelmann(result.frame, result.car_rect, result.smoke_rect, self.__detector.bg_frame)
            if l <= 0:
                if l == -1 and self.__fix:
                    track.smoke_count = -self.fps
                else:
                    track.smoke_count -= 1
            else:
                # 更新黑烟相关信息
                img = result.frame.copy()
                cv2.rectangle(img, *result.car_rect, (0, 0, 255), 2)
                track.smoke_image = img  # 图片
                track.Ringelmann = l    # 林格曼黑度
                track.check_time = result.check_time.strftime('%Y-%m-%d %H:%M:%S.%f')   # 检测时间
                track.timestamp = result.check_time.timestamp()  # 时间戳
                track.lane_no = result.lane_no  # 车道号
                track.car_rect = result.car_rect  # 位置

    @staticmethod
    def __verifyAuth(auth_code):
        from hashlib import md5
        from hmac import compare_digest
        from . import getAuthID

        code = 1
        for c in getAuthID().replace("f", "").replace("e", "").split("-"):
            if c:
                code *= int(c, 16)

        if not compare_digest(md5(bin(code).encode()).hexdigest(), str(auth_code)):
            raise Exception("授权码校验失败")
