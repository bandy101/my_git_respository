from datetime import datetime
from typing import Callable
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from time import sleep

from ProcessManager.Log import Log


class TimerTask:

    """ 定时任务类 """

    def __init__(self, name: str, func: Callable, *args, **kwargs):
        """ 定时任务
        - name str: 任务名称
        - func callable: 任务回调
        - *args: 回调位置参数
        - **kwargs: 回调键值参数
        """
        self.name = name
        self._func = func
        self._args = args
        self._kwargs = kwargs

    def run(self):
        """ 执行回调函数 """
        self._func(*self._args, **self._kwargs)

    def __eq__(self, value):
        if isinstance(value, TimerTask):
            return self.name == value.name
        return False

    def __hash__(self):
        return hash("{}_{}".format(__name__, self.name))


class TimerServer(Log):

    """ 定时作业服务 """

    def __init__(self, log_name: str):
        """ 定时作业服务
        - log_name str: 日志名称
        """
        super().__init__("[TIMER]", log_name)
        self._event_dict = defaultdict(set)
        self.__stop = True

    def startServer(self):
        """ 启动服务 """
        if self.__stop:
            self.__stop = False
            Thread(target=self._serverThread).start()

    def stopServer(self):
        """ 停止服务 """
        self.__stop = True

    def add(self, interval: int, task: TimerTask):
        """ 添加一个定时任务列表中, 相同名称的任务在只能存在一个
        - interval int: 作业执行时间间隔, 单位为秒
        - task Task: 要执行的任务
        """
        for s in self._event_dict.values():
            if task in s:
                self._warning("[{}]添加失败, 已存在相同名称的任务".format(task.name))
                break
        else:
            self._event_dict[interval].add(task)
            self._info("[{}]已加入定时任务列表".format(task.name))

    def remove(self, task: str or TimerTask):
        """ 移除指定名称的定时任务
        - name str: 定时任务的名称
        """
        if not isinstance(task, TimerTask):
            task = TimerTask(task, None)
        for s in self._event_dict.values():
            if task in s:
                s.remove(task)
        self._info("[{}]已从定时任务列表中移除".format(task.name))

    def _eval(self, task: TimerTask):
        """ 执行指定函数 """
        try:
            task.run()
            self._debug("[{}]执行完成".format(task.name))
        except:
            self._warning("[{}]执行失败".format(task.name), exc_info=True)

    def _serverThread(self):
        self._info("定时服务已启动")

        # 创建线程池
        pool = ThreadPoolExecutor(10)

        while self.__stop is False:
            # 计算当前秒数
            curr_time = datetime.now()
            curr_time = curr_time.hour * 60 * 60 + curr_time.minute * 60 + curr_time.second

            try:
                # 遍历任务时间
                for interval, task_list in self._event_dict.items():
                    if curr_time % interval == 0:
                        # 将定时任务加入线程池
                        for task in task_list:
                            self._debug("[{}]已加入执行队列".format(task.name))
                            pool.submit(self._eval, task)
            except:
                self._warning("执行定时任务时发生错误", exc_info=True)

            if self.__stop is False:
                # 等待下一秒开始
                sleep(1 - datetime.now().microsecond / 1000000)
        self._info("定时服务正在停止, 正在等待所有执行任务完成...")
        pool.shutdown()
        self._info("定时服务已停止")
