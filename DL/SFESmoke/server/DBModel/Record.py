import os
from os import path
from datetime import datetime

from sqlalchemy import Column, DateTime, String, Index, BigInteger, SmallInteger, Boolean

from DBModel import ModelBase


class Record(ModelBase):
    __tablename__ = "t_record"

    # 字段 -----------------------------------
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    # 检测时间
    timestamp = Column(BigInteger, nullable=False)
    # 站点ID
    st_id = Column(String(50), nullable=False)
    # 站点名称
    st_name = Column(String(50), nullable=False)

    # 林格曼黑度
    Ringelmann = Column(SmallInteger, nullable=False)
    # 林格曼黑度阈值
    RingelmannLimit = Column(SmallInteger, nullable=False)

    # 车牌号
    plate = Column(String(50), nullable=False)
    # 车牌颜色
    plate_color = Column(String(10), nullable=False)
    # 车牌类型
    plate_type = Column(String(10), nullable=False)

    # 车辆类型
    car_type = Column(String(50), nullable=False)
    # 车辆颜色
    car_color = Column(String(10), nullable=False)
    # 车道号
    car_lane = Column(SmallInteger, nullable=False)

    # 文件保存目录
    save_dir = Column(String(1024), nullable=False)

    # 审核状态
    status = Column(Boolean, nullable=False, default=False)
    # 上传状态
    upload_status = Column(String(16), nullable=False, default="0")

    # 索引 -------------------------------------
    Index("idx_sid_time", st_id, timestamp)

    # 属性 -------------------------------------
    @property
    def check_time(self) -> datetime:
        """ 检测时间 由`timestamp`字段转换 """
        return datetime.fromtimestamp(int(self.timestamp) / 1000)

    @property
    def img_plate_path(self) -> str:
        """ 车辆识别图片路径 """
        return path.join(self.save_dir, "0.jpg")

    @property
    def img_smoke_path(self) -> str:
        """ 黑烟识别图片路径 """
        return path.join(self.save_dir, "1.jpg")

    @property
    def video_path(self) -> str:
        """ 视频路径 """
        return path.join(self.save_dir, "video.mp4")

    # 类方法 -----------------------------------

    @classmethod
    def fromTrackObject(cls, track, st_id: str, st_name: str, RingelmannLimit: int, save_dir: str):
        """ 从追踪对象中生成`Record`
        - track SFE.SmokeDetector.TrackObject: 追踪对象
        - st_id str: 站点ID
        - st_name str: 站点名称
        - RingelmannLimit int: 林格曼黑度阈值
        - save_dir str: 文件保存目录
        """
        record = cls()
        record.st_id = st_id
        record.st_name = st_name or "未命名站点"
        record.timestamp = int(track.timestamp * 1000)
        record.Ringelmann = track.Ringelmann
        record.RingelmannLimit = RingelmannLimit
        record.car_lane = track.lane_no
        record.plate = track.plate or "无车牌"
        record.plate_color = track.plate_color or "其他"
        record.plate_type = track.plate_type or "其他"
        record.car_type = track.car_type or "其它车型"
        record.car_color = track.car_color or "其他"
        record.save_dir = save_dir

        return record
