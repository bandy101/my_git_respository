# coding: utf-8
from datetime import datetime, timedelta
import logging
from time import sleep

import requests

from . import utlis

invilad_token_code = 30006
ip = 'http://192.168.150.151:8055'
ver = 'v1'
token = None


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
    url = f'{ip}/api/{ver}/oauth/token'
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


def upload(record: utlis.RecordData, refresh=False, send_file=True):
    url = f'{ip}/api/{ver}/smokeMessage{"" if send_file else "Data"}'
    headers = dict(Authorization=f'bearer {getToken(refresh)}')
    t = datetime.fromtimestamp(record.timestamp / 1000)
    data = dict(
        monitorTimeStr=f'{t:%Y-%m-%d %H:%M:%M}:{t.microsecond/1000:03.0f}',              # 检测时间
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
        belonging='0',                                                               # ? 所属辖区 常量 未设置
        standard='0',                                                           # ? 排放标准 附录 13.2 常量 未设置
        hbflbz=0,                                                               # ? 环保分类标志
        status='0'                                                                # 审核结果 0: 待审核
    )
    if send_file:
        files = dict(
            file1=open(record.img_plate_path, 'rb'),
            file2=open(record.img_smoke_path, 'rb'),
            file3=open(record.video_path, 'rb')
        )
    else:
        files = None
    try:
        ret = requests.post(url, data=data, files=files, headers=headers)

        ret = ret.json()
        if ret['errcode'] == 0 and ret['content'] is True:
            return True
        elif ret['errcode'] == invilad_token_code:
            return upload(record, True, send_file)
    except:
        log = logging.getLogger(record.st_id)
        log.error(f'上传时发生异常, data={data}', exc_info=True)

    return False


def statistics(st_id, time: datetime, interval: int=0) -> bool:
    url = f'{ip}/api/{ver}/trafficFlow'
    headers = dict(Authorization=f'bearer {getToken()}')

    # 统计
    results = []
    for minute in range(0, 60, 5):
        start_time = datetime(time.year, time.month, time.day, time.hour, minute)
        results.append(utlis.statistics(st_id, start_time, start_time + timedelta(minutes=5)))

    for idx, key in enumerate(utlis.STATISTICS_DICT_KEYS):
        # 初始化数据
        data = dict(
            kind=idx + 1,
            tsNo=str(st_id),
            stNumberLogNo=time.strftime('%Y%m%d'),
            hour=time.hour,
            authorId='1',
            creationTimeStr=time.strftime('%Y-%m-%d')
        )

        # 初始化统计数据
        for i, result in enumerate(results):
            data[f'minute{(i+1)*5:02}'] = result[key]

        try:
            result = requests.post(url, json=data, headers=headers).json()
            if result['errcode'] != 0:
                print(result)
        except:
            log = logging.getLogger(st_id)
            log.error(f'车流量上传发生异常, data={data}', exc_info=True)
        sleep(0.1)

    return True
