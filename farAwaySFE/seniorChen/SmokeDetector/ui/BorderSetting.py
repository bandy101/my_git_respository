# coding: utf-8
import sys
from copy import deepcopy

import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from .ui_border_setting import Ui_Dialog


class BorderSetting(QDialog, Ui_Dialog):

    def __init__(self, img_path, parent=None, border=None):
        super().__init__(parent)
        self.setupUi(self)

        # 设置图片点击事件
        self.label_image.mousePressEvent = self.on_label_image_mousePressEvent

        # 计算图片缩放 设置图片
        img = QPixmap(img_path)
        w_scale = self.label_image.width() / (img.width() or 1)
        h_scale = self.label_image.height() / (img.height() or 1)
        scale = min((w_scale, h_scale))
        w, h = int(img.width() * scale), int(img.height() * scale)
        img = img.scaled(w, h, Qt.KeepAspectRatio)
        self.label_image.setPixmap(img)

        self.__image_size = np.array([img.width(), img.height()])

        # 初始化鼠标图形
        self.__setCursor(False)

        # 设置初始化边界
        self.__border_type = None
        if border:
            self.border_up, self.border_down = deepcopy(border)
        else:
            self.border_up = []
            self.border_down = []

        self.updateBorderUp()
        self.updateBorderDown()

    def __setCursor(self, cross=True):
        cursor = Qt.CrossCursor if cross else Qt.ArrowCursor
        # self.setCursor(cursor)
        self.label_image.setCursor(cursor)
        self.__cross_cursor = cross

    def updateBorderUp(self):
        self.label_border_up.setText(f'上边界({len(self.border_up)})')
        self.edit_up.setText(str(self.border_up))

    def updateBorderDown(self):
        self.label_border_down.setText(f'上边界({len(self.border_down)})')
        self.edit_down.setText(str(self.border_down))

    @pyqtSlot()
    def on_btn_up_add_clicked(self):
        self.__setCursor(True)
        self.__border_type = 'up'

    @pyqtSlot()
    def on_btn_down_add_clicked(self):
        self.__setCursor(True)
        self.__border_type = 'down'

    @pyqtSlot()
    def on_btn_up_del_clicked(self):
        if len(self.border_up) > 0:
            self.border_up.pop()
            self.updateBorderUp()

    @pyqtSlot()
    def on_btn_down_del_clicked(self):
        if len(self.border_down) > 0:
            self.border_down.pop()
            self.updateBorderDown()

    @pyqtSlot(QMouseEvent)
    def on_label_image_mousePressEvent(self, event: QMouseEvent):
        if self.__cross_cursor is False or event.button() == Qt.MiddleButton:
            return

        if event.button() == Qt.LeftButton:
            point = event.x(), event.y()
            if self.__border_type == 'up':
                border = self.border_up
                update = self.updateBorderUp
            else:
                border = self.border_down
                update = self.updateBorderDown

            border.append(list(map(lambda x: round(x, 2), point / self.__image_size * 100)))
            update()
        self.__setCursor(False)

    def accept(self):
        if len(self.border_up) != len(self.border_down):
            QMessageBox.critical(self, '错误', '上下边界成员个数必须相同')
        else:
            QDialog.accept(self)


def getBorder(parent, video_source, default_border):
    ''' 获取上下边界
    出错或未修改时返回`None` 其他情况返回边界数组
    '''
    import tempfile
    import os
    import cv2
    from SFE.Video import VideoReader

    # 打开视频
    vr = VideoReader()
    if video_source.count('||') == 4:
        user, pwd, ip, port, channel = video_source.split('||')
        port, channel = int(port), int(channel)
        vr.openStream(user, pwd, ip, port, channel)
    else:
        vr.openVideo(video_source)
    if not vr.is_opened:
        QMessageBox.warning(parent, '警告', '请确认视频源输入正确')
        return

    # 保存截图
    ret, img = vr.read()
    del vr
    if not ret:
        QMessageBox.critical(parent, '错误', '视频读取失败')
        return
    fd, fn = tempfile.mkstemp(suffix='.jpg')
    with open(fd, 'wb') as fp:
        fp.write(cv2.imencode('.jpg', img)[1])

    # 打开设置窗口
    dlg = BorderSetting(fn, parent, default_border)
    if dlg.exec_():
        return dlg.border_up, dlg.border_down

    os.remove(fn)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dlg = BorderSetting('E:/Desktop/bg/1.jpg')
    dlg.show()
    app.exec_()
    print(dlg.border_up, dlg.border_down)
