# coding: utf-8
from subprocess import Popen, PIPE, STDOUT
import os

import cv2


class RTMP:

    def __init__(self, id, fps, in_size, out_size=None, bitrate=4096, host=None):
        """ 启动RTMP推送流
        - id str: 推送地址ID
        - fps int: 帧率
        - in_size tuple: (width, height) 输入图片的大小
        - out_size tuple: (width, height) 输出图片的大小, 为`None`时与`in_size`相同
        - bitrate int: 码率 单位为k
        - host str[None]: 推送地址 默认为`127.0.0.1`
        """
        # 输入为从PIPE输入图片数据 无音频
        # 输出 FPS=fps 默认帧大小等于输入图片大小 格式为flv 码率为4M 输出到rtmp://127.0.0.1/live/id
        if out_size is None:
            out_size = in_size

        if not host:
            host = "127.0.0.1"

        cmd = "ffmpeg -re -f rawvideo -s {in_width}*{in_height} -pix_fmt bgr24 -an -i - -s {out_width}*{out_height} -r {fps} -b:v {bitrate}k -f flv rtmp://{host}/live/{id}".format(
            fps=fps,
            bitrate=bitrate,
            id=id,
            in_width=in_size[0],
            in_height=in_size[1],
            out_width=out_size[0],
            out_height=out_size[1],
            host=host
        )
        self.ffmpeg = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT, shell=True)

    def stop(self):
        self.ffmpeg.stdin.close()
        self.ffmpeg.terminate()

    def __del__(self):
        self.stop()

    def write(self, frame):
        try:
            self.ffmpeg.stdin.write(frame)
            self.ffmpeg.stdin.flush()
            return True
        except:
            return self.ffmpeg.stdout.read()


if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    rtmp = RTMP('test', fps, (width, height))

    try:
        while True:
            ret, frame = cap.read()
            if ret:
                rtmp.write(frame)
            else:
                break
    finally:
        del rtmp
