# coding: utf-8
import json
import os
from os import path
from datetime import datetime, timedelta
from collections import defaultdict

import requests

from SFE.Serialize import Serialize


class RecordData(Serialize):
    ''' 黑烟数据记录 '''

    def __init__(self):
        super().__init__()

        self.id = ''                # 记录ID
        self.timestamp = 0          # 记录13位时间戳

        self.st_id = 0              # 站点ID
        self.st_name = ''           # 站点名称

        self.Ringelmann = 0         # 林格曼黑度
        self.RingelmannLimit = 0    # 林格曼阈值

        self.plate = '无车牌'             # 车牌
        self.plate_color = '其他'       # 车牌颜色

        self.car_type = '其它车型'          # 车辆类型
        self.car_color = '其他'         # 车辆颜色
        self.car_lane = 1           # 车辆所在车道号

        self.img_plate_path = ''    # 车牌识别图像路径
        self.img_smoke_path = ''    # 黑烟判定图像路径
        self.video_path = ''        # 黑烟视频存放路径

    @property
    def check_time(self):
        return datetime.fromtimestamp(int(self.id) / 1000000) if self.id else datetime.now()

    @classmethod
    def fromTrackObject(cls, track, st_id: str, st_name: str, RingelmannLimit: int, img_plate_path: str, img_smoke_path: str, video_path: str):
        """ 从追踪对象中生成`RecordData`
        - track SFE.SmokeDetector.TrackObject: 追踪对象
        - st_id str: 站点ID
        - st_name str: 站点名称
        - RingelmannLimit int: 林格曼黑度阈值
        - img_plate_path str: 车牌识别图片路径
        - img_smoke_path str: 黑烟图片路径
        - video_path str: 视频路径
        """
        record = cls()
        record.st_id = st_id
        record.st_name = st_name
        record.id = track.id
        record.timestamp = int(track.timestamp * 1000)
        record.Ringelmann = track.Ringelmann
        record.RingelmannLimit = RingelmannLimit
        record.car_lane = track.lane_no
        if track.plate:
            record.plate = track.plate
        if track.plate_color:
            record.plate_color = track.plate_color
        if track.car_type:
            record.car_type = track.car_type
        if track.car_color:
            record.car_color = track.car_color
        record.img_plate_path = img_plate_path
        record.img_smoke_path = img_smoke_path
        record.video_path = video_path

        return record


invilad_token_code = 30006
self_token = ''


def upload(record: RecordData):
    ''' 上传到自己平台 '''
    global self_token
    ip = "localhost:8080/blacksmoke"

    # 初始化token
    if not self_token:
        url = "http://{}/api/v1/oauth/token".format(ip)
        jsondata = {
            "clientId": "098f6bcd4621d373cade4e832627b4f6",
            "userName": "admin",
            "password": "sfe5188",
            "captchaCode": "232",
            "captchaValue": "232"
        }
        data = requests.post(url, json=jsondata).json()
        self_token = data["content"]["access_token"]

    # 初始化上传数据
    url = "http://{}/api/v1/dataReceive/uploadsSmokeMessage".format(ip)
    headers = {"Authorization": "bearer {}".format(self_token)}

    fs = dict(
        file1=open(record.img_plate_path, 'rb'),
        file2=open(record.img_smoke_path, 'rb'),
        file3=open(record.video_path, 'rb')
    )

    data = {
        "stNumber": record.st_id,
        "stName": record.st_name,
        "lineNo": record.car_lane,
        "ringelmanEmittance": record.Ringelmann,
        "plate": record.plate,
        "plateColor": record.plate_color,
        "vehicleType": "0",
        "vehicleOwnerShip": "1",
        "greenYellowCar": "0",
        "throughTime": record.timestamp,
        "remarks": "",
        "plate": record.plate,
        "plateColor": record.plate_color
    }

    # 上传
    response = requests.post(url, data=data, files=fs, headers=headers)
    data = response.json()
    errcode = data.get('errcode', -1)

    if errcode == 0:
        return True
    elif errcode == 30006:  # token失效
        self_token = None
        return upload(record)
    else:
        print(response.text)
        return False
