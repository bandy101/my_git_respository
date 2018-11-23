# coding: utf-8
import os
from os import path
from datetime import datetime, timedelta


class RecordData:
    ''' 黑烟数据记录 '''

    def __init__(self):
        self.id = ''                # 记录ID
        self.timestamp = 0          # 记录13位时间戳

        self.st_id = 0              # 站点ID
        self.st_name = ''           # 站点名称

        self.Ringelmann = 0         # 林格曼黑度
        self.RingelmannLimit = 0    # 林格曼阈值

        self.plate = ''             # 车牌
        self.plate_color = ''       # 车牌颜色

        self.car_type = ''          # 车辆类型
        self.car_color = ''         # 车辆颜色
        self.car_lane = 1           # 车辆所在车道号

        self.img_plate_path = ''    # 车牌识别图像路径
        self.img_smoke_path = ''    # 黑烟判定图像路径
        self.video_path = ''        # 黑烟视频存放路径

    def toDict(self):
        return self.__dict__

    @staticmethod
    def fromDict(data: dict):
        record = RecordData()
        d = record.toDict()
        for k, v in data.items():
            if k in d:
                d[k] = v
        return record


STATISTICS_DICT_KEYS = (
    '其它车型',
    '小型车',
    '大型车',
    '客车',
    '货车',
    '轿车',
    '面包车',
    '小货车'
)


def statistics(st_id, start_time: datetime, end_time: datetime) -> dict:
    ''' 统计指定站点在指定时间返回内的车流量统计
    st_id: 站点ID
    start_time: 开始时间
    end_time: 结束时间
    return: 返回dict key:value=类型:数量
    '''
    # 车辆类型包括: 其它车型 小型车 大型车 客车 货车 轿车 面包车 小货车
    default = dict(
        其它车型=0,
        小型车=0,
        大型车=0,
        客车=0,
        货车=0,
        轿车=0,
        面包车=0,
        小货车=0
    )

    base_dir = '/FTP'
    ftp_dir = path.join(base_dir, st_id)
    if not path.isdir(ftp_dir):
        return default

    st = f'{start_time:%Y%m%d%H%M%S}'
    et = f'{end_time:%Y%m%d%H%M%S}'

    result = dict()
    for f in os.listdir(ftp_dir):
        if not f.lower().endswith('.jpg'):
            continue
        if not (st < f < et):
            continue

        f = path.splitext(f)[0]
        t = f.split('_')[-1]

        if t in result:
            result[t] += 1
        else:
            result[t] = 1

    default.update(result)
    return default
