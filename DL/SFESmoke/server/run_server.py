import sys
import os
from os import path
from hashlib import md5
import tempfile
import typing
from threading import Timer
from datetime import datetime
from collections import Iterable
import re


import cherrypy
from cherrypy.lib import auth_digest
import cv2
import numpy as np
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import or_, desc

ROOT_PATH = path.dirname(path.abspath(__file__))
SERVER_CONFIG_PATH = path.join(ROOT_PATH, "server.json")
STATIC_PATH = path.join(ROOT_PATH, "web_static")
os.chdir(ROOT_PATH)

from DBModel import Record, Session, User
from SFE.Video import VideoReader
from SFE import getAuthID
from common import Config
from ProcessManager.MainServer import MainServer


# 定义管理对象
server = MainServer(SERVER_CONFIG_PATH)

# 定义常用错误
NOT_EXISTS_ID_ERROR = "指定ID不存在"
EXISTS_ID_ERROR = "已存在相同ID"
JSON_DATA_ERROR = "数据解析失败"
UNKNOWN_ERROR = "未知错误"
UNKNOWN_ACTION_ERROR = "未知的操作"
PLATE_COLOR = [
    "蓝",
    "黄",
    "白",
    "黑",
    "绿",
    "黄绿",
    "其他"
]
PLATE_TYPE = [
    "大型汽车",
    "小型汽车",
    "使馆汽车",
    "领馆汽车",
    "境外汽车",
    "外籍汽车",
    "农用运输车",
    "拖拉机",
    "挂车",
    "教练汽车",
    "警用汽车",
    "大型新能源汽车",
    "小型新能源汽车",
    "其他"
]
VEHICLE_COLOR = [
    "白",
    "银",
    "灰",
    "黑",
    "红",
    "深蓝",
    "蓝",
    "黄",
    "绿",
    "棕",
    "粉",
    "紫",
    "深灰",
    "青",
    "其他"
]
VEHICLE_TYPE = [
    "客车",
    "货车",
    "轿车",
    "面包车",
    "小货车",
    "行人",
    "二轮车",
    "三轮车",
    "SUV/MPV",
    "中型客车",
    "机动车",
    "非机动车",
    "小型轿车",
    "微型轿车",
    "皮卡车",
    "其他"
]



def hasConfigId(id):
    """ 判断是否存在指定id """
    return server.config_manager.exists(id)


def RequireLogin(permission_list: list):
    def wrapper(func):
        def wrap(*args, **kwargs):
            if cherrypy.session.get("permission", -1) in permission_list:
                return func(*args, **kwargs)
            else:
                return False, "访问权限不足"
        return wrap
    return wrapper


def ResultWrapper(func):
    """ 将返回结果打包为`dict` 同时将函数暴露出去 """
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def wrapper(*args, **kwargs):
        success, content = func(*args, **kwargs)
        return dict(success=success, content=content)
    return wrapper

@cherrypy.expose
class ListRoute:
    """ 记录下拉列表路由 """

    @ResultWrapper
    @RequireLogin([1, 2])
    def plate_color(self):
        """ 车牌颜色 """
        return True, PLATE_COLOR

    @ResultWrapper
    @RequireLogin([1, 2])
    def plate_type(self):
        """ 车牌类型 """
        return True, PLATE_TYPE
        
    @ResultWrapper
    @RequireLogin([1, 2])
    def vehicle_color(self):
        """ 车辆颜色 """
        return True, VEHICLE_COLOR

    @ResultWrapper
    @RequireLogin([1, 2])
    def vehicle_type(self):
        """ 车辆类型 """
        return True, VEHICLE_TYPE

@cherrypy.expose
@cherrypy.popargs("id")
class ConfigRoute:

    @ResultWrapper
    @RequireLogin([2])
    def GET(self, id=None, action=None):
        if isinstance(action, str) and len(action.strip()) == 0:
            action = None
        if id is None:
            return self.getAll(action)
        else:
            return self.getByID(id, action)

    def getByID(self, id, action):
        """ 返回ID详细配置 当查询字符串中的`action`为以下值是会进行特殊操作, 并返回操作结果
        - start: 启动该配置
        - stop: 停止该配置
        - restart: 重启该配置
        """
        if not hasConfigId(id):
            return False, NOT_EXISTS_ID_ERROR

        if action is None:
            return True, server.config_manager.getConfig(id).toDict()
        elif action == "start":
            if not server.start(id):
                return False, "启动失败, 详细原因请查看日志"
        elif action == "stop":
            server.stop(id)
        elif action == "restart":
            server.restart(id)
        elif action == "reload":
            server.reload(id)
        elif action == "shutdown":
            server.shutdown(id)
        else:
            return False, UNKNOWN_ACTION_ERROR
        return True, None

    def getAll(self, action):
        """ 返回配置列表 当查询字符串中的`action`为以下值是会进行特殊操作, 并返回操作结果
        - reload: 重新加载
        - startAll: 启动所有配置
        - stopAll: 停止所有配置
        """
        if action is None:
            return True, [i.toDict() for i in server.config_manager.getConfigList()]
        if action == "startAll":
            server.startAll()
        elif action == "stopAll":
            server.stopAll()
        elif action == "shutdownAll":
            server.shutdownAll()
        else:
            return False, UNKNOWN_ACTION_ERROR
        return True, None

    @cherrypy.tools.json_in()
    @ResultWrapper
    @RequireLogin([2])
    def POST(self, id=None):
        """ 创建新的配置 """
        cfg = Config.fromDict(cherrypy.request.json)
        if cfg.id != id:
            return False, "数据ID与路径ID不一致"
        err = cfg.check()
        if err:
            return False, err

        if server.config_manager.add(cfg):
            return True, None
        else:
            return False, "添加失败, 详细原因请查看日志"

    @cherrypy.tools.json_in()
    @ResultWrapper
    @RequireLogin([2])
    def PUT(self, id=None):
        """ 修改配置 """
        cfg = Config.fromDict(cherrypy.request.json)
        if cfg.id != id:
            return False, "数据ID与路径ID不一致"
        err = cfg.check()
        if err:
            return False, err

        if server.config_manager.update(cfg):
            return True, None
        else:
            return False, "修改失败, 详细原因请查看日志"

    @ResultWrapper
    @RequireLogin([2])
    def DELETE(self, id=None):
        """ 删除配置 """
        if hasConfigId(id):
            if server.status(id) != "未启动":
                server.shutdown(id)
            if server.config_manager.remove(id):
                return True, None
            else:
                return False, "删除失败, 详细原因请查看日志"
        else:
            return False, NOT_EXISTS_ID_ERROR


@cherrypy.expose
@cherrypy.popargs("sid", "rid")
class RecordRoute:

    @ResultWrapper
    @RequireLogin([0, 1, 2])
    def index(self, sid=None, rid=None):
        if sid is None:
            return True, server.config_manager.getConfigIdList()
        if not hasConfigId(sid):
            return False, NOT_EXISTS_ID_ERROR

        if rid is None:
            return self.getRecordInfo(sid, cherrypy.session["permission"])

        sess = Session()
        try:
            record: Record = sess.query(Record).filter(Record.st_id == sid, Record.id == rid).one()

            return True,  {
                "st_id": record.st_id,
                "st_name": record.st_name,
                "Ringelmann": record.Ringelmann,
                "plate": record.plate,
                "plate_color": record.plate_color,
                "plate_type": record.plate_type,
                "vehicle_type": record.car_type,
                "vehicle_color": record.car_color,
                "lane": record.car_lane,
                "timestamp": record.timestamp,
                "image1": "{}{}image1".format(cherrypy.request.script_name, cherrypy.request.path_info),
                "image2": "{}{}image2".format(cherrypy.request.script_name, cherrypy.request.path_info),
                "video": "{}{}video".format(cherrypy.request.script_name, cherrypy.request.path_info)
            }
        except NoResultFound:
            return False, "记录ID不存在"
        except:
            server._warning("查询记录时发生错误", exc_info=True)
            return False, "发生未知错误"
        finally:
            sess.close()

    @ResultWrapper
    @RequireLogin([1, 2])
    def status(self, sid, rid):
        if not hasConfigId(sid):
            return False, NOT_EXISTS_ID_ERROR

        sess = Session()
        try:
            record: Record = sess.query(Record).filter(Record.st_id == sid, Record.id == rid).one()
            record.status = True
            sess.commit()
            return True, None
        except NoResultFound:
            return False, "记录ID不存在"
        except:
            sess.rollback()
            server._warning("查询记录时发生错误", exc_info=True)
            return False, "未知错误"
        finally:
            sess.close()

    @cherrypy.tools.json_in()
    @ResultWrapper
    @RequireLogin([1, 2])
    def upload(self, sid, rid):
        if not hasConfigId(sid):
            return False, NOT_EXISTS_ID_ERROR

        # 数据验证
        data = cherrypy.request.json
        if not (isinstance(data.get("Ringelmann", None), int) and 0 <= data["Ringelmann"] <= 5):
            return False, "林格曼黑度值必须在0~5之间"
        if data.get("plate_color", None) not in PLATE_COLOR:
            return False, "车牌颜色取值错误"
        if data.get("plate_type", None) not in PLATE_TYPE:
            return False, "车牌类型取值错误"
        if data.get("vehicle_type", None) not in VEHICLE_TYPE:
            return False, "车辆类型取值错误"
        if data.get("vehicle_color", None) not in VEHICLE_COLOR:
            return False, "车辆颜色取值错误"
        if isinstance(data.get("lane", None), int) is False or data["lane"] < 1:
            return False, "车道号必须为大于0的整数"

        sess = Session()
        try:
            record: Record = sess.query(Record).filter(Record.st_id == sid, Record.id == rid).one()
            # 修改记录数据
            record.Ringelmann = data["Ringelmann"]
            record.plate_color = data["plate_color"]
            record.plate_type = data["plate_type"]
            record.car_type = data["vehicle_type"]
            record.car_color = data["vehicle_color"]
            record.car_lane = data["lane"]
            record.plate = data.get("plate", None) or "无车牌"

            # 修改确认状态、上传状态
            record.status = True
            if record.upload_status == "0":
                record.upload_status = "1"
            sess.commit()
            return True, None
        except NoResultFound:
            return False, "记录ID不存在"
        except:
            sess.rollback()
            server._warning("查询记录时发生错误", exc_info=True)
            return False, "未知错误"
        finally:
            sess.close()

    def getRecordInfo(self, sid, perm) -> typing.List[typing.Dict]:
        upload_status = {
            "0": "未上传",
            "1": "等待上传",
            "2": "已上传"
        }

        sess = Session()
        result = []

        try:
            query = sess.query(Record.id, Record.status, Record.upload_status, Record.timestamp).order_by(desc(Record.timestamp))
            if perm == 2:
                records = query.filter(Record.st_id == sid, or_(Record.status == False, Record.upload_status != "0")).all()
            elif perm == 1:
                records = query.filter(Record.st_id == sid, Record.status == False).all()
            else:
                records = query.filter(Record.st_id == sid, Record.upload_status != "0").all()

            for _id, status, upload, timestamp in records:
                result.append({
                    "id": _id,
                    "name": datetime.fromtimestamp(timestamp/1000).strftime("%Y/%m/%d %H:%M:%S.%f")[:-3],
                    "status": status,
                    "upload":  upload_status[upload]
                })
        except:
            server._warning("查询记录时发生错误", exc_info=True)
            return False, "发生未知错误"
        finally:
            sess.close()

        return True, result

    def getResource(self, sid, rid, name):
        if cherrypy.session.get("permission", -1) not in [0, 1, 2]:
            raise cherrypy.HTTPError(401, "权限不足")

        sess = Session()
        try:
            record = sess.query(Record).filter(Record.st_id == sid, Record.id == rid).one()

            if name == "image1":
                url, _type = record.img_plate_path, "image/jpeg"
            elif name == "image2":
                url, _type = record.img_smoke_path, "image/jpeg"
            elif name == "video":
                url, _type = record.video_path, "video/mp4"
            else:
                raise NoResultFound()
            if not path.isfile(url):
                raise NoResultFound()
            return cherrypy.lib.static.serve_file(url, _type)
        except NoResultFound:
            raise cherrypy.HTTPError(404)
        except:
            server._warning("查询记录时发生错误", exc_info=True)
            raise cherrypy.HTTPError(500, "发生未知错误")
        finally:
            sess.close()

    @cherrypy.expose
    def image1(self, sid, rid):
        return self.getResource(sid, rid, "image1")

    @cherrypy.expose
    def image2(self, sid, rid):
        return self.getResource(sid, rid, "image2")

    @cherrypy.expose
    def video(self, sid, rid):
        return self.getResource(sid, rid, "video")


class APIRoute():
    config = ConfigRoute()
    record = RecordRoute()
    list = ListRoute()

    @ResultWrapper
    @cherrypy.popargs("id")
    @RequireLogin([2])
    def rtmp(self, id=None, action=None):
        """ 返回配置当前的RTMP状态 当id不为`None`且查询字符串中的`action`为以下值是会进行特殊操作, 并返回操作结果
        - start: 启动RTMP推送
        - stop: 停止RTMP推送
        """
        if isinstance(action, str) and len(action.strip()) == 0:
            action = None

        if id is None:
            return True, {_id: server.RTMPStatus(_id) for _id in server.config_manager.getConfigIdList()}

        if not hasConfigId(id):
            return False, NOT_EXISTS_ID_ERROR

        if action is None:
            return True, server.RTMPStatus(id)
        elif action == "start":
            succ = server.startRTMP(id)
        elif action == "stop":
            succ = server.stopRTMP(id)
        else:
            return False, UNKNOWN_ACTION_ERROR

        if succ:
            return True, None
        else:
            return False, "操作失败, 详细原因请查看日志"

    @ResultWrapper
    @cherrypy.popargs("id")
    @RequireLogin([0, 1, 2])
    def status(self, id=None):
        """ 返回配置的当前运行状态 """
        if id is None:
            return True, [{
                    "id": cfg.id,
                    "name": cfg.name,
                    "status": server.status(cfg.id),
                    "rtmp": server.RTMPStatus(cfg.id),
                } for cfg in server.config_manager.getConfigList()]

        cfg = server.config_manager.getConfig(id)
        if cfg is not None:
            return True, {
                "id": id,
                "name": cfg.name,
                "status": server.status(id),
                "rtmp": server.RTMPStatus(id),
            }
        else:
            return False, NOT_EXISTS_ID_ERROR

    @ResultWrapper
    @cherrypy.popargs("id")
    @RequireLogin([2])
    def frame(self, id):
        """ 生成当前配置视频源的一帧图片 生成路径为`STATIC_PATH/frame/**.jpg` 图片会在30秒后自动删除 """
        if not hasConfigId(id):
            return False, NOT_EXISTS_ID_ERROR

        # 打开视频
        video = server.config_manager.getConfig(id).video_source
        vr = VideoReader()
        if isinstance(video, str) and video.count("||") == 5:
            user, pwd, ip, port, channel, open_type = video.split("||")
            port, channel = int(port), int(channel)
            if open_type == "0":
                vr.openStream(user, pwd, ip, port, channel)
            elif open_type == "1":
                vr.openHKRTSP(user, pwd, ip, port, channel)
        else:
            vr.openVideo(video)
        if vr.is_opened is False:
            return False, "视频打开失败"

        # 读取一帧
        ret, frame = vr.read()
        del vr
        if ret is False:
            return False, "视频帧读取失败"

        fd, img_path = tempfile.mkstemp(".jpg", dir=path.join(STATIC_PATH, "frame"))

        # 保存
        with open(fd, 'wb') as fp:
            ret, data = cv2.imencode('.jpg', frame)
            if ret is False:
                return False, "图片生成失败"
            fp.write(data)

        Timer(30, os.remove, args=(img_path, )).start()
        return True, "/frame/{}".format(path.basename(img_path))

    @ResultWrapper
    @RequireLogin([2])
    def autostart(self, action=None):
        """ 设置进程自动启动 """
        if action is None:
            return True, server.auto
        elif action == "start":
            server.auto = True
        elif action == "stop":
            server.auto = False
        else:
            return False, UNKNOWN_ACTION_ERROR
        return True, None

    @ResultWrapper
    @cherrypy.popargs("id")
    @RequireLogin([2])
    def log(self, id=None):
        if id is None:
            log_path = path.join(server.LOG_DIR, "log.log")
        else:
            if hasConfigId(id) is False:
                return False, NOT_EXISTS_ID_ERROR
            log_path = server.config_manager.getConfig(id).save_path
            log_path = path.join(log_path, "logs", "log.log")

        if path.isfile(log_path):
            try:
                with open(log_path, encoding="utf-8") as fp:
                    return True, [i.strip() for i in fp.readlines()]
            except:
                return False, "日志读取失败"
        else:
            return True, ""

    @cherrypy.tools.json_in()
    @ResultWrapper
    def login(self):
        data = cherrypy.request.json
        sess = Session()
        try:
            perm = sess.query(User.permission).filter(User.username == data.get("user", ""), User.password == data.get("password", "")).one()[0]
            cherrypy.session["permission"] = perm
            return True, perm
        except NoResultFound:
            return False, "用户名或密码错误"
        except:
            server._warning("用户登录时发生错误", exc_info=True)
            return False, "发生未知错误"
        finally:
            sess.close()

    @ResultWrapper
    def permission(self):
        return True, cherrypy.session.get("permission", -1)

    @ResultWrapper
    @RequireLogin([2])
    def rtmp_host(self):
        host = server.NET_RTMP_HOST
        if host is None:
            return False, "RTMP服务未配置外部访问端口, 请联系管理员"
        return True, host

    @ResultWrapper
    def server_name(self):
        return True, server.SERVER_NAME

    @cherrypy.expose
    def auth(self, auth_code=None):
        if cherrypy.session.get("permission", -1) != 2:
            raise cherrypy.HTTPError(401, "权限不足")
        elif auth_code is None:
            msg = ""
        else:
            server.auth_code = auth_code
            msg = "<script>alert('授权码更新成功，请重载配置使授权生效')</script>"

        return """
        <!DOCTYPE html>
        <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <meta http-equiv="X-UA-Compatible" content="ie=edge">
                <title>设置授权码</title>
            </head>
            <body>
                <p>机器码:{auth_id}</p>
                <form action="" method="post">
                    <label>授权码: <input type="text" name="auth_code" id="auth_code"></label>
                    <input type="submit" value="提交"> <input type="reset" value="重置">
                </form>
                <p style="color:red">服务器不对提交的授权码做任何验证，请谨慎修改</p>
                {msg}
            </body>
        </html>
        """.format(auth_id=getAuthID(), msg=msg)


def main(port=80, host="0.0.0.0", daemon=True):
    """ 黑烟检测管理Web服务
    - port int[80]: 端口号
    - host str["0.0.0.0"]: 绑定地址
    - daemon bool[True]: 在非Windows系统下是否已守护进程模式启动
    """
    # 全局配置
    log_dir = server.LOG_DIR
    os.makedirs(log_dir, exist_ok=True)
    global_conf = {
        # 设置绑定的地址、端口
        "server.socket_host": host,
        "server.socket_port": port,

        # 设置服务器日志文件
        "log.access_file": path.join(log_dir, "access_log.log"),
        "log.error_file": path.join(log_dir, "error_log.log"),
    }
    cherrypy.config.update(global_conf)

    # 静态文件配置
    root_conf = {
        "/": {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": STATIC_PATH,
            "tools.staticdir.index": "login.html",
        }
    }

    # API配置
    api_conf = {
        "/": {
            "tools.sessions.on": True,
        },
        "/config": {
            "request.dispatch": cherrypy.dispatch.MethodDispatcher(),
        }
    }

    # 挂载站点
    cherrypy.tree.mount(None, "", root_conf)
    cherrypy.tree.mount(APIRoute(), "/api", api_conf)

    # 将PID生成到文件中
    pid = cherrypy.process.plugins.PIDFile(cherrypy.engine, path.join(server.LOG_DIR, "pid"))
    pid.subscribe()

    # 注册消息事件
    cherrypy.engine.signals.subscribe()

    # 注册服务器停止回调
    cherrypy.engine.subscribe("stop", server.stopServer)

    if sys.platform != "win32" and daemon is True:
        daemon = cherrypy.process.plugins.Daemonizer(cherrypy.engine)
        daemon.subscribe()

    # 启动服务
    cherrypy.engine.start()

    # 设置自动启动检测进程
    server.startServer()
    server.auto = True

    cherrypy.engine.block()


if __name__ == "__main__":
    from fire import Fire
    Fire(main)
