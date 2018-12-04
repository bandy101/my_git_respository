# coding: utf-8
import logging
import logging.config
import os
from os import path
from datetime import datetime, timedelta
from threading import Thread, Timer
from time import sleep
from queue import Queue, Empty
import shutil
from subprocess import Popen, PIPE, STDOUT

import cv2

from common import Config, RTMP, COMMAND
from DBModel import Record, Session
from SFE import loadModule
from SFE.SmokeDetector import SmokeDetector, TrackObject
from SFE.Tools import drawLabel

''' config文件格式见 config文件说明.MD '''


class SmokeProcess():

    def __init__(self, config_path: str, auth_code: str, rtmp_host: str=None):
        ''' 黑烟采集进程
        - config_path str: 配置文件路径
        - auth_code str: 授权码
        - rtmp_host str[None]: RTMP流推送地址 默认为`127.0.0.1` 流将推送到`rtmp://rtmp_host/live/id`
        '''
        self.__config_path = config_path
        self.loadConfig()

        self.__auth_code = auth_code

        # RTMP流设置初始化
        self.__rtmp_host = rtmp_host
        self.__rtmp_play = False
        self.__rtmp = None
        self.__rtmp_frame_size = (800, 600)
        self.__rtmp_bitrate = 2048

        self.__stop = True
        self.__video = None

    def loadConfig(self):
        """ 加载配置文件 """
        config_path = self.__config_path
        if not path.isfile(config_path):
            raise FileNotFoundError("配置文件不存在")

        # 加载配置文件
        self.__cfg = Config.load(config_path)
        err = self.__cfg.check()
        if err:
            raise Exception(err)

        # 初始化保存目录
        save_path = path.abspath(self.__cfg.save_path)
        self.__record_dir = path.join(save_path, 'record')
        self.__log_dir = path.join(save_path, 'logs')
        for p in [self.__record_dir,  self.__log_dir]:
            os.makedirs(p, exist_ok=True)

        # 初始化日志设置
        self.__initLog(str(self.__cfg.id))
        self.__log = logging.getLogger(str(self.__cfg.id))
        self.__log.info('配置加载完成')

    def start(self, rtmp=False, thread=False):
        """ 开始检测
        - rtmp bool[False]: 是否在开始后启动推流
        - thread bool[False]: 是否以线程模式启动
        """
        if not self.__stop:
            return

        if thread:
            Thread(target=self.start, args=(rtmp, False)).start()
            return

        # 打开视频源
        self.__stop = False
        try:
            self.__video = SmokeDetector(self.__cfg.video_source, self.__cfg.border, auth_code=self.__auth_code)
        except:
            self.__log.critical("启动失败", exc_info=True)
            self.stop()
            return
        else:
            self.__log.info('视频源打开成功')

        self.__fps = self.__video.fps
        self.__size = self.__video.size

        if rtmp is True:
            self.rtmp_play = True

        # 创建记录保存队列 启动记录保存线程
        queue = Queue()
        Thread(target=self.__saveThread, args=(queue, )).start()
        self.__log.info("记录保存线程已启动")

        # 开始检测视频
        # 设置一轮读取几帧视频 每轮只有第一帧记录跟踪信息
        frame_skip = 2
        epoch_frame = list(range(frame_skip))
        try:
            while not self.__stop:
                for skip in epoch_frame:
                    # 读取数据
                    frame, tracks, save_list = self.__video.nextFrame(only_frame=skip)
                    if not skip:
                        draw_tracks = tracks

                    # 保存记录
                    if save_list:
                        frames = self.__video.getSaveFrames()
                        for save in save_list:
                            if save.Ringelmann >= self.__cfg.Ringelmann:
                                queue.put((save, frames))
                        del frames

                    # 是否停止
                    if frame is None:
                        break

                    # 是否推流
                    if self.rtmp_play:
                        frame = frame.copy()
                        for track in draw_tracks:
                            result = track.last_result
                            color = (0, 0, 255) if track.smoke_count >= 3 else (0, 255, 0)

                            cv2.rectangle(frame, *result.car_rect, color, 2)
                        if self.__rtmp:
                            err = self.__rtmp.write(frame)
                            if err is not True:
                                self.__log.error('推流时发生错误 正在手动停止RTMP流推送, stdout/stderr={}'.format(err))
                                self.rtmp_play = False

                if frame is None:
                    break
        except:
            self.__log.error('检测过程中发生错误, 检测已停止', exc_info=True)
        else:
            self.__log.warning('视频已结束/超时/停止')
        finally:
            del self.__video
            self.__video = None
            self.stop()

    def stop(self):
        """ 停止检测 """
        self.rtmp_play = False
        if not self.__stop:
            self.__stop = True
            sleep(0.5)

    def restart(self, reload=False, thread=False):
        """ 重启检测
        - reload bool[False]: 是否重新加载配置
        - thread bool[False]: 启动检测时是否以线程模式启动
        """
        is_rtmp = self.rtmp_play

        self.stop()

        if reload:
            self.loadConfig()

        self.start(is_rtmp, thread)
        self.__log.info("重启完成")

    @property
    def rtmp_play(self):
        return self.__rtmp_play

    @rtmp_play.setter
    def rtmp_play(self, value):
        if value:
            if self.rtmp_play is False:
                self.__rtmp = RTMP(self.__cfg.id, self.__video.fps, self.__video.size, self.__rtmp_frame_size, self.__rtmp_bitrate, host=self.__rtmp_host)
                self.__rtmp_play = True
                self.__log.info('启动RTMP流推送')
        else:
            if isinstance(self.__rtmp, RTMP):
                self.__rtmp.stop()
                self.__log.info('停止RTMP流推送')
            self.__rtmp = None
            self.__rtmp_play = False

    def __initLog(self, name):
        """ 初始化日志模块 """
        log_path = path.join(self.__log_dir, "log.log")
        logging.config.dictConfig({
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'console': {
                    'format': '[{name}][%(asctime)s][%(levelname)s]%(message)s'.format(name=name)
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
                    'backupCount': 90,          # 最多保存90天
                    'filename': log_path,
                    'encoding': 'utf-8',
                    'formatter': 'file'
                }
            },
            'loggers': {
                name: {
                    'level': 'DEBUG',
                    'handlers': ['file', 'console']
                }
            }
        })

    def __saveThread(self, queue: Queue):
        ''' 保存队列中的黑烟记录 '''
        while True:
            if self.__stop is True and queue.empty():
                self.__log.info("所有记录保存完成，记录保存线程已退出。")
                break
            try:
                data = queue.get(timeout=.1)
                self.__saveRecord(*data)
            except Empty:
                pass
            except:
                self.__log.warning("保存记录时出现异常", exc_info=True)

    def __saveRecord(self, track, frames):
        """ 保存黑烟记录 """
        savepath = path.join(self.__record_dir, datetime.fromtimestamp(track.timestamp).strftime("%Y%m%d%H%M%S.%f"))
        # 创建保存目录
        while True:
            if path.exists(savepath):
                # 检查记录是否已保存过
                record = Record.fromJSON(savepath)
                if record.id == track.id:
                    del frames
                    return
                savepath += "_"
            else:
                break
        os.makedirs(savepath, exist_ok=True)

        # 保存图片
        try:
            for i, img in enumerate([track.plate_image, track.smoke_image]):
                p = path.join(savepath, '{}.jpg'.format(i))
                cv2.imwrite(p, img)
        except:
            self.__log.error('保存记录图片时出现错误', exc_info=True)
            shutil.rmtree(savepath)
            return

        # 保存视频
        sub = None
        try:
            p = path.join(savepath, 'video.mp4')
            cmd = "ffmpeg -f rawvideo -pix_fmt bgr24 -an -s {width}*{height} -i - -r {fps} -b:v 4096k -bufsize 4096k -c:a avc -c:v h264 {file}".format(
                fps=self.__fps,
                file=p,
                width=self.__size[0],
                height=self.__size[1]
            )
            sub = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT, shell=True)
            while frames:
                sub.stdin.write(frames.pop(0))
            sub.stdin.close()
            sub.wait()

        except:
            self.__log.error('保存记录视频时出错', exc_info=True)
            if isinstance(sub, Popen):
                if sub.stdout.readable():
                    self.__log.error("stdout/stderr:{}".format(sub.stdout.read()))
            shutil.rmtree(savepath)
            return
        finally:
            del frames

        # 转换格式 更新数据
        record = Record.fromTrackObject(track, self.__cfg.id, self.__cfg.name, self.__cfg.Ringelmann, savepath)

        # 保存记录
        sess = Session()
        try:
            sess.add(record)
            sess.commit()
            self.__log.info('记录保存成功')
        except:
            sess.rollback()
            self.__log.error('保存黑烟信息时出错', exc_info=True)
            shutil.rmtree(savepath)
        finally:
            sess.close()

    def __excCommand(self, cmd: COMMAND, client):
        """ 执行指定指令
        - cmd COMMAND: 要执行的指令
        """
        if cmd is None:
            self.__log.warning("[command]未知指令: `{}`".format(line))
        if cmd == COMMAND.SHUTDOWN:
            self.stop()
        elif cmd == COMMAND.RESTART:
            self.restart(thread=True)
        elif cmd == COMMAND.RELOAD:
            if self.__stop:
                self.loadConfig()
            else:
                self.restart(reload=True, thread=True)
        elif cmd == COMMAND.START:
            self.start(thread=True)
        elif cmd == COMMAND.STOP:
            self.stop()
        elif cmd == COMMAND.STATUS:
            client.send(b"0" if self.__stop else b"1")
        elif cmd == COMMAND.RTMP_START:
            if self.__stop:
                self.start(True, True)
            else:
                self.rtmp_play = True
        elif cmd == COMMAND.RTMP_STOP:
            self.rtmp_play = False
        elif cmd == COMMAND.RTMP_STATUS:
            client.send(b"1" if self.rtmp_play else b"0")

    def connect(self, address: str, start: bool=False, rtmp: bool=False):
        r''' 连接到指定socket服务并等待指令
        - address str: socket服务地址 形式为"ip:port" 如 "127.0.0.1:8888"
        - start bool[False]: 是否在连接成功后立即启动检测
        - rtmp bool[False]: 是否在启动检测的同时开始推送rtmp

        socket连接成功后支持以下指令(所有指令以"\n"结尾):
        - "shutdown": 停止并关闭程序
        - "start": 启动检测
        - "stop": 停止检测
        - "restart": 重启检测
        - "reload": 重新加载配置, 若正在进行检测, 将重启检测
        - "status": 获取当前黑烟检测运行状态 返回0或1
        - "rtmp start": 开始推送rtmp流指令
        - "rtmp stop": 停止推送rtmp流指令
        - "rtmp status": 获取rtmp推送状态 返回0或1
        '''
        try:
            host, port = address.split(":")
            port = int(port)
        except:
            self.__log.error("[command]Socket地址不合法, 将停止指令服务", exc_info=True)
            return

        import socket

        def readline(c: socket.socket):
            buff = []
            last_line = ""
            while True:
                try:
                    data = c.recv(512).decode()
                    self.__log.debug("recv data: {}".format(data))
                    if data == "":
                        return ""
                except socket.timeout:
                    continue

                last_line += data
                if "\n" in last_line:
                    lines = last_line.split("\n")
                    buff += lines[:-1]
                    last_line = lines[-1]

                while buff:
                    yield buff.pop(0)

        client = None
        lines = None
        fail_max = 3
        fail = 0
        while True:
            # 连接服务器
            if client is None:
                try:
                    client = socket.socket()
                    client.connect((host, port))
                    client.settimeout(1)
                    # 发送自身ID
                    client.send(str(self.__cfg.id).encode())
                    if start:
                        self.start(rtmp=rtmp, thread=True)
                    self.__log.info("[command]已连接到Socket服务器")
                    # 接收指令
                    lines = readline(client)
                    fail = 0
                except:
                    fail += 1
                    if fail > fail_max:
                        self.__log.critical("[command]Socket连接失败次数过多, 将退出进程")
                        break
                    self.__log.error("[command]Socket连接失败, 将在5秒后尝试重新连接", exc_info=True)
                    client.close()
                    client = None
                    lines = None
                    sleep(5)
                    continue

            try:
                line = next(lines)
            except Exception as e:
                if isinstance(e, StopIteration):
                    self.__log.warning("[command]Socket已被关闭, 将重新进行连接")
                else:
                    self.__log.warning("[command]接收命令时发生错误, 将重新连接服务器", exc_info=True)
                client.close()
                client = None
                continue
            except:
                self.__log.warning("[command]接收到退出信号", exc_info=True)
                break

            self.__log.debug("[command]接收到指令: `{}`".format(line))
            # 执行
            cmd = COMMAND.getCommand(line)
            try:
                if cmd == COMMAND.SHUTDOWN:
                    break
                else:
                    self.__excCommand(cmd, client)
            except (SystemExit, KeyboardInterrupt):
                self.__log.warning("[command]接收到退出信号", exc_info=True)
                break
            except:
                self.__log.warning("[command]执行指令时发生错误", exc_info=True)

            self.__log.debug("[command]指令执行完成")

        if isinstance(client, socket.socket):
            client.close()
        self.stop()
        self.__log.info("进程已退出")


if __name__ == '__main__':
    from fire import Fire
    Fire(SmokeProcess)
