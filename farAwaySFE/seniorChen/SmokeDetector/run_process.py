# coding: utf-8
import json
import logging
import logging.config
import os
import re
import stat
import sys
import threading
from argparse import ArgumentParser
from datetime import datetime, timedelta
from glob import glob
from os import path
from threading import Thread, Timer
from time import sleep
from queue import Queue
import pickle
import shutil
import json
from importlib import import_module

import cv2

from upload_func.utlis import RecordData
from SFE.SmokeDetector import SmokeDetector

''' config文件格式见 config文件说明.MD '''


class SmokeProcess():

    def __init__(self):
        self.__module_path = 'resource'  # 模型所在路径

    def __initStart(self, config_path):
        assert path.isfile(config_path), '配置文件不存在'

        # 加载配置文件
        with open(config_path, encoding='utf-8') as fp:
            self.__cfg = json.load(fp)
        self.__cfg['save_path'] = path.abspath(self.__cfg['save_path'])

        # 初始化日志设置
        self.__initLog(str(self.__cfg['id']), self.__cfg['save_path'])
        self.__log = logging.getLogger(str(self.__cfg['id']))
        self.__log.info('日志初始化完成')

        # 清除30天以前的记录
        self.__cleanData()
        self.__log.info('已清除过期数据')

        # 初始化记录上传方法
        models = self.__cfg.get('upload_func', '')
        self.__upload = []
        if models and isinstance(models, str):
            models = self.__getUploadModels(models)
            self.__upload.extend(self.__getFunc(models, 'upload'))

        # 初始化车流量统计上传方法
        models = self.__cfg.get('statistics', '')
        self.__statistics = []
        if models and isinstance(models, str):
            interval = self.__cfg.get('statis_interval', '')

            if isinstance(interval, int):
                interval = str(interval)

            if models.count('|') != interval.count('|'):
                self.__log.error(f'车流量统计函数与统计间隔数量不一致')
            else:
                interval = [int(i) for i in interval.split('|')]
                models = self.__getUploadModels(models)
                func = self.__getFunc(models, 'statistics')
                self.__statistics.extend(zip(func, interval))

        # 打开视频源
        try:
            self.__video = SmokeDetector(self.__cfg['video_source'], self.__module_path, self.__cfg['border'])
        except:
            self.__log.critical('打开视频源失败', exc_info=True)
            raise Exception('打开视频源失败')
        else:
            self.__log.info('视频源打开成功')
        self.__fps = self.__video.fps
        self.__size = self.__video.size

        self.__stop = False

    def __getUploadModels(self, models: str):
        ret = []
        for model_name in (i for i in models.split('|') if i):
            model_property = ''
            # 分割名称、属性
            if '[' in model_name:
                idx = model_name.index('[')
                model_name, model_property = model_name[:idx], model_name[idx:]

            # 获取模块
            try:
                model = import_module(f'upload_func.{model_name}')
                ret.append(model)
            except:
                self.__log.warning(f'不存在上传模块 {model_name}')
                continue

            # 设置属性
            for name, value in re.findall(r'\[(.*?)=(.*?)\]', model_property):
                setattr(model, name, value)

        return ret

    def __getFunc(self, models: list, func_name: str):
        ret = []
        for model in models:
            if hasattr(model, func_name):
                ret.append(getattr(model, func_name))
            else:
                self.__log.warning(f'模块 {model.__name__} 不存在方法 {func_name}')
        return ret

    def start(self, config_path, is_subprocess=False):
        ''' 开始检测
        config_path str: 配置文件路径
        is_subprocess bool[False]: 是否为子进程
        '''
        # 初始化
        self.__initStart(config_path)

        # 创建记录保存队列 启动记录保存线程
        self.__save_queue = Queue()
        Thread(target=self.__saveThread).start()

        # 启动定时上传
        if 'statistics' in self.__cfg:
            self.__statisticsUploadThread(False)

        # 启动等待停止线程
        if is_subprocess:
            Thread(target=self.__waitStopThread, daemon=True).start()

        # 开始检测视频
        try:
            while not self.__stop:
                # 读取数据
                frame, tracks, save_list = self.__video.nextFrame()

                # 保存视频
                if save_list:
                    frames = self.__video.getSaveFrames()
                for save in save_list:
                    if save.Ringelmann >= self.__cfg['Ringelmann']:
                        self.__save_queue.put((save, frames))

                if frame is None:
                    break

                # 跳帧
                for i in range(1):
                    self.__video.nextFrame(True)
        except:
            self.__log.error('检测过程中发生错误', exc_info=True)
        else:
            self.__log.warning('视频已结束/超时/停止')
        self.stop()

    def stop(self):
        self.__stop = True
        try:
            self.__timer.cancel()
        except:
            pass

    def __initLog(self, name, base_path):
        log_dir = path.join(base_path, 'logs')
        log_fn = 'log.log'
        log_path = path.join(log_dir, log_fn)

        if not path.isdir(log_dir):
            os.makedirs(log_dir)

        logging.config.dictConfig({
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'console': {
                    'format': f'[{name}][%(asctime)s][%(levelname)s]%(message)s'
                },
                'file': {
                    'format': f'[%(asctime)s][%(levelname)s]%(message)s'
                },
            },
            'handlers': {
                'console': {
                    'level': 'INFO',
                    'class': 'logging.StreamHandler',
                    'formatter': 'console'
                },
                'file': {
                    'level': 'INFO',
                    'class': 'logging.handlers.TimedRotatingFileHandler',   # 按时间分割日志文件
                    'when': 'midnight',         # 在00:00分割
                    'interval': 1,              # 间隔一天
                    'backupCount': 90,          # 最多保存90天
                    'filename': log_path,
                    'encoding': 'utf-8',
                    'formatter': 'file'
                }
            },
            'loggers': {
                name: {
                    'level': 'INFO',
                    'handlers': ['file', 'console']
                }
            }
        })

    def __track2record(self, track, file_list):
        record = RecordData()
        record.st_id = self.__cfg['id']
        record.st_name = self.__cfg['name']
        record.id = track.id
        record.timestamp = int(track.id[:13])
        record.Ringelmann = track.Ringelmann
        record.RingelmannLimit = self.__cfg['Ringelmann']
        record.car_lane = track.lane_no
        if track.plate:
            record.plate = track.plate
        if track.plate_color:
            record.plate_color = track.plate_color
        if track.car_type:
            record.car_type = track.car_type
        if track.car_color:
            record.car_color = track.car_color
        record.img_plate_path, record.img_smoke_path, record.video_path = file_list

        return record

    def __saveThread(self):
        ''' 保存队列中的黑烟记录 '''
        queue = self.__save_queue
        while True:
            if self.__stop and queue.empty():
                break
            try:
                data = queue.get(timeout=1)
                self.__saveRecord(*data)
            except:
                pass

    def __saveRecord(self, track, frames):
        savepath = path.join(self.__cfg['save_path'], track.id)
        # 创建保存目录
        os.makedirs(savepath, exist_ok=True)

        files = []
        # 保存图片
        try:
            for i, img in enumerate([track.smoke_image, track.plate_image]):
                p = path.join(savepath, f'{i}.jpg')
                cv2.imwrite(p, img)
                files.append(p)
        except:
            self.__log.error(f'ID:{track.id} 保存图片时出错', exc_info=True)
            return

        # 保存视频
        try:
            p = path.join(savepath, 'video.mp4')
            writer = cv2.VideoWriter(p, cv2.VideoWriter_fourcc(*'H264'), self.__fps, self.__size)
            assert writer.isOpened(), '视频打开失败'
            for img in frames:
                writer.write(img)
            writer.release()
            files.append(p)
        except:
            self.__log.error(f'ID:{track.id} 保存视频时出错', exc_info=True)
            return

        # 转换格式 更新数据
        record = self.__track2record(track, files)
        self.__setHKInfo(record)

        # 保存信息
        try:
            with open(path.join(savepath, 'record.json'), mode='w', encoding='utf-8') as fp:
                json.dump(record.toDict(), fp, ensure_ascii=False)
        except:
            self.__log.error(f'ID:{track.id} 保存黑烟信息时出错', exc_info=True)
        else:
            self.__log.info(f'ID:{track.id} 本地保存成功')

        # 上传记录
        for func in self.__upload:
            try:
                if func(record):
                    self.__log.info(f'{func.__module__} 上传 ID:{track.id} 成功')
                else:
                    self.__log.warning(f'{func.__module__} 上传 ID:{track.id} 失败')
            except:
                self.__log.error(f'{func.__module__} 上传 ID:{track.id} 时发生错误', exc_info=True)

    def __setHKInfo(self, record: RecordData):
        ''' 从海康数据中统合数据 '''
        if not record.plate:
            record.plate = '无车牌'
            return

        # 1504850340.549000 20170908135900549_甘AQF020_蓝_02_其它色_小型车.jpg
        ftp_dir = path.join('/FTP', self.__cfg['id'])
        if not path.isdir(ftp_dir):
            os.makedirs(ftp_dir)
            os.chmod(ftp_dir, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

        time = datetime.fromtimestamp(record.timestamp / 1000)
        st = f'{time + timedelta(seconds=-2):%Y%m%d%H%M%S}'  # 开始时间
        et = f'{time + timedelta(seconds=3):%Y%m%d%H%M%S}'  # 结束时间
        for fn in os.listdir(ftp_dir):
            if st < fn < et:
                fn = path.splitext(fn)[0]   # 去后缀名
                info = fn.split('_')[1:]    # 去时间
                if info[0] == track.plate:
                    record.plate, record.palte_color, record.car_lane, record.car_color[:-1], record.car_type = info
                    record.car_lane = int(record.car_lane)
                    break

    def __waitStopThread(self):
        ''' 启动等待停止线程 在处于子进程模式时被调用, 作用为等待接收父进程的停止指令, 收到时手动停止处理过程 '''
        while True:
            line = input()
            if line == 'stop' or self.__stop:
                self.stop()
                break

    def __statisticsUploadThread(self, upload=True):
        ''' 车流量上传线程 定时任务 每分钟读取配置文件中的上传函数、上传间隔, 满足上传间隔时间时调用上传函数 '''
        if upload:
            # 计算当前分钟数
            t = datetime.now()
            curr_min = t.hour * 60 + t.minute

            # 上传
            for func, interval in self.__statistics:
                if curr_min % interval == 0:
                    try:
                        if func(self.__cfg['id'], t, interval):
                            self.__log.info(f'{func.__module__} 上传车流量成功')
                        else:
                            self.__log.warning(f'{func.__module__} 上传车流量失败')
                    except:
                        self.__log.error(f'{func.__module__} 上传车流量时发生错误', exc_info=True)

        # 启动下一次定时任务
        if not self.__stop:
            self.__timer = Timer(60 - datetime.now().second,  self.__statisticsUploadThread)
            self.__timer.start()

    def __cleanData(self):
        # 获取30天前00:00的时间戳
        time = datetime.now()
        time = datetime(time.year, time.month, time.day)
        time = time - timedelta(days=30)

        save_path = self.__cfg['save_path']

        # 删除过期记录
        timestamp = time.timestamp() * 1000000
        for d in os.listdir(save_path):
            if path.isdir(d) and d.isnumeric() and int(d) <= time:
                p = path.join(save_path, d)
                shutil.rmtree(p, True)

        # 清除海康上传记录
        t = time.strftime('%Y%m%d')
        p = path.join('/FTP', self.__cfg['id'])
        if not path.isdir(p):
            return
        for fn in os.listdir(p):
            if fn < t:
                try:
                    os.remove(path.join(p, fn))
                except:
                    pass


if __name__ == '__main__':
    from fire import Fire
    p = SmokeProcess()

    Fire(p.start)
