"""
Socket服务
处理来自`run_process`的socket连接
"""
import socket
from typing import Dict, Tuple
from threading import Thread, Lock
from time import sleep

from common import COMMAND
from ProcessManager.Log import Log


class SocketServer(Log):

    server: socket.socket = None
    client_dict: Dict[str, socket.socket] = None

    def __init__(self, log_name: str):
        """ Socket服务
        - log_name str: 使用的log的名称
        """
        super().__init__("[SOCKET]", log_name)
        self.__stop = True
        self.client_dict = dict()
        self._lock = Lock()

    def sendCommand(self, client_id: str, cmd: COMMAND) -> Tuple[bool, str or None]:
        """ 发送指定指令
        - client_id str: 客户端ID
        - cmd COMMAND: 要发送的指令
        """
        self._lock.acquire()
        try:
            send = self._send(client_id, cmd.value)
            if send and cmd in [
                COMMAND.STATUS,
                COMMAND.RTMP_STATUS
            ]:
                data = self._recv(client_id, 1)
                if isinstance(data, bytes):
                    data = data.decode()
                    return True, data
                else:
                    return False, None
            return send, None
        finally:
            self._lock.release()
        return False, None

    def _send(self, client_id: str, data: bytes) -> bool:
        """ 发送指定数据到客户端
        - client_id str: 客户端ID
        - data bytes: 要发送的数据
        - return bool: 返回发送是否成功
        """
        if client_id not in self.client_dict:
            self._debug("[{}]{}发送失败, 该客户端未连接到服务器".format(client_id, data))
            return False
        client: socket.socket = self.client_dict[client_id]

        try:
            client.send(data)
            self._debug("[{}]{}发送成功".format(client_id, data))
            return True
        except socket.timeout:
            self._warning("[{}]{}发送超时".format(client_id, data))
            return False
        except:
            self._warning("[{}]{}发送失败, 将断开连接".format(client_id, data), exc_info=True)
            self.closeClient(client_id)
            return False

    def _recv(self, client_id: str, buffsize: int=255) -> bytes or None:
        """ 从指定客户端接收数据
        - client_id str: 客户端ID
        - buffsize int[255]: 缓冲区大小, 最多从客户端接收缓冲区大小的数据
        - return bytes or None: 读取成功返回已读取到的数据, 失败返回None
        """
        if client_id not in self.client_dict:
            self._warning("[{}]数据接收失败, 该客户端未连接到服务器".format(client_id))
            return None
        client: socket.socket = self.client_dict[client_id]

        try:
            data = client.recv(buffsize)

            if len(data) == 0:
                self._warning("[{}]数据接收失败, 客服端已断开连接".format(client_id))
                self.closeClient(client_id)
                return None
            self._debug("[{}]接收到数据：{}".format(client_id, data))
            return data
        except socket.timeout:
            self._warning("[{}]数据接收超时, 将断开连接".format(client_id))
            self.closeClient(client_id)
            return None
        except:
            self._warning("[{}]数据接收失败, 将断开连接".format(client_id), exc_info=True)
            self.closeClient(client_id)
            return None

    def closeClient(self, client_id: str):
        """ 关闭与指定客户端的连接 """
        if client_id in self.client_dict:
            self.client_dict[client_id].close()
            self.client_dict.pop(client_id)
            self._info("[{}]连接已断开".format(client_id))

    def startServer(self, port: int) -> bool:
        """ 创建并启动Socket服务
        - port int: 服务绑定的端口号
        - return bool: 返回是否启动成功
        """
        if self.__stop is False:
            self._warning("服务正在运行, 跳过本次启动服务")
            return True

        self.__stop = False
        self.server = socket.socket()
        self.server.settimeout(1)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            self.server.bind(("0.0.0.0", port))
            self.server.listen()
            self._info("服务已启动")
            Thread(target=self._acceptThread).start()
            return True
        except:
            self._error("服务启动失败", exc_info=True)
            self.stopServer()
            return False

    def stopServer(self):
        """ 停止Socket服务 
        - cmd COMMAND[COMMAND.SHUTDOWN]: 服务停止前发送给当前已连接客户端的指令
        """
        if self.__stop is False:
            self.__stop = True

            for cid in self.client_dict.keys():
                self.closeClient(cid)
            self._info("已断开所以与客户端的连接")

            if isinstance(self.server, socket.socket):
                self.server.close()
                self.server = None
                self._info("已停止Socket服务")

    def __del__(self):
        if self.__stop is False:
            self.stopServer()

    def _acceptThread(self):
        self._info("开始等待客户端连接")
        while self.__stop is False:
            try:
                client, addr = self.server.accept()
                client.settimeout(3)
                try:
                    sid = client.recv(255).decode().strip()
                    self._info("[{}]连接到服务器, 地址信息为: {}".format(sid, addr))
                    client.settimeout(None)
                except:
                    self._warning("{}连接到服务器, 读取客户端ID失败, 已断开连接")
                    client.close()

                if sid in self.client_dict:
                    self.sendCommand(sid, COMMAND.SHUTDOWN)
                    self.client_dict[sid].close()
                    self._warning("[{}]旧客户端仍在连接, 已强制断开".format(sid))
                self.client_dict[sid] = client

            except socket.timeout:
                pass
            except:
                self._warning("接受客户端连接时发生错误", exc_info=True)
        self._info("停止等待客户端连接")
