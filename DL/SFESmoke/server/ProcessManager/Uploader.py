"""
记录上传模块
"""
from typing import Dict, List, Callable
from time import sleep
from datetime import datetime
from threading import Thread
from logging import Logger

from SFE import loadModule


from DBModel import Session, Record

from ProcessManager.Log import Log


class UploadInfo:
    def __init__(self, name: str=None, func: Callable=None, stations: List[str]=None):
        self.name = name
        self.func = func
        self.stations = stations


class Uploader(Log):

    def __init__(self, log_name: str, upload_dict: Dict[str, List[str]]):
        """
        - log_name str: 日志名称
        - upload_dict: 需要上传的站点信息 key: 上传模块名称, value: 站点列表
        """
        super().__init__("[UPLOAD]", log_name)

        self.upload_dict = dict()
        if upload_dict:
            self.loadUploadModule(upload_dict)

        self.__stop = True

    def loadUploadModule(self, upload_dict: Dict[str, List[str]]):
        """ 加载上传模块 """
        res = dict()
        for name, stations in upload_dict.items():
            # 加载模块
            module = loadModule("upload_func.{}".format(name))
            if module is None:
                self._warning("上传模块: `{}`不存在".format(name))
                continue

            # 获取上传方法
            func = getattr(module, "upload", None)
            if func is None:
                self._warning("上传模块: `{}`中不存在上传方法".format(name))
            else:
                res[name] = UploadInfo(name=name, func=func, stations=stations)

        self.upload_dict = res
        self._info("上传模块加载完成")

    def upload(self):
        """ 执行一次上传操作 """
        sess = Session()
        for info in self.upload_dict.values():
            try:
                records = sess.query(Record).filter(Record.upload_status == "1", Record.st_id.in_(info.stations)).all()
                for record in records:
                    if info.func(record):
                        record.upload_status = "2"
                        sess.commit()
                        self._info("[{}]上传成功".format(info.name))
                    else:
                        self._warning("[{}]上传失败".format(info.name), exc_info=True)
            except:
                sess.rollback()
                self._warning("[{}]上传失败".format(info.name), exc_info=True)
        sess.close()
