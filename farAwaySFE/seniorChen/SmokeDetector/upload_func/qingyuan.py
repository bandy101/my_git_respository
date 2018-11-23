# coding: utf-8
import json
import os
from datetime import datetime, timedelta

import requests

from . import utlis

invilad_token_code = 30006
token = ''
ip = 'http://192.168.4.151:8080/platform_telemetry_smoke_qingyuan-1.0'

# 车牌颜色
__plate_color = dict(
    蓝='1',
    黄='2',
    白='3',
    黑='4',
    绿='5',
    黄绿='6'
)

# 车身颜色
__car_color = dict(
    白='A',
    灰='B',
    黄='C',
    粉='D',
    红='E',
    萦='F',
    绿='G',
    蓝='H',
    棕='I',
    黑='J',
    其他='Z'
)

# 车辆类型
__car_type = dict(
    其它车型='X99',
    小型车='K33',
    大型车='H11',
    客车='K11',
    货车='H11',
    小货车='H31',
    轿车='K33',
    面包车='K41'
)


def getToken(refresh=False):
    global token
    if (not refresh) and token:
        return token
    url = f'{ip}/api/1/oauth/token'
    data = dict(
        clientId='098f6bcd4621d373cade4e832627b4f6',
        userName='admin',
        password='sfe5188',
        captchaCode='232',
        captchaValue='232'
    )

    try:
        ret = requests.post(url, json=data).json()
        if ret['errcode'] == 0:
            token = ret['content']['accessToken']
            return token
    except:
        pass
    token = ''
    return token


def upload(record: utlis.RecordData, refresh=False):
    url = f'{ip}/api/1/smokeMessage'
    headers = dict(Authorization=f'bearer {getToken(refresh)}')
    t = datetime.fromtimestamp(record.timestamp / 1000)
    data = dict(
        jcsjStr=f'{t:%Y-%m-%d %H:%M:%M}:{t.microsecond/1000:03.0f}',              # 检测时间
        tsNo=str(record.st_id),                                                 # 站点编号 yyyy-MM-dd HH:mm:ss:SSS
        line='0',                                                               # ? 检测线编号 常量 未设置
        lane=record.car_lane,                                                   # 车道号
        ringelman=record.Ringelmann,                                            # 林格曼黑度
        ringelmanLimit=record.RingelmannLimit,                                  # 林格曼黑度阈值
        license=record.plate,                                                   # 车牌
        licenseCode='99',                                                       # 车牌类型 GA 24.7
        licenseType=__plate_color.get(record.plate_color, '0'),                 # 车牌颜色 对照表
        vehicleType=__car_type.get(record.car_type, __car_type['其它车型']),     # 车辆类型 对照表
        vehicleColor=__car_color.get(record.car_color, __car_color['其他']),     # 车辆颜色 GA 24.8
        fuelType='0',                                                           # ? 燃油种类
        ssxq='0',                                                               # ? 所属辖区 常量 未设置
        standard='0',                                                           # ? 排放标准 附录 13.2 常量 未设置
        hbflbz=0,                                                               # ? 环保分类标志
        shzt='0'                                                                # 审核结果 0: 待审核
    )
    files = dict(
        file1=open(record.img_plate_path, 'rb'),
        file2=open(record.img_smoke_path, 'rb'),
        file3=open(record.video_path, 'rb')
    )
    try:
        ret = requests.post(url, data=data, files=files, headers=headers)
        ret = ret.json()
        if ret['errcode'] == 0 and ret['content'] is True:
            return True
        elif ret['errcode'] == invilad_token_code:
            return upload(record, True)
    except:
        pass
    return False


def statistics(st_id, time: datetime, interval=5, refresh=False):
    upload_type = {
        5: '1',
        15: '2',
        60: '3',
        1440: '4'
    }

    assert interval in upload_type, '统计间隔时间错误'
    s_data = utlis.statistics(st_id, time, time - timedelta(minutes=interval))
    url = f'{ip}/api/1/trafficFlow'
    headers = dict(Authorization=f'bearer {getToken(refresh)}')
    data = dict(
        tsNo=st_id,                             # 站点编号
        lane=0,                                 # 车道号
        kind=1,                                 # 流量分类 1: 车道, 2: 段面
        statsTime=upload_type[interval],        # 统计间隔 1: 5min, 2: 15min, 3: 1hour, 4: 24hour
        gatherTime=f'{time:%H}',                # 统计时间
        statsDate=f'{time.timestamp():.0f}',    # 统计日期
        sedan=s_data.get('轿车', 0),              # 轿车数
        minbus=s_data.get('面包车', 0),            # 面包车数
        passengerCar=s_data.get('客车', 0),       # 客车数
        middleTruck=s_data.get('小货车', 0),       # 小货车数
        largeTruck=s_data.get('货车', 0),         # 大货车数
        cars=0,                                 # 通过车辆数折算成标准车 暂时传0
        speedAvg=0,                             # 平均速度 暂时传0
        queueLengthAvg=0                        # 平均排队长度 暂时传0
    )

    try:
        ret = requests.post(url, json=data, headers=headers).json()
        if ret['errcode'] == 0 and ret['content'] is True:
            return True
        elif ret['errcode'] == invilad_token_code:
            return statistics(st_id, time, True)
    except:
        pass
    return False
