# coding: utf-8
from datetime import datetime, timedelta
import logging
from time import sleep
from collections import defaultdict

import requests

from DBModel import Record

SERVER_LOG_NAME = "server"


class Upload():
    # 车牌颜色
    __plate_color = defaultdict(lambda: "10",
                                蓝='1',
                                黄='2',
                                白='3',
                                黑='4',
                                绿='5',
                                黄绿='6'
                                )
    # 车辆类型
    __plate_type = defaultdict(lambda: "99",
                               大型汽车="01",
                               小型汽车="02",
                               使馆汽车="03",
                               领馆汽车="04",
                               境外汽车="05",
                               外籍汽车="06",
                               #    两三轮摩托车="07",
                               #    轻便摩托车="08",
                               #    使馆摩托车="09",
                               #    领馆摩托车="10",
                               #    境外摩托车="11",
                               #    外籍摩托车="12",
                               农用运输车="13",
                               拖拉机="14",
                               挂车="15",
                               教练汽车="16",
                               #    教练摩托车="17",
                               #    试验汽车="18",
                               #    试验摩托车="19",
                               #    临时入境汽车="20",
                               #    临时入境摩托车="21",
                               #    临时行驶车="22",
                               警用汽车="23",
                               #    警用摩托="24",
                               大型新能源汽车="51",
                               小型新能源汽车="52",
                               )

    # 车身颜色
    __car_color = defaultdict(lambda: "0",
                              白="1",
                              银="2",
                              灰="3",
                              黑="4",
                              红="5",
                              深蓝="6",
                              蓝="7",
                              黄="8",
                              绿="9",
                              棕="10",
                              粉="11",
                              紫="12",
                              深灰="13",
                              青="14",
                              未进行车身颜色识别="0xff",
                              )

    # 车辆类型
    __car_type = defaultdict(lambda: "0",
                             客车="1",
                             货车="2",
                             轿车="3",
                             面包车="4",
                             小货车="5",
                             行人="6",
                             二轮车="7",
                             三轮车="8",
                             SUV="9",
                             MPV="9",
                             中型客车="10",
                             机动车="11",
                             非机动车="12",
                             小型轿车="13",
                             微型轿车="14",
                             皮卡车="15",
                             )
    __car_type["SUV/MPV"] = "9"

    def __init__(self, ip, ver, user, pwd):
        self.invilad_token_code = 30006
        self.token = None
        self.TIMEOUT = 5
        self.ip = ip
        self.ver = ver
        self.user = user
        self.pwd = pwd

    def getToken(self, refresh=False):
        if (not refresh) and self.token:
            return self.token
        url = "{}/api/{}/oauth/token".format(self.ip, self.ver)
        data = dict(
            clientId='098f6bcd4621d373cade4e832627b4f6',
            userName=self.user,
            password=self.pwd,
            captchaCode='232',
            captchaValue='232'
        )

        try:
            ret = requests.post(url, json=data, timeout=self.TIMEOUT).json()
            if ret['errcode'] == 0:
                self.token = ret['content']['accessToken']
        except:
            self.token = ''

        return self.token

    def upload(self, record: Record, refresh=False, send_file=True) -> bool:
        url = "{}/api/{}/smokeMessage{}".format(self.ip, self.ver, "" if send_file else "Data")
        headers = dict(Authorization="bearer {}".format(self.getToken(refresh)))
        t = datetime.fromtimestamp(record.timestamp / 1000)
        data = dict(
            monitorTimeStr=t.strftime("%Y-%m-%d %H:%M:%S:%f"),  # 检测时间
            tsNo=record.st_id,  # 站点编号 yyyy-MM-dd HH:mm:ss:SSS
            line='0',  # ? 检测线编号 常量 未设置
            lane=record.car_lane,  # 车道号
            ringelman=record.Ringelmann,  # 林格曼黑度
            ringelmanLimit=record.RingelmannLimit,  # 林格曼黑度阈值
            license=record.plate,  # 车牌
            licenseCode=self.__plate_type[record.plate_type],  # 车牌类型 GA 24.7
            licenseType=self.__plate_color[record.plate_color],  # 车牌颜色 对照表
            vehicleType=self.__car_type[record.car_type],  # 车辆类型 对照表
            vehicleColor=self.__car_color[record.car_color],  # 车辆颜色 GA 24.8
            fuelType='0',  # ? 燃油种类
            belonging='0',  # ? 所属辖区 常量 未设置
            standard='0',  # ? 排放标准 附录 13.2 常量 未设置
            hbflbz=0,  # ? 环保分类标志
            status='0'  # 审核结果 0: 待审核
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
            ret = requests.post(url, data=data, files=files, headers=headers, timeout=self.TIMEOUT)
            ret = ret.json()
            if ret['errcode'] == 0 and ret['content'] is True:
                return True
            elif ret['errcode'] == self.invilad_token_code:
                return self.upload(record, True, send_file)
        except:
            log = logging.getLogger(SERVER_LOG_NAME)
            log.error("[upload][{}]上传时发生异常, data={}".format(record.st_id, data), exc_info=True)
        finally:
            if files:
                for fp in files.values():
                    fp.close()

        return False


U_upload = Upload(ip="http://smoke.etc-cn.com", ver="v1", user="sfesmoke", pwd="ekoms")
upload = U_upload.upload
