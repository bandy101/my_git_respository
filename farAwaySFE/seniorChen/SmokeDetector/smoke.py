# coding: utf-8
import sys
import os
from os import path
from time import sleep
from threading import Thread
import threading
from queue import Queue
from datetime import datetime
import math
import time
import copy
import shutil
import json

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import cv2

import ui
from SFE.SmokeDetector import SmokeDetector
from SFE.Tools import *

title_list = ['胜霏尔汽车黑烟监测系统', '安车黑烟车视频遥感监控系统']
ui_model = ['ui_sfe_smoke', 'ui_ac_smoke']
select = 0
title = title_list[select]
ui_smoke = getattr(ui, ui_model[select])  # 获取界面

upload_flag = False
if upload_flag:
    import upload
    upload.initToken()

save_path = "save"
sid = "测试点1"


if not path.exists(save_path):
    os.makedirs(save_path)


def saveSmoke(savepath, info):
    # 创建保存目录
    if not path.exists(savepath):
        try:
            os.makedirs(savepath)
        except:
            pass

    files = []

    # 保存图片
    for i in range(len(info["imgs"])):
        p = path.join(savepath, "{}.jpg".format(i))
        files.append(p)
        cv2.imwrite(p, info["imgs"][i])
    # 保存信息
    with open(path.join(savepath, "info.txt"), mode="w", encoding='utf-8') as fp:
        lines = [
            f"检测时间:{info['check_time']}",
            f"检测编号:{info['id']}",
            f"点位编号:{sid}",
            f"车道号:{info['lane_no']}",
            f"车牌:{info['plate']}",
            f"车牌颜色:{info['plate_color']}",
            f"林格曼黑度:{info['Ringelmann']}",
            f"车型:{None}",
            f"车身颜色:{None}"
        ]
        for line in lines:
            print(line, file=fp, flush=True)

    # 保存视频
    p = path.join(savepath, "video.mp4")
    files.append(p)
    writer = cv2.VideoWriter(p, cv2.VideoWriter_fourcc(*"H264"), info["fps"], info["size"])
    if writer.isOpened() is False:
        return
    for img in info["video"]:
        writer.write(img)
    writer.release()

    # 上传记录
    if upload_flag:
        data = {
            "stNumber": "1",
            "stName": sid,
            "lineNo": info["lane_no"],
            "ringelmanEmittance": info["Ringelmann"],
            "plate": info["plate"],
            "plateColor": info["plate_color"],
            "vehicleType": "0",
            "vehicleOwnerShip": "1",
            "greenYellowCar": "0",
            "throughTime": info["id"][:13],
            "remarks": ""
        }
        data["plate"] = data["plate"] if data["plate"] else ""
        data["plateColor"] = data["plateColor"] if data["plateColor"] else ""
        print(upload.upload(data, files))


class SmokeDialog(QDialog, ui_smoke.Ui_Dialog):

    run_stop_signal = pyqtSignal(bool)      # 控制检测过程
    save_signal = pyqtSignal(dict, bool)    # 触发保存
    __main_size = (800, 600)                # 主显示窗口大小
    __child_size = (320, 240)               # 次显示窗口大小
    __play_stop = True                      # 控制回放状态
    __play_is_stop = True                   # 回放当前状态
    __headLabels = ["检测时间", "车牌", "林格曼"]
    __history = ["检测时间", "记录编号", "上传状态"]
    __start_timer = None                    # 自动开始定时器
    __stop_timer = None                     # 自动停止定时器
    __save_path = save_path                 # 保存目录

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        # self.setFixedSize(self.size())                              # 设置窗口固定大小
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)   # 关闭帮助按钮
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)       # 显示最小化按钮
        self.setWindowTitle(title)

        # 设置多选框状态    
        self.checkBoxCar.setChecked(True)
        self.checkBoxSmoke.setChecked(True)
        self.checkBoxSave.setChecked(True)
        self.checkBoxSave.setEnabled(False)

        # 连接自定义消息
        self.run_stop_signal.connect(self.on_stop_changed)
        self.save_signal.connect(self.on_save)

        # 初始化检测结果表
        self.model = QStandardItemModel(self.tableView)
        self.model.setColumnCount(3)
        self.model.setHorizontalHeaderLabels(self.__headLabels) #设置的列表表头
        self.tableView.setModel(self.model)
        self.tableView.selectionModel().currentRowChanged.connect(self.on_row_changed)
        self.tableView.doubleClicked.connect(self.on_dclicked)

        # 初始化历史记录表
        self.model2 = QStandardItemModel(self.tableHistory)
        self.model2.setColumnCount(3)
        self.tableHistory.setModel(self.model2)
        self.tableHistory.selectionModel().currentRowChanged.connect(self.on_row_changed2)
        self.tableHistory.doubleClicked.connect(self.on_dclicked2)
        self.load_history()

        # 设置初始模式为视频模式
        self.radioVideo.toggle()
        self.on_radioVideo_toggled(True)

        # 设置保存目录
        if not path.exists(self.__save_path):
            os.makedirs(self.__save_path)
        self.editSave.setText(path.abspath(self.__save_path))
        self.editSave.setReadOnly(True)
        self.btnSave.clicked.connect(lambda i: QDesktopServices.openUrl(QUrl(self.__save_path)))

        # 设置林格曼初始阈值
        self.sliderLevel.setValue(1)

        self.stop = True

        self.border = None

    # 自动停止
    @pyqtSlot(bool)
    def on_checkBoxAutoStop_clicked(self, checked):
        if checked:
            self.__stop_timer = QTimer(self)
            self.__stop_timer.timeout.connect(self.on_timeout)
            self.__stop_timer.start(10000)
        else:
            self.__stop_timer.stop()
            self.__stop_timer = None

    # 自动开始
    @pyqtSlot(bool)
    def on_checkBoxAutoStart_clicked(self, checked):
        if checked:
            self.__start_timer = QTimer(self)
            self.__start_timer.timeout.connect(self.on_timeout)
            self.__start_timer.start(10000)
        else:
            self.__start_timer.stop()
            self.__start_timer = None

    # 自动任务执行
    def on_timeout(self):
        if self.__start_timer:
            if self.timeEditStart.time() <= QTime.currentTime():
                self.checkBoxAutoStart.clicked.emit(False)
                self.checkBoxAutoStart.setChecked(False)
                if self.btnStart.isEnabled():
                    self.btnStart.clicked.emit()
        if self.__stop_timer:
            if self.timeEditStop.time() <= QTime.currentTime():
                self.checkBoxAutoStop.clicked.emit(False)
                self.checkBoxAutoStop.setChecked(False)
                if self.btnStop.isEnabled():
                    self.btnStop.clicked.emit()

    # 加载历史记录
    def load_history(self):
        self.model2.clear()
        self.model2.setHorizontalHeaderLabels(self.__history)
        fl = os.listdir(self.__save_path)
        fl.sort(reverse=True)
        for d in fl:
            if path.isfile(path.join(self.__save_path, d)):
                continue
            with open(path.join(self.__save_path, d + "/info.txt"), encoding='utf-8') as f:
                lines = f.readlines()
                lines = [":".join(i.split(":")[1:])[:-1] for i in lines][:-2]
                keys = ["check_time", "id", "sid", "lane_no", "plate", "plate_color", "Ringelmann"]
                info = dict(zip(keys, lines))
                name = QStandardItem(info["check_time"])
                name.setData(info)
                self.model2.appendRow([
                    name,
                    QStandardItem(info["id"]),
                    QStandardItem("已上传")
                ])

    @property
    def stop(self):
        return self._stop

    @stop.setter
    def stop(self, value):
        self._stop = value

        group = [
            self.btnStart,
            self.checkBoxCar, self.checkBoxSmoke, self.checkBoxSave,
            self.sliderLevel,
            self.checkBoxAutoStart, self.timeEditStart,
            self.checkBoxAutoStop, self.timeEditStop,
            self.editSave, self.btnSave,
            self.radioVideo, self.radioStream,
            self.btnBorder,
        ]
        [i.setEnabled(value) for i in group]
        self.btnStop.setEnabled(not value)

    @pyqtSlot()
    def on_btnBorder_clicked(self):
        from ui.BorderSetting import getBorder

        if self.radioVideo.isChecked():
            video_source = self.editPath.text()
        else:
            video_source = '||'.join([
                self.editUser.text(),
                self.editPwd.text(),
                self.editIP.text(),
                self.editPort.text(),
                self.editChannel.text()
            ])

        border = getBorder(self, video_source, self.border)
        if border:
            self.border = border

    @pyqtSlot(bool)
    def on_radioVideo_toggled(self, model):
        ''' 模式切换 '''
        group1 = [self.editIP, self.editPort, self.editChannel, self.editUser, self.editPwd]
        group2 = [self.editPath, self.btnOpen] 
        #模式切换后禁用的控件
        [i.setEnabled(not model) for i in group1]
        [i.setEnabled(model) for i in group2]

    @pyqtSlot()
    def on_btnOpen_clicked(self):
        '''打开文件'''
        files = QFileDialog.getOpenFileName(self, "选择视频文件", "SFE/resource/video/smoke", "视频文件(*.mp4 *.avi)\n所有文件(*.*)")
        print('file:',files)
        if files[0]:
            self.editPath.setText(files[0])

    @pyqtSlot()
    def on_btnStart_clicked(self):
        '''开始检测'''
        # 检测是否有视频
        mode = self.radioVideo.isChecked()
        print('mode:',mode)
        if (mode):
            videoSource = self.editPath.text()
            if not videoSource:
                QMessageBox.warning(self, "警告", "请选择一个视频！")
                return
        else:
            items = [self.editUser.text(), self.editPwd.text(), self.editIP.text(), self.editPort.text(), self.editChannel.text()]
            for item in items:
                if not item:
                    QMessageBox.warning(self, "警告", "不允许出现空选项")
                    return
            videoSource = "||".join(items)

        self.model.clear()
        self.model.setHorizontalHeaderLabels(self.__headLabels)
        self.load_history()
        Thread(target=self.run, args=(videoSource, )).start()

    def on_stop_changed(self, stop):
        self.stop = stop

    @pyqtSlot(bool)
    def on_btnStop_clicked(self):
        '''停止检测'''
        self.run_stop_signal.emit(True)

    def on_save(self, info, playback=True):
        savepath = path.join(self.__save_path, info["id"])

        # 显示信息
        imgs = info["imgs"]
        level = info["Ringelmann"]
        plate = info["plate"]

        img1 = cv2pixmap(cv2.resize(imgs[0], self.__child_size))
        img2 = cv2pixmap(cv2.resize(imgs[1], self.__child_size))

        self.model.appendRow([
            QStandardItem(info["check_time"]),
            QStandardItem(plate),
            QStandardItem(level)
        ])
        rowIdx = self.model.rowCount() - 1
        item = self.model.item(rowIdx)
        data = copy.copy(info)
        data["imgs"] = [img1, img2]
        item.setData(data)
        self.tableView.selectRow(rowIdx)

        # 显示视频
        imgs = info["video"]
        fps = info["fps"]
        size = info["size"]

        if playback:
            self.__play_stop = True
            Thread(target=self.play, args=(imgs, fps)).start()

        Thread(target=saveSmoke, args=(savepath, info)).start()

    def on_row_changed(self, new, old):
        ''' 表格选中项被修改 '''
        data = self.model.item(new.row()).data()
        self.show_info(data)

    def on_row_changed2(self, new, old):
        ''' 表格选中项被修改 '''
        data = self.model2.item(new.row()).data()
        self.show_info(data)

    def show_info(self, info):
        if not info.get("imgs"):
            info["imgs"] = []
            for i in range(2):
                img = cv2.imread("{}/{}/{}.jpg".format(self.__save_path, info["id"], i))
                img = cv2.resize(img, self.__child_size)
                img = cv2pixmap(img)
                info["imgs"].append(img)

        self.labelImg1.setPixmap(info["imgs"][0])
        self.labelImg2.setPixmap(info["imgs"][1])
        self.labelPlate.setText(info["plate"])
        self.labelPColor.setText(info["plate_color"])
        self.labelRingelmann.setText(info["Ringelmann"])
        self.labelSId.setText(info["sid"])
        self.labelId.setText(info["id"])
        self.labelTime.setText(info["check_time"])
        self.labelLine.setText(info["lane_no"])

    def on_dclicked(self, idxModel):
        ''' 表项被双击 '''
        name = self.model.item(idxModel.row()).data()["id"]
        self.video_playback(name)

    def on_dclicked2(self, idxModel):
        ''' 表项被双击 '''
        name = self.model2.item(idxModel.row()).data()["id"]
        self.video_playback(name)

    def video_playback(self, name):
        video = "{}/{}/video.mp4".format(self.__save_path, name)
        if not path.exists(video):
            return
        self.__play_stop = True
        Thread(target=self.play, args=(None, None, video)).start()

    def play(self, imgs, fps, frompath=None):
        ''' 在窗口中回放视频 '''
        while not self.__play_is_stop:
            sleep(0.01)
        self.__play_is_stop = False
        self.__play_stop = False

        # 从文件回放
        if frompath:
            video = cv2.VideoCapture(frompath)
            fps = video.get(cv2.CAP_PROP_FPS)

        interval = fps / 1000

        while True:
            if frompath:
                retVal, frame = video.read()
            else:
                frame = imgs[0]
                del imgs[0]
                retVal = len(imgs) > 0

            if not retVal or self.__play_stop:
                break

            frame = cv2.resize(frame, self.__child_size)
            frame = cv2pixmap(frame)
            self.labelBack.setPixmap(frame)
            sleep(interval)

        self.__play_is_stop = True

    def __draw(self, image, lt, rb, color, label):
        ''' 在图片中用指定颜色画出矩形 并在左上角添加标签 '''
        label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, 1)[0]
        cv2.rectangle(image, lt, rb, color, 2)

        cv2.rectangle(image, lt, (lt[0] + label_size[0] + 3, lt[1] + label_size[1] + 5), color, -1)
        cv2.putText(image, label, (lt[0], lt[1] + label_size[1]), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 0), 1)

    def run(self, vpath):
        ''' 主运行过程 '''
        self.run_stop_signal.emit(False) #改变self.stop

        # 初始化变量
        show_car = self.checkBoxCar.isChecked()
        show_smoke = self.checkBoxSmoke.isChecked()
        save = self.checkBoxSave.isChecked()

        # 打开视频
        try:
            video = SmokeDetector(vpath, "resource", self.border)
        except Exception as e:
            print(e)
            QMessageBox.critical(self, "错误", "视频打开失败!")
            self.run_stop_signal.emit(True)
            return

        jump = 1 if vpath.count("||") == 4 else 0
        interval = 1 / video.fps
        # 遍历结果
        while True:
            #控制视频的播放与停止
            if self.stop:   
                break
            start_time = datetime.now()
            frame, tracks, save_list = video.nextFrame()

            if save and len(save_list) > 0:
                frames = video.getSaveFrames()
                for save_obj in save_list:
                    self.sendSave(save_obj, video.size, video.fps, frames, save_obj is save_list[-1])

            if frame is None:
                break

            for track in tracks:
                if show_smoke and track.smoke_count >= 3:
                    cv2.rectangle(frame, *track.last_result.car_rect, (0, 0, 255), 2)
                elif show_car:
                    cv2.rectangle(frame, *track.last_result.car_rect, (0, 255, 0), 2)

            # 在主窗口中显示
            img = cv2.resize(frame, self.__main_size)
            self.labelMain.setPixmap(cv2pixmap(img))
            # t = interval - (datetime.now() - start_time).microseconds / 1000000
            # t = t if t > 0 else 0
            # time.sleep(t)

            for i in range(jump):
                frame = video.nextFrame()[0]
                if frame is None:
                    break
                img = cv2.resize(frame, self.__main_size)
                self.labelMain.setPixmap(cv2pixmap(img))
                # time.sleep(interval)

        self.run_stop_signal.emit(True)

    def sendSave(self, save_obj, size, fps, frames, playback=True):
        if save_obj.Ringelmann < self.sliderLevel.value():
            return

        self.save_signal.emit({
            "sid": sid,
            "id": save_obj.id,
            "plate_color": save_obj.plate_color,
            "plate": save_obj.plate,
            "check_time": save_obj.check_time,
            "imgs": [save_obj.smoke_image, save_obj.plate_image],
            "lane_no": str(save_obj.lane_no),
            "Ringelmann": str(save_obj.Ringelmann),
            "fps": fps,
            "size": size,
            "video": frames
        }, playback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dlg = SmokeDialog()
    dlg.show()
    app.exec_()
