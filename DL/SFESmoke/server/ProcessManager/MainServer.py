import logging
import logging.config
import os
from os import path
import sys
from subprocess import Popen, STDOUT
from datetime import datetime, timedelta
from time import sleep
import json
from threading import Thread, RLock
from typing import Callable
import shutil

from sqlalchemy import or_, and_

PATH = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(PATH)

from common import COMMAND
from DBModel import Session, Record
from ProcessManager.ConfigManager import ConfigManager
from ProcessManager.Log import Log
from ProcessManager.SocketServer import SocketServer
from ProcessManager.Uploader import Uploader
from ProcessManager.TimerServer import TimerServer, TimerTask


def getDefaultConfig():
    """ 获取默认的服务器配置 """
    return {
        "server_name": "测试站点",           # 服务站点名称
        "log_dir": "./logs",                # 服务日志存放目录
        "socket_port": 12345,               # 本地socket服务端口
        "rtmp_host": "127.0.0.1",           # 本地RTMP推送地址
        "auth_code_path": "./auth_code",    # 授权码文件存放路径
        "config_dir": "./config",           # 黑烟站点存放目录
        "net_rtmp_host": None,              # RTMP外网访问地址
    }


class MainServer(Log):

    """ 主服务类 """

    # 初始化 -------------------------------------

    __LOG_NAME: str = "server"
    __rlock = RLock()

    def __init__(self, config_path: str=None):
        """ 黑烟检测主服务程序
        - config_path str[None]: 主服务配置路径
        """

        self.loadServerConfig(config_path)

        # 初始化目录
        os.makedirs(self.CONFIG_DIR, exist_ok=True)

        # 初始化日志
        self.__initLog()

        # 初始化父类
        super().__init__("[MAIN]", self.__LOG_NAME)
        self._info("正在进行初始化...")

        self._info("当期服务配置为: {}".format(json.dumps(self._config, ensure_ascii=False, indent=4)))

        # 初始化配置管理
        self.config_manager = ConfigManager(self.CONFIG_DIR, self.__LOG_NAME)

        # 初始化上传服务
        self.uploader = Uploader(self.__LOG_NAME, None)
        self.loadUploadFunc()

        # 初始化定时作业服务
        self.timer_server = TimerServer(self.__LOG_NAME)
        # 记录上传 间隔1小时
        self.timer_server.add(1 * 60 * 60, TimerTask("UPLOAD", self.uploader.upload))
        # 记录删除 间隔12小时
        self.timer_server.add(12 * 60 * 60, TimerTask("CLEAN", self.cleanRecord))
        # 配置状态 间隔2秒
        self._status_dict = dict()
        self._status_rtmp_dict = dict()
        self.timer_server.add(2, TimerTask("STATUS", self.updateStatus))

        # 初始化Socket服务
        self.socket_server = SocketServer(self.__LOG_NAME)

        self.__is_auto = False

        self._info("初始化完成")

    def __del__(self):
        self.stopServer()

    def __lock(func):
        def wrap(self, *args, **kwargs):
            self.__rlock.acquire()
            try:
                return func(self, *args, **kwargs)
            finally:
                self.__rlock.release()
        return wrap

    def loadServerConfig(self, config_path: str):
        """ 加载服务器配置
        - config_path str: 配置文件路径
        """
        if isinstance(config_path, str):
            with open(config_path, encoding="utf-8") as fp:
                config = json.load(fp)
        else:
            config = dict()
        is_reload = hasattr(self, "_config")
        self._config = getDefaultConfig()
        self._config.update(config)
        if is_reload:
            self._info("已重载服务器配置, 当前配置为: {}".format(json.dumps(self._config, ensure_ascii=False, indent=4)))

    def startServer(self):
        """ 启动所有服务 """
        self.timer_server.startServer()
        for _ in range(3):
            if self.socket_server.startServer(self.SOCKET_PORT):
                break
        else:
            err = "Socket服务启动失败, 主服务无法启动"
            self._critical(err)
            raise Exception(err)

    def stopServer(self):
        """ 停止所有服务 """
        self.auto = False
        self.timer_server.stopServer()
        self.shutdownAll()
        self.socket_server.stopServer()

    # 检测控制 -----------------------------------------------

    @__lock
    def startProcess(self, id: str, start: bool=False, rtmp: bool=False) -> bool:
        """ 启动检测进程
        - id str: 配置ID
        - start bool[False]: 是否在启动进程的同时启动检测
        - rtmp bool[False]: 是否在启动进程的同时启动RTMP推送（启动推送时会启动检测）
        """
        if self.config_manager.getConfig(id) is None:
            self._warning("ID: {} 不存在".format(id))
            return False

        import run_process
        cmd = '"{}" "{}" --config-path "{}" --auth-code {} --rtmp-host {} - connect --address 127.0.0.1:{} --start {} --rtmp {}'.format(
            sys.executable,
            run_process.__file__,
            self.config_manager.getConfigPath(id),
            self.auth_code,
            self.RTMP_HOST,
            self.SOCKET_PORT,
            start,
            rtmp
        )
        self._info("启动子进程: {}".format(cmd))
        Popen(cmd, shell=True, stdout=open(os.devnull, "w"), stderr=STDOUT)
        # Popen(cmd, shell=True)
        return True

    @__lock
    def start(self, id: str, rtmp: bool=False) -> bool:
        """ 启动黑烟检测
        - id str: 配置ID
        - rtmp bool[False]: 是否在启动检测的同时启动RTMP推送
        """
        if id not in self.socket_server.client_dict:
            return self.startProcess(id, True, rtmp)
        return self.socket_server.sendCommand(id, COMMAND.START)[0]

    @__lock
    def restart(self, id: str) -> bool:
        """ 重启黑烟检测
        - id str: 配置ID
        """
        if id not in self.socket_server.client_dict:
            return self.start(id)
        return self.socket_server.sendCommand(id, COMMAND.RESTART)[0]

    @__lock
    def reload(self, id: str) -> bool:
        """ 重载黑烟检测配置
        - id str: 配置ID
        """
        if id not in self.socket_server.client_dict:
            return True
        return self.socket_server.sendCommand(id, COMMAND.RELOAD)[0]

    def stop(self, id: str) -> bool:
        """ 停止黑烟检测
        - id str: 配置ID
        """
        if id not in self.socket_server.client_dict:
            return True
        return self.socket_server.sendCommand(id, COMMAND.STOP)[0]

    def shutdown(self, id: str) -> bool:
        """ 关闭黑烟检测进程
        - id str: 配置ID
        """
        if id not in self.socket_server.client_dict:
            return True
        return self.socket_server.sendCommand(id, COMMAND.SHUTDOWN)[0]

    def _status(self, id: str) -> str:
        """ 立即获取黑烟检测运行状态
        - id str: 配置ID
        - return str: 所有状态包括`未启动`,`未知`,`未启动`,`正在检测`,`就绪`
        """
        if id not in self.socket_server.client_dict:
            return "未启动"
        e, s = self.socket_server.sendCommand(id, COMMAND.STATUS)
        if e is False:
            return "未知"
        if s is None:
            return "未启动"
        if s == "1":
            return "正在检测"
        return "就绪"

    def status(self, id: str) -> str:
        """ 获取黑烟检测运行状态
        - id str: 配置ID
        - return str: 所有状态包括`未启动`,`未知`,`未启动`,`正在检测`,`就绪`
        """
        return self._status_dict.get(id, "未启动")

    @__lock
    def startAll(self):
        """ 启动所有黑烟检测 """
        for _id in self.config_manager.getConfigIdList():
            self.start(_id)

    def stopAll(self):
        """ 停止所有黑烟检测 """
        for _id in self.socket_server.client_dict:
            self.stop(_id)

    def shutdownAll(self):
        """ 关闭所有黑烟检测进程 """
        for _id in self.socket_server.client_dict:
            self.shutdown(_id)

    @__lock
    def startRTMP(self, id: str) -> bool:
        """ 启动RTMP推送
        - id str: 配置ID
        """
        if id not in self.socket_server.client_dict:
            self.start(id, True)
        return self.socket_server.sendCommand(id, COMMAND.RTMP_START)[0]

    def stopRTMP(self, id: str) -> bool:
        """ 停止RTMP推送
        - id str: 配置ID
        """
        if id not in self.socket_server.client_dict:
            return True
        return self.socket_server.sendCommand(id, COMMAND.RTMP_STOP)[0]

    def _RTMPStatus(self, id: str) -> bool:
        """ 立即查看RTMP状态
        - id str: 配置ID
        """
        if id not in self.socket_server.client_dict:
            return False
        e, s = self.socket_server.sendCommand(id, COMMAND.RTMP_STATUS)
        return e is True and s == "1"

    def RTMPStatus(self, id: str) -> bool:
        """ 查看RTMP状态
        - id str: 配置ID
        """
        return self._status_rtmp_dict.get(id, False)

    def updateStatus(self):
        """ 更新配置运行状态、RTMP状态 """
        id_list = list(self.socket_server.client_dict.keys())
        self._status_dict = {_id: self._status(_id) for _id in id_list}
        self._status_rtmp_dict = {_id: self._RTMPStatus(_id) for _id in id_list}

    # 属性 ----------------------------------

    @property
    def SERVER_NAME(self) -> str:
        """ 服务器名称 """
        return self._config["server_name"]

    @property
    def SERVER_CONFIG(self) -> dict:
        """ 服务器配置 """
        return self._config

    @property
    def RTMP_HOST(self) -> str:
        """ 内部RTMP推送地址 """
        return self._config["rtmp_host"]

    @property
    def NET_RTMP_HOST(self) -> str:
        """ 外部RTMP访问地址 """
        return self._config["net_rtmp_host"]

    @property
    def SOCKET_PORT(self) -> int:
        """ Socket服务绑定的端口 """
        return self._config["socket_port"]

    @property
    def CONFIG_DIR(self) -> str:
        """ 黑烟配置的文件夹路径 """
        return self._config["config_dir"]

    @property
    def LOG_DIR(self) -> str:
        """ 服务日志文件夹路径 """
        return self._config["log_dir"]

    @property
    def auto(self) -> bool:
        """ 自动启动检测 """
        return self.__is_auto

    @auto.setter
    def auto(self, value: bool):
        """ 自动启动检测 """
        if value == self.__is_auto:
            return
        self.__is_auto = value
        if value:
            self.timer_server.add(10, TimerTask("AUTO", self._autoEvent))
        else:
            self.timer_server.remove("AUTO")

    @property
    def auth_code(self) -> str:
        """ 授权码 """
        p = self._config["auth_code_path"]
        if path.isfile(p):
            with open(p, encoding="utf-8") as fp:
                return fp.read().strip()
        return None

    @auth_code.setter
    def auth_code(self, value: str) -> str:
        """ 授权码 """
        p = self._config["auth_code_path"]
        with open(p, "w", encoding="utf-8") as fp:
            fp.write(str(value))

    # 辅助方法 ---------------------------------------------

    def cleanRecord(self, days1: int=30, days2: int=90):
        """ 清除指定天数以前的黑烟记录
        - days1 int[30]: 已确认未上传记录最长保留时间
        - days2 int[90]: 未确认记录最长保留时间
        """
        sess = Session()
        timestamp1 = int((datetime.now() - timedelta(days=days1)).timestamp() * 1000)
        timestamp2 = int((datetime.now() - timedelta(days=days2)).timestamp() * 1000)
        try:
            # 查询过期记录
            records = sess.query(Record.id, Record.save_dir).filter(
                or_(
                    and_(
                        Record.timestamp < timestamp1,
                        Record.status == True,
                        Record.upload_status == "0"
                    ),
                    and_(
                        Record.timestamp < timestamp2,
                        Record.status == False,
                    )
                )
            ).all()
            # 尝试删除记录文件夹
            delete_list = []
            for _id, _dir in records:
                if path.isdir(_dir) is False:
                    delete_list.append(_id)
                else:
                    try:
                        shutil.rmtree(_dir)
                        delete_list.append(_id)
                    except:
                        pass

            # 删除记录
            count = 0
            if delete_list:
                count = sess.query(Record).filter(Record.id.in_(delete_list)).delete(False)
                sess.commit()
            self._info("[CLEAN]共找到符合条件记录{}条, 删除{}条".format(len(records), count))
        except:
            sess.rollback()
            self._warning("[CLEAN]记录删除失败", exc_info=True)

    def _autoEvent(self):
        def getT(time):
            if isinstance(time, str):
                hour, minute = map(int, time.split(":"))
            elif isinstance(time, datetime):
                hour, minute = time.hour, time.minute
            return hour * 60 + minute

        _start = False  # 标志位 每轮最多启动一次进程
        for config in self.config_manager.getConfigList():
            _id = config.id
            t = getT(datetime.now())
            status = self.status(_id)
            # 自动停止
            if config.stop_time and t >= getT(config.stop_time):
                if status != "未启动":
                    self.shutdown(_id)
            # 自动启动
            elif config.start_time and getT(config.start_time) <= t < getT(config.stop_time):
                if status == "就绪":
                    self.start(_id)
                elif status == "未启动" and _start is False:
                    _start = True
                    self.start(_id)

    def loadUploadFunc(self):
        """ 加载上传方法 """
        upload_dict = dict()
        # 获取上传方法
        for _id in self.config_manager.getConfigIdList():
            config = self.config_manager.getConfig(_id)
            for u in (config.upload_func or "").split("|"):
                if not u:
                    continue
                upload_dict.setdefault(u, [])
                upload_dict[u].append(_id)
        self.uploader.loadUploadModule(upload_dict)

    def __initLog(self):
        """ 初始化日志模块 """
        os.makedirs(self.LOG_DIR, exist_ok=True)
        log_path = path.join(self.LOG_DIR, "log.log")
        logging.config.dictConfig({
            'version': 1,
            'disable_existing_loggers': True,
            'formatters': {
                'console': {
                    'format': '[%(asctime)s][%(levelname)s]%(message)s'
                },
                'file': {
                    'format': '[%(asctime)s][%(levelname)s]%(message)s'
                },
            },
            'handlers': {
                'console': {
                    'level': 'DEBUG',
                    'class': 'logging.StreamHandler',
                    'formatter': 'console'
                },
                'file': {
                    'level': 'INFO',
                    'class': 'logging.handlers.TimedRotatingFileHandler',   # 按时间分割日志文件
                    'when': 'midnight',         # 在00:00分割
                    'interval': 1,              # 间隔一天
                    'backupCount': 30,          # 最多保存90天
                    'filename': log_path,
                    'encoding': 'utf-8',
                    'formatter': 'file'
                }
            },
            'loggers': {
                self.__LOG_NAME: {
                    'level': 'DEBUG',
                    'handlers': ['file', 'console']
                }
            }
        })
