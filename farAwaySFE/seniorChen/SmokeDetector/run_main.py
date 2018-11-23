# coding: utf-8
import os
from os import path
import sys
import logging
from datetime import datetime
from time import sleep
from subprocess import Popen, PIPE, STDOUT
import json
from threading import Thread
from queue import Queue
from tempfile import NamedTemporaryFile

import cv2
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from ui.ui_main import Ui_MainWindow
from ui.BorderSetting import getBorder


class MainWindow(QMainWindow, Ui_MainWindow):
    process_data = None                     # 保存正在运行的子进程对象 key: value = sid: Process
    cdir = "./configure/"                   # 配置文件保存的目录
    timer = None                            # 定时器 间隔1s 检查自动开始、自动停止、进程状态、日志输出
    timer_clear = None                      # 定时器 间隔1h 清空界面日志
    signal_process = pyqtSignal(str, int)   # 控制进程的自定义事件
    signal_set_stop_msg = pyqtSignal(int)   # 停止指定进程后显示停止结果
    queue_log = None                        # 用于保存日志的队列

    @property
    def coding(self):
        ''' 返回字符集编码 '''
        return 'gbk' if sys.platform == 'win32' else 'utf-8'

    @property
    def pyName(self):
        ''' 返回Python执行程序名称 '''
        return 'python' if sys.platform == 'win32' else 'python3.6'

    # 构造函数、析构函数 ---------------------------------------------------

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # 变量初始化
        self.process_data = dict()
        self.queue_log = Queue()
        self.signal_process.connect(self.on_process)
        self.signal_set_stop_msg.connect(self.on_set_stop_msg)

        if not path.isdir(self.cdir):
            os.makedirs(self.cdir)

        # 定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.on_timer_timeout)
        self.timer.start(1000)

        # 清除日志定时器
        self.timer_clear = QTimer(self)
        self.timer_clear.timeout.connect(self.on_timer_hour_timeout)
        self.timer_clear.start(1000 * 60 * 60)

        # 状态条 总配置数
        label = QLabel(self)
        label.setText("总配置数")
        self.label_count = QLabel(self)
        self.label_count.setText("0")
        self.statusBar.addWidget(label)
        self.statusBar.addWidget(self.label_count)

        # 状态条 运行数
        label = QLabel(self)
        label.setText("正在运行")
        self.label_running = QLabel(self)
        self.label_running.setText("0")
        self.statusBar.addWidget(label)
        self.statusBar.addWidget(self.label_running)

        # 配置项列表
        self.cfg_model = QStandardItemModel(self.tv_cfg)
        self.cfg_model.setColumnCount(3)
        self.tv_cfg.setModel(self.cfg_model)
        self.tv_cfg.selectionModel().currentRowChanged.connect(self.on_cfg_row_changed)
        self.loadCfg()

    # 子进程控制 --------------------------------------------------------------------------------------

    def stopSubProcess(self, row):
        ''' 发送停止指令并等待进程结束 '''
        row, item, cfg = self.getRowData(row)
        if row == -1:
            return
        id = cfg["id"]
        if id not in self.process_data:
            return
        self.cfg_model.item(row, 1).setText("正在停止")

        # 停止进程
        def waitStop():
            if id in self.process_data:
                try:
                    process = self.process_data[id]
                    self.__stopProcess(process)
                    while process.poll() is None:
                        sleep(0.01)
                except:
                    pass
                finally:
                    self.signal_set_stop_msg.emit(row)
                    try:
                        self.process_data.pop(id)
                    except:
                        pass

        thread = QThread(self)
        thread.run = waitStop
        thread.start()

    def __stopProcess(self, process):
        if process.poll() is None and process.stdin.writable():
            process.stdin.write("stop\n".encode(self.coding))
            process.stdin.flush()

    def checkSubProcess(self, row):
        ''' 获取进程输出 检查进程是否已结束 '''
        color = {
            "INFO": "black",
            "WARNING": "gray",
            "ERROR": "orange",
            "CRITICAL": "red"
        }
        row, item, cfg = self.getRowData(row)
        if row == -1:
            return
        id = cfg["id"]
        process = self.process_data[id]
        out = process.stdout

        # 读取子进程日志
        while True:
            line = out.readline().decode(self.coding).strip()
            if (id not in self.process_data) and (not line):
                self.__stopProcess(process)
                break
            if not line:
                break
            elif line.count("[") >= 3:
                level = line.split("]")[2][1:]
                self.queue_log.put((line, color[level]))

        # 停止子进程
        self.signal_process.emit('stop', row)

    def startSubProcess(self, row):
        ''' 启动检测子进程 '''
        row, item, cfg = self.getRowData(row)
        if row == -1:
            return
        id = cfg["id"]

        if id in self.process_data and type(self.process_data[id]) is Popen:
            print(f"{id} 已运行")
            return

        cmd = f"{self.pyName} run_process.pyc {path.join(self.cdir, id)}.json True"
        process = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT, shell=True)

        if process.pid:
            self.cfg_model.item(row, 1).setText("正在运行")
            self.cfg_model.item(row, 2).setText(str(process.pid))
            self.process_data[id] = process
            # 启动进程检查
            self.signal_process.emit("check", row)
        else:
            QMessageBox.information(self, '提示:', f'{id} 启动失败！')

    # 文本框日志 -------------------------------------------------------------------------------

    def log(self, message, color="black"):
        ''' 使用指定颜色将消息输出到日志文本框 '''
        self.text_log.append(f"<font color='{color}'>{message}</font>")

    # 加载、保存配置文件 ---------------------------------------------------------------------

    def loadCfg(self):
        ''' 从配置文件夹加载配置列表 '''
        self.cfg_model.clear()
        self.cfg_model.setHorizontalHeaderLabels(["名称", "状态", "进程ID"])
        fl = os.listdir(self.cdir)
        fl.sort()
        for f in fl:
            if not f.endswith(".json"):
                continue
            try:
                with open(path.join(self.cdir, f), encoding='utf-8') as fp:
                    cfg = json.load(fp)
                    if cfg["id"] == path.splitext(f)[0]:
                        self.new_row(cfg)
            except Exception as e:
                print(e)
        self.label_count.setText(str(self.cfg_model.rowCount()))
        try:
            self.tv_cfg.setCurrentIndex(0)
        except:
            pass

    def saveCfg(self, update=False):
        ''' 将配置保存到文件夹 '''
        # 转换配置到dict
        cfg = {
            "id": self.edit_id.text(),
            "name": self.edit_name.text(),
            "upload_func": self.edit_func.text() or None,
            "video_source": self.edit_video.text(),
            "Ringelmann": self.spin_ringelmann.value(),
            "save_path": self.edit_save.text()
        }
        # 车流量统计
        if self.edit_statistics_func.text():
            cfg['statistics'] = self.edit_statistics_func.text()
            cfg['statis_interval'] = self.edit_staits_interval.text()
        # 自动任务
        for k, c, t in [("start_time", self.cb_start, self.tedit_start), ("stop_time", self.cb_stop, self.tedit_stop)]:
            if c.isChecked():
                cfg[k] = t.time().toString("H:m")

        cfg['border'] = self.btn_border.property('border')

        # 验证
        fn = path.join(self.cdir, f"{cfg['id']}.json")
        if update is False and path.exists(fn):
            QMessageBox.critical(self, "错误：", "已存在相同ID的配置文件，保存失败！")
            return

        # 保存
        try:
            with open(fn, "w", encoding='utf-8') as fp:
                json.dump(cfg, fp, ensure_ascii=False)
        except:
            QMessageBox.critical(self, "错误：", "保存失败！")
        else:
            QMessageBox.information(self, "提示：", "保存成功！\n提示：正在运行的程序按原配置文件运行，重启后才按新配置文件运行。")
            return cfg

    # 行数据相关 -----------------------------------------------------------

    def new_row(self, cfg):
        ''' 根据配置创建新的一行列表 '''
        name = QStandardItem(cfg["name"])
        name.setData(cfg)
        self.cfg_model.appendRow([
            name,
            QStandardItem("未运行"),
            QStandardItem("")
        ])

    def getRowData(self, row=None):
        ''' 返回配置项的行索引、行第一列对象、行数据 '''
        try:
            row = row if row is not None else self.tv_cfg.currentIndex().row()
            item = self.cfg_model.item(row)
            return row, item, item.data() if item else None
        except:
            return -1, None, None

    # 事件 -----------------------------------------------------------------

    @pyqtSlot(int)
    def on_set_stop_msg(self, row):
        self.cfg_model.item(row, 1).setText("已停止")
        self.cfg_model.item(row, 2).setText("")

    @pyqtSlot(str, int)
    def on_process(self, state, row):
        ''' 进程状态控制 '''
        if state == "start":
            self.startSubProcess(row)
        elif state == "check":
            Thread(target=self.checkSubProcess, args=(row, )).start()
        elif state == "stop":
            self.stopSubProcess(row)

    @pyqtSlot(QModelIndex, QModelIndex)
    def on_cfg_row_changed(self, new_row, old_row):
        ''' 配置列表当前选中项被修改 '''
        if new_row.row() < 0:
            return
        cfg = self.cfg_model.item(new_row.row()).data()

        # 站点ID 站点名称 上传函数
        self.edit_id.setText(cfg["id"])
        self.edit_name.setText(cfg["name"])
        self.edit_func.setText(cfg["upload_func"] or "")

        # 自动开始时间
        if cfg.get("start_time"):
            self.cb_start.setChecked(True)
            self.tedit_start.setTime(QTime.fromString(cfg["start_time"], "H:m"))
        else:
            self.cb_start.setChecked(False)

        # 自动停止时间
        if cfg.get("stop_time"):
            self.cb_stop.setChecked(True)
            self.tedit_stop.setTime(QTime.fromString(cfg["stop_time"], "H:m"))
        else:
            self.cb_stop.setChecked(False)

        # 视频源 林格曼阈值
        self.edit_video.setText(cfg["video_source"])
        self.spin_ringelmann.setValue(cfg["Ringelmann"])

        # 车道数据
        self.btn_border.setProperty('border', cfg.get('border'))

        # 车流量统计
        if 'statistics' in cfg:
            self.edit_statistics_func.setText(cfg['statistics'])
        else:
            self.edit_statistics_func.setText('')
        if 'statis_interval' in cfg:
            self.edit_staits_interval.setText(cfg['statis_interval'])
        else:
            self.edit_staits_interval.setText('')

        # 保存目录
        self.edit_save.setText(cfg["save_path"])

    @pyqtSlot()
    def on_btn_border_clicked(self):
        # 打开视频
        video_source = self.edit_video.text()
        default_border = self.btn_border.property('border')

        border = getBorder(self, video_source, default_border)
        if border:
            self.btn_border.setProperty('border', border)

    @pyqtSlot()
    def on_btn_add_clicked(self):
        ''' 添加配置按钮被点击 '''
        cfg = self.saveCfg()
        if not cfg:
            return
        self.new_row(cfg)
        self.tv_cfg.selectRow(self.cfg_model.rowCount() - 1)
        self.label_count.setText(str(self.cfg_model.rowCount()))

    @pyqtSlot()
    def on_btn_update_clicked(self):
        ''' 更新配置按钮被点击 '''
        row, item, cfg = self.getRowData()
        if row == -1:
            if QMessageBox.question(self, '询问:', '未选中任何配置项, 是否新增配置?') == QMessageBox.Yes:
                self.on_btn_add_clicked()
            return

        if cfg["id"] != self.edit_id.text():
            if QMessageBox.question(self, "询问:", "设备编号已被修改, 是否恢复设备编号并保存?") == QMessageBox.Yes:
                self.edit_id.setText(cfg["id"])
            else:
                return

        cfg = self.saveCfg(True)
        if cfg:
            item.setData(cfg)
            self.edit_name.setText(cfg['name'])

    @pyqtSlot()
    def on_btn_delete_clicked(self):
        ''' 删除设置按钮被点击 '''
        row, item, cfg = self.getRowData()
        if row == -1:
            return

        id = cfg["id"]
        if id in self.process_data:
            QMessageBox.information(self, '提示:', '请先停止运行该配置。')
            return

        if QMessageBox.question(self, "询问：", "确认删除该配置？") == QMessageBox.Yes:
            f = path.join(self.cdir, f"{id}.json")
            if path.exists(f):
                os.remove(f)

            self.cfg_model.removeRow(row)
            self.label_count.setText(str(self.cfg_model.rowCount()))

    @pyqtSlot()
    def on_btn_video_clicked(self):
        ''' 选择视频源按钮被点击 '''
        fn = QFileDialog.getOpenFileName(self, "选择视频文件", filter="MP4文件(*.mp4)\n所有文件(*.*)")[0]
        if fn:
            self.edit_video.setText(fn)

    @pyqtSlot()
    def on_btn_save_clicked(self):
        ''' 选择保存目录按钮被点击 '''
        d = QFileDialog.getExistingDirectory(self, "选择保存文件夹")
        if d:
            self.edit_save.setText(d)

    @pyqtSlot()
    def on_btn_start_clicked(self):
        ''' 开始按钮被点击 '''
        self.signal_process.emit("start", self.tv_cfg.currentIndex().row())

    @pyqtSlot()
    def on_btn_stop_clicked(self):
        ''' 停止按钮被点击 '''
        self.signal_process.emit("stop", self.tv_cfg.currentIndex().row())

    @pyqtSlot()
    def on_btn_start_all_clicked(self):
        ''' 开始所有按钮被点击 '''
        for i in range(self.cfg_model.rowCount()):
            self.signal_process.emit("start", i)

    @pyqtSlot()
    def on_btn_stop_all_clicked(self):
        ''' 停止所有按钮被点击 '''
        for i in range(self.cfg_model.rowCount()):
            self.signal_process.emit("stop", i)

    @pyqtSlot()
    def on_timer_hour_timeout(self):
        self.text_log.setText('')

    @pyqtSlot()
    def on_timer_timeout(self):
        ''' 1秒定时器事件 '''
        for i in range(self.cfg_model.rowCount()):
            row, item, cfg = self.getRowData(i)
            id = cfg["id"]

            start_time = QTime.fromString(cfg.get('start_time', '00:00'), "H:m")
            stop_time = QTime.fromString(cfg.get('stop_time', '23:59'), "H:m")
            if id not in self.process_data:
                # 自动开始检测
                if cfg.get("start_time"):
                    if start_time <= QTime.currentTime() < stop_time:
                        self.signal_process.emit("start", i)

            # 自动停止检测
            if cfg.get("stop_time") and id in self.process_data:
                if QTime.currentTime() >= stop_time:
                    self.signal_process.emit("stop", i)

        # 输出日志
        while not self.queue_log.empty():
            self.log(*self.queue_log.get())

        self.label_running.setText(str(len(self.process_data.keys())))

    def closeEvent(self, event: QCloseEvent):
        # 停止定时器
        self.timer.stop()
        self.timer_clear.stop()

        # 停止子进程
        for i in range(self.cfg_model.rowCount()):
            self.stopSubProcess(i)

        # 等待所有子进程停止
        if self.process_data:
            event.ignore()

            dlg = QMessageBox(self)
            dlg.setWindowTitle('提示:')
            dlg.setText('请稍等, 正在等待子进程关闭...')
            dlg.setIcon(QMessageBox.Information)
            dlg.show()

            t = QThread()

            def waitStop(thread=t):
                while self.process_data:
                    sleep(0.1)
                dlg.close()
                QApplication.quit()

            t.run = waitStop
            t.start()
        else:
            event.accept()


def main():
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    app.exec_()


if __name__ == "__main__":
    main()
