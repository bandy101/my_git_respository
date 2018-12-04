"""
SOCKET交互指令
"""

from enum import Enum


class COMMAND(Enum):
    # 停止检测并退出进程
    SHUTDOWN = b"shutdown\n"

    # 启动检测
    START = b"start\n"

    # 停止检测
    STOP = b"stop\n"

    # 重启检测
    RESTART = b"restart\n"

    # 重载配置并重启检测
    RELOAD = b"reload\n"

    # 获取当前检测状态
    STATUS = b"status\n"

    # 启动RTMP推流
    RTMP_START = b"rtmp start\n"

    # 停止RTMP推流
    RTMP_STOP = b"rtmp stop\n"

    # 获取当前RTMP状态
    RTMP_STATUS = b"rtmp status\n"

    @staticmethod
    def getCommand(cmd: str):
        """ 通过文本指定获取对应指令 如: 输入"start"会返回COMMAND.START
        - cmd str: 指令文本
        - return COMMAND or None: 指令存在则返回输入指令, 否则返回None
        """
        cmd = (cmd + "\n").encode()
        for i in COMMAND:
            if i.value == cmd:
                return i
        else:
            return None
