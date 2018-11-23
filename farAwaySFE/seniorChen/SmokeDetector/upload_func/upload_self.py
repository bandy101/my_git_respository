# coding: utf-8
import json
import os

import requests

from .utlis import RecordData

invilad_token_code = 30006
self_token = ''


def upload(record: RecordData):
    ''' 上传到自己平台 '''
    global self_token
    ip = "localhost:8080/blacksmoke"

    # 初始化token
    if not self_token:
        url = f"http://{ip}/api/v1/oauth/token"
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
    url = f"http://{ip}/api/v1/dataReceive/uploadsSmokeMessage"
    headers = {"Authorization": f"bearer {self_token}"}

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
