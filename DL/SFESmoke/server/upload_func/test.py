from datetime import datetime, timedelta
import json
from logging import getLogger
from DBModel import Record

ip = None


def getTestRecord():
    record = Record()
    record.st_id = '0'
    record.st_name = '测试点'
    record.id = 123456789
    record.timestamp = 1504850340549
    record.Ringelmann = 2
    record.RingelmannLimit = 1
    record.car_lane = 1
    record.plate = 'test'
    record.plate_color = '黄'
    record.car_type = '小型车'
    record.car_color = '黄'
    record.img_plate_path = '1.jpg'
    record.img_smoke_path = '1.jpg'
    record.video_path = 'SFE/resource/video/smoke/001.avi'
    return record


def testUpload(func, record: Record = None):
    if record is None:
        record = getTestRecord()
    return func(record)


def upload(record: Record):
    getLogger("root").info("上传测试")
    return True
