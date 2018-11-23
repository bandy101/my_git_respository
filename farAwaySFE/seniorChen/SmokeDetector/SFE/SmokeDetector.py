# coding: utf-8
from queue import Queue
import numpy as np
import cv2

from .Tools import segment
from .FrameDetector import DetectResult
from .Video import VideoReader
from .FrameDetector import FrameDetector
from .Tools import getPlate
from .DL import VehicleModel


class TrackObject():

    @property
    def last_result(self):
        return self.list[-1] if self.list else None

    def __init__(self):
        self.id = None           # 追踪对象的ID

        self.check_time = None   # 进行车牌识别的时间
        self.timestamp = None    # 进行车牌识别的时间戳

        self.car_rect = None     # 进行车牌识别时该车的位置
        self.car_type = None     # 车型
        self.car_color = None    # 车身颜色
        self.lane_no = 0         # 进行车牌识别时的车道号

        self.plate = None        # 车牌
        self.plate_color = None  # 车牌颜色
        self.plate_image = None  # 进行车牌识别时的帧

        self.Ringelmann = 0      # 林格曼黑度
        self.smoke_image = None  # 追踪被判定为黑烟时的帧

        self.list = []           # 跟踪列表

        self.smoke_count = 0     # 判定为黑烟的次数 3次即被判定为黑烟

        self.last_index = 0


class SmokeDetector:

    def __init__(self, video_source, module_path, border, fix=True, only_car=True):
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
        self.track_total = 0            # 目前跟踪对象的总数 包括被删除的跟踪对象
        self.only_car = only_car        # 排除非车信息

        self.__fix = fix                # 是否排除计算林格曼的值等于-1的对象

        # 打开视频(视频文件和流文件)
        if video_source.count("||") == 4:
            user, pwd, ip, port, channel = video_source.split("||")
            port, channel = int(port), int(channel)
            self.__reader.openStream(user, pwd, ip, port, channel)
        else:
            self.__reader.openVideo(video_source)
        assert self.__reader.is_opened, "视频打开失败"

        # 获取视频基本参数
        self.fps = self.__reader.fps
        self.size = self.__reader.size
        self.__frame_queue = Queue(self.fps * 10)

        self.__detector = FrameDetector(
            self.__reader.size, module_path, border)

        self.max_track_interval = int(self.fps / 3)
        self.max_save_interval = self.__frame_queue.maxsize

    def nextFrame(self, only_frame=False):
        ''' 获取下一帧结果
        only_frame: 是否只读取帧 不做其他处理
        return: frame, tracks, save_list
        '''

        ret, frame = self.__reader.read()
        # 视频结束 返回所有未保存的对象
        if ret is False:
            if only_frame:
                return None, [], []
            else:
                save_list = [i["track"] for i in self.__save_list]
                self.__save_list = []
                return None, [], save_list

        # 更新队列
        if self.__frame_queue.full():
            self.__frame_queue.get()
        self.__frame_queue.put(frame)

        self.__index += 1

        if only_frame:
            return frame, [], []

        results = self.__detector.detect(frame)
        tracks = self.__updateTrackList(results)

        # 确认需要保存的对象
        for track in tracks:
            if track.smoke_count == 3:
                if not [i for i in self.__save_list if track.id == i["id"]]:
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
                self.__updatePlateInfo(track)

                self.__save_list.remove(obj)

        return frame, tracks, save_objs

    def getSaveFrames(self):
        ''' 返回帧队列中的所有帧 '''
        return list(self.__frame_queue.queue)

    def __updateTrackList(self, results: [DetectResult, ...]):
        #results 一副图像中的轮廓符合要求的动态物体转化为DetectResult
        tracks = []
        if self.only_car:
            results = [i for i in results if i.is_car]
        car_rect_list = {i.car_rect for i in results if i.is_car}

        for result in results:
            # 添加、更新物体
            for track in self.tracking_list:
                # 在跟踪间隔内 且两中心点距离的小于r则判定为同一物体
                if self.__index - track.last_index <= self.max_track_interval and track.last_result.inR(result):
                    break
            else:
                track = TrackObject()
                track.id = f"{result.check_time.timestamp() * 1000000:.0f}"#时间戳整数
                self.__updateCarInfo(track, result)
                self.tracking_list.append(track)
                self.track_total += 1
            tracks.append(track)

            # 更新最后信息
            track.list.append(result)
            track.last_index = self.__index#  追踪的最后帧数等于检测的当前帧
            self.__updateSmokeInfo(track, car_rect_list)

        # 移除过期物
        for track in self.tracking_list:
            if self.__index - track.last_index > self.max_track_interval:
                self.tracking_list.remove(track)
        
        return tracks

    def __updateCarInfo(self, track: TrackObject, result: DetectResult):
        ''' 更新车辆信息 ''' 
        track.plate_image = result.frame.copy()  # 图片
        cv2.rectangle(track.plate_image, *result.car_rect,
                      (0, 0, 255), 2)  # 标志位置
                      #bgr qt rgb 
        track.check_time = result.check_time.strftime(
            '%Y-%m-%d %H:%M:%S.%f')   # 检测时间
        track.timestamp = result.check_time.timestamp()  # 时间戳
        track.lane_no = result.lane_no  # 车道号
        track.car_rect = result.car_rect  # 位置
        track.car_type = VehicleModel[result.is_car]  # 车辆类型

    def __updateSmokeInfo(self, track: TrackObject, rect_list: []):
        ''' 更新黑烟状态 '''
        result = track.last_result
        if not result.is_smoke:
            return

        # 更新判定为黑烟的次数
        track.smoke_count += 1
        if track.smoke_count == 3:
            l = self.__updateRingelmann(result.frame, result, rect_list)
            if l == -1 and self.__fix:
                track.smoke_count = -self.fps
            else:
                track.smoke_image = result.frame.copy()
                cv2.rectangle(track.smoke_image, *
                              result.car_rect, (0, 0, 255), 2)
                track.Ringelmann = l

    def __updatePlateInfo(self, track: TrackObject):
        ''' 更新车牌信息 '''
        # 车牌识别
        for i in (i for i in track.list if i.is_recognize_plate):
            (x, y), (x2, y2) = i.car_rect
            img = i.frame[y:y2, x:x2]
            plate, color = getPlate(img)
            if plate:
                track.plate = plate
            if color:
                track.plate_color = color if '牌' not in color else color[:-1]
            if all([track.plate, track.plate_color]):
                self.__updateCarInfo(track, i)
                break

    def __updateRingelmann(self, frame, result, rect_list):
        ''' 更新林格曼等级 '''
        lv = [212.5, 170, 127.5, 85, 42.5, 0]
        source = frame

        # 初始化背景帧
        if self.__detector.bg_frame is None:
            background = np.full(frame.shape, 0, np.uint8)
        else:
            background = self.__detector.bg_frame

            
        # 转为灰度图
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        background = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
        
        # 减除前景
        mask1 = segment(frame.tobytes(), frame.shape, 0.35, 1100, 50)
        mask1 = np.frombuffer(mask1, np.uint8)
        mask1 = mask1.reshape(   .shape)
        print ('mask1',mask1)
        # 减除车辆
        for (x, y), (x2, y2) in rect_list:
            frame[y:y2, x:x2] = 0
            background[y:y2, x:x2] = 0

        # ROI
        (x, y), (x2, y2) = result.car_rect
        (x3, y3), (x4, y4) = result.smoke_rect
        roi = frame[y3:y4, x3:x4]
        bg = background[y3:y4, x3:x4]
        mask1 = mask1[y3:y4, x3:x4]

        # 计算变化区域
        mask2 = cv2.absdiff(roi, bg)
        mask2 = cv2.GaussianBlur(mask2, (5, 5), 1)
        mask2 = cv2.threshold(mask2, 20, 255, cv2.THRESH_BINARY)[1]
        mask2 = cv2.erode(mask2, None, iterations=2)

        roi[mask1 == 0] = 0
        roi[mask2 == 0] = 0
        r = roi

        # 计算林格曼
        rois = [
            r[max(0, y - y3 - 50):y - y3, x - x3:x2 - x3],  # 上
            r[y2 - y3:y2 - y3 + 50, x - x3:x2 - x3],        # 下
            r[y - y3:y2 - y3, max(0, x - x3 - 50):x - x3],  # 左
            r[y - y3:y2 - y3, x2 - x3:x2 - x3 + 50]         # 右
        ]
        # 排除宽度或高度为0的roi
        rois = [i for i in rois if min(i.shape[:2]) > 0]

        level = []
        for i in rois:
            r = i[i > 0].reshape(-1)
            if r.size / i.size < 0.01:
                continue

            i = np.median(r)
            for k, v in enumerate(lv):
                if i >= v:
                    level.append(k)
                    break

        return max(level, default=-1)
