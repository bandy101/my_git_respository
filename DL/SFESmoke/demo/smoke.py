import sys
import os
from os import path
from importlib import import_module
from datetime import datetime
from queue import Queue
from time import sleep
from threading import Thread
import traceback as tb
from subprocess import Popen, PIPE
import webbrowser

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import cv2

from SFE.SmokeDetector import SmokeDetector
from upload import RecordData
from upload import upload
from ui.BorderSetting import getBorder


# 设置UI界面
title_list = ['胜霏尔汽车黑烟监测系统', '安车黑烟车视频遥感监控系统']
ui_model = ['ui_sfe_smoke', 'ui_ac_smoke']
# 当当前目录存在 ac 文件时为安车 否则为胜霏尔
select = 1 if path.isfile("./ac") else 0
title = title_list[select]
ui_smoke = import_module("ui.{}".format(ui_model[select]))


def cv2pixmap(img):
    ''' 将 opencv 图片 转为 QPixmap '''
    size = img.shape[1::-1]
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    qi = QImage(rgb.tobytes(), *size, QImage.Format_RGB888)
    return QPixmap.fromImage(qi)


class SmokeDialog(QMainWindow, ui_smoke.Ui_MainWindow):

    signalVideoError = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # 初始化变量
        self.__station_id = "TEST01"
        self.__station_name = "测试点1"
        self.__headLabels = ["检测时间", "车牌", "林格曼"]
        self.__history = ["检测时间", "记录编号", "上传状态"]
        self.__start_timer = None                    # 自动开始定时器
        self.__stop_timer = None                     # 自动停止定时器
        self.__save_path = "./save"                 # 保存目录
        self.__border = None
        self.__playback_queue = Queue()
        self.__record_queue = Queue()
        self.__realplay_queue = Queue()
        self.realplay_stop = True

        self.signalVideoError.connect(lambda msg: QMessageBox.critical(self, "错误", msg))

        if path.isfile("upload"):
            self.is_upload = True
        else:
            self.is_upload = False

        # 初始化线程
        # 回放线程
        Thread(target=self.playbackThread, daemon=True).start()
        # 记录保存线程
        Thread(target=self.saveRecordThread, daemon=True).start()
        # 主检测线程
        Thread(target=self.mainThread, daemon=True).start()

        # 初始化UI
        self.setWindowTitle(title)

        # 设置多选框状态
        self.checkBoxCar.setChecked(True)
        self.checkBoxSmoke.setChecked(True)
        self.checkBoxSave.setChecked(True)
        self.checkBoxSave.setEnabled(False)

        # 初始化检测结果表
        self.record_model = QStandardItemModel(self.tableView)
        self.record_model.setColumnCount(3)
        self.record_model.setHorizontalHeaderLabels(self.__headLabels)
        self.tableView.setModel(self.record_model)
        self.tableView.selectionModel().currentRowChanged.connect(self.on_row_changed)
        self.tableView.doubleClicked.connect(self.on_row_doubleclicked)

        # 初始化历史记录表
        self.history_model = QStandardItemModel(self.tableHistory)
        self.history_model.setColumnCount(3)
        self.tableHistory.setModel(self.history_model)
        self.tableHistory.selectionModel().currentRowChanged.connect(self.on_row_changed)
        self.loadHistory()
        self.tableHistory.doubleClicked.connect(self.on_row_doubleclicked)
        # self.load_history()

        # 设置保存目录
        self.__save_path = path.abspath(self.__save_path)
        os.makedirs(self.__save_path, exist_ok=True)
        self.editSave.setText(path.abspath(self.__save_path))
        self.editSave.setReadOnly(True)
        self.btnSave.clicked.connect(lambda i: webbrowser.open(self.__save_path))

        self.labelMain.setScaledContents(True)
        self.labelImg1.setScaledContents(True)
        self.labelImg2.setScaledContents(True)
        self.labelBack.setScaledContents(True)

        # 自动开始、自动停止
        def timeout():
            if (
                self.checkBoxAutoStart.isChecked() and
                self.timeEditStart.time() <= QTime.currentTime() and
                self.realplay_stop is True
            ):
                self.btnStart.clicked.emit()

            if (
                self.checkBoxAutoStop.isChecked() and
                self.timeEditStop.time() <= QTime.currentTime() and
                self.realplay_stop is False
            ):
                self.btnStop.clicked.emit()

        self.timer = QTimer(self)
        self.timer.timeout.connect(timeout)
        self.timer.start(3000)

        # 设置林格曼初始阈值
        self.sliderLevel.setValue(1)

        # 设置初始模式为视频模式
        self.radioVideo.toggle()
        self.on_radioVideo_toggled(True)

    def playbackThread(self):
        """ 回放线程 当有回放队列中有数据时回放视频 """
        while True:
            video_path = self.__playback_queue.get()
            video = cv2.VideoCapture(video_path)
            interval = video.get(cv2.CAP_PROP_FPS) / 1000
            while self.__playback_queue.qsize() == 0:
                ret, frame = video.read()
                if not ret:
                    break
                img = cv2pixmap(frame)
                self.labelBack.setPixmap(img)
                sleep(interval)
            video.release()

    def saveRecordThread(self):
        """ 记录保存线程 当记录队列中有数据时保存队列中的数据 """
        while True:
            track, frames, fps, size = self.__record_queue.get()
            save_path = path.join(self.__save_path, track.id)
            # 创建保存目录
            os.makedirs(save_path, exist_ok=True)

            files = []
            # 保存图片
            try:
                for i, img in enumerate([track.plate_image, track.smoke_image]):
                    p = path.join(save_path, '.jpg'.format(i))
                    cv2.imwrite(p, img)
                    files.append(p)
            except:
                print("image error")
                tb.print_exc()
                return

            # 保存视频
            try:
                p = path.join(save_path, 'video.mp4')
                cmd = "ffmpeg -f rawvideo -pix_fmt bgr24 -an -s {width}*{height} -i - -r {fps} -b:v 4096k -bufsize 4096k -c:a avc -c:v h264 {file}".format(
                    fps=fps,
                    file=p,
                    width=size[0],
                    height=size[1]
                )
                sub = Popen(cmd, stdin=PIPE, shell=True)
                while frames:
                    sub.stdin.write(frames.pop(0))
                sub.stdin.close()
                sub.wait()
                files.append(p)
            except:
                print("video error")
                tb.print_exc()
                return

            # 转换格式 更新数据
            record = RecordData.fromTrackObject(track, self.__station_id, self.__station_name, self.sliderLevel.value(), *files)

            # 保存信息
            if not record.save(path.join(save_path, 'record.json')):
                print("record error")
                tb.print_exc()
                return

            self.addRecord(record)
            if self.is_upload:
                upload(record)
            self.__playback_queue.put(record.video_path)

    @property
    def realplay_stop(self):
        return self.__realplay_stop

    @realplay_stop.setter
    def realplay_stop(self, value):
        self.btnStart.setEnabled(value)
        self.btnStop.setEnabled(not value)
        self.__realplay_stop = value

    def mainThread(self):
        """ 主播放线程 """
        while True:
            video_source = self.__realplay_queue.get()
            self.loadHistory()

            # 读取授权码
            try:
                with open("auth_code", encoding="utf-8") as fp:
                    auth_code = fp.read().strip()
            except:
                self.signalVideoError.emit("授权文件读取失败, 请检查授权文件是否存在")
                continue

            try:
                sd = SmokeDetector(video_source, self.__border, auth_code=auth_code)
            except AssertionError as e:
                self.signalVideoError.emit(e.args[0])
                continue
            except:
                tb.print_exc()
                self.signalVideoError.emit("发生了未知的错误")
                continue

            draw_car = self.checkBoxCar.isChecked()
            draw_smoke = self.checkBoxSmoke.isChecked()
            save_record = self.checkBoxSave.isChecked()

            self.realplay_stop = False

            while self.realplay_stop is False:
                frame, tracks, save_list = sd.nextFrame()

                # 保存记录
                if save_record and save_list:
                    frames = sd.getSaveFrames()
                    for track in save_list:
                        if track.Ringelmann >= self.sliderLevel.value():
                            self.__record_queue.put((track, frames, sd.fps, sd.size))
                    del frames

                if frame is None:
                    break

                # 画出边框
                for track in tracks:
                    color = None
                    if draw_smoke and track.smoke_count >= 3:
                        color = (0, 0, 255)
                    elif draw_car:
                        color = (0, 255, 0)
                    if color:
                        rect = track.last_result.car_rect
                        cv2.rectangle(frame, *rect, color, 2)
                        bl = rect[0][0] + 5, rect[1][1] - 5
                        cv2.putText(frame, str(track.last_result.is_car), bl, cv2.FONT_HERSHEY_COMPLEX, 2, color, 2)

                # 显示图片
                self.labelMain.setPixmap(cv2pixmap(frame))

            del sd
            self.realplay_stop = True

    def showRecord(self, record: RecordData):
        """ 显示记录 """
        # 记录图片
        self.labelImg1.setPixmap(QPixmap(record.img_plate_path))
        self.labelImg2.setPixmap(QPixmap(record.img_smoke_path))

        # 记录信息
        self.labelSId.setText(record.st_name)
        self.labelId.setText(record.id)
        self.labelTime.setText(str(record.check_time))
        self.labelLine.setText(str(record.car_lane))
        self.labelRingelmann.setText(str(record.Ringelmann))
        self.labelPlate.setText(record.plate)
        self.labelPColor.setText(record.plate_color)
        self.labelCarType.setText(record.car_type)
        self.labelCarColor.setText(record.car_color)

    def addRecord(self, record: RecordData):
        """ 添加记录 """
        item = QStandardItem(str(record.check_time))
        item.setData(record)

        self.record_model.appendRow([
            item,
            QStandardItem(record.plate),
            QStandardItem(str(record.Ringelmann))
        ])

        new_row = self.record_model.index(self.record_model.rowCount()-1, 0)
        old_row = self.tableView.currentIndex()
        self.tableView.selectionModel().currentRowChanged.emit(new_row, old_row)

    def addHistoryRecord(self, record: RecordData):
        """ 添加历史记录 """
        item = QStandardItem(str(record.check_time))
        item.setData(record)

        self.history_model.appendRow([
            item,
            QStandardItem(record.id),
            QStandardItem("已上传")
        ])

    @pyqtSlot()
    def on_btnStart_clicked(self):
        """ 开始按钮被点击 """
        if self.radioVideo.isChecked():
            self.__realplay_queue.put(self.editPath.text())
        else:
            video_source = "||".join([i.text() for i in (self.editUser, self.editPwd, self.editIP, self.editPort, self.editChannel, "0")])
            self.__realplay_queue.put(video_source)

    @pyqtSlot()
    def on_btnStop_clicked(self):
        """ 停止按钮被点击 """
        self.__realplay_stop = True

    def on_row_changed(self, new_row, old_row):
        """ 列表选中项被改变 """
        self.showRecord(new_row.model().item(new_row.row()).data())

    def on_row_doubleclicked(self, row):
        """ 列表项被双击 """
        reocrd = row.model().item(row.row()).data()
        self.__playback_queue.put(reocrd.video_path)

    def loadHistory(self):
        """ 加载历史记录 """
        self.record_model.clear()
        self.record_model.setHorizontalHeaderLabels(self.__headLabels)

        self.history_model.clear()
        self.history_model.setHorizontalHeaderLabels(self.__history)

        if not path.isdir(self.__save_path):
            return

        dl = os.listdir(self.__save_path)
        dl.sort(reverse=True)

        for d in dl:
            fn = path.join(self.__save_path, d, "record.json")
            if path.isfile(fn):
                record = RecordData.load(fn)
                self.addHistoryRecord(record)

    @pyqtSlot(bool)
    def on_radioVideo_toggled(self, value):
        """ 切换播放模式 """
        video_group = [self.editPath, self.btnOpen]
        stream_group = [self.editIP, self.editPort, self.editChannel, self.editUser, self.editPwd]

        [i.setEnabled(value) for i in video_group]
        [i.setEnabled(not value) for i in stream_group]

    @pyqtSlot()
    def on_btnBorder_clicked(self):
        """ 设置车道边界 """
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

        self.__border = getBorder(self, video_source, self.__border) or self.__border

    @pyqtSlot()
    def on_btnOpen_clicked(self):
        """ 选择视频文件 """
        files = QFileDialog.getOpenFileName(self, "选择视频文件", None, "视频文件(*.mp4 *.avi)\n所有文件(*.*)")
        if files[0]:
            self.editPath.setText(files[0])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlg = SmokeDialog()
    dlg.show()
    app.exec_()
