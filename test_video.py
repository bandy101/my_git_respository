# coding: utf-8
from argparse import ArgumentParser
import os
from os import path
import shutil
from datetime import datetime
import tarfile
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from time import sleep

import cv2

from SFE.SmokeDetector import TrackObject, SmokeDetector


def packResult(pack_dir, save_dir='/FTP/result'):
    if not path.exists(pack_dir):
        return
    sd = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sd = path.join(save_dir, sd)

    for dn in os.listdir(pack_dir):
        os.makedirs(path.join(sd, dn), exist_ok=True)
        for pd in os.listdir(path.join(pack_dir, dn)):
            fn = path.join(sd, dn, pd + '.tar.gz')
            pp = path.join(pack_dir, dn, pd)

            with tarfile.open(fn, 'w:gz') as tar:
                tar.add(pp, pd)


def run(video: str, save_dir: str, prefix: str, save_car: bool, save_smoke: bool):
    '''
    - *video*: 视频所在路径
    - *save_dir*: 文件保存目录
    - *prefix*: 保存文件前缀
    - *save_car*: 是否保存车辆图片
    - *save_smoke*: 是否保存黑烟图片
    '''

    pool = ThreadPoolExecutor()

    # 定义保存函数
    def save(self: TrackObject):
        count = len(self.list)
        if count <= 5:
            save_list = self.list
        else:
            center = int(count/2)
            idx = [0, center-1, center, center+1, count-1]
            save_list = [v for i, v in enumerate(self.list) if i in idx]

        for idx, result in enumerate(save_list):
            fn = "{prefix}{id}_{idx}.jpg".format(prefix=prefix + "_" if prefix else "", id=self.id, idx=idx)
            if save_car: 
                fd = path.join(save_dir, 'car', str(result.is_car))
                os.makedirs(fd, exist_ok=True) #=false 如果exit 会抛出错误
                fp = path.join(fd, fn)
                try:
                    pool.submit(cv2.imwrite, fp, result.car_img)
                except:
                    pass
            if save_smoke and result.is_car:
                fd = path.join(save_dir, 'smoke', str(bool(result.is_smoke)))
                os.makedirs(fd, exist_ok=True)
                fn = fn[:-4]
                try:
                    for name, img in zip(["src", "left", "right", "bottom"], result.smoke_img):
                        fp = path.join(fd, f"{fn}_{name}.jpg")
                        pool.submit(cv2.imwrite, fp, img)
                except:
                    pass

    setattr(TrackObject, '__del__', save)

    # 打开视频
    sm = SmokeDetector(video, fix=False, only_car=False)
    while True:
        frame, tracks, save_list = sm.nextFrame()
        if frame is None:
            break
    del sm

    sleep(1)
    pool.shutdown()
    print(video, 'done')


def main(test_src, save_dir='./result', clean=True, save_car=True, save_smoke=True, pack=False, pack_dir='/FTP/result'):
    ''' 测试指定视频文件
    - test_src str/tuple: 视频源
    - save_dir str[./result]: 检测结果保存目录
    - clean bool[True]: 是否先清空保存目录
    - save_car bool[True]: 保存车辆图片
    - save_smoke bool[True]: 保存黑烟图片
    - pack bool[False]: 是否打包检测结果
    - pack_dir str[/FTP/result]: 打包文件保存路径
    '''

    # 清除保存目录
    if clean and path.isdir(save_dir):
        shutil.rmtree(save_dir)

    pool = ProcessPoolExecutor(min(4, os.cpu_count()))

    # 检测文件
    def run_file(src):
        src = path.abspath(src)
        src_path, src_file = path.split(src)
        prefix = "{}_{}".format(path.basename(src_path), path.splitext(src_file)[0])
        #prefix =/data/video/ video_video_to1_4_2
        pool.submit(run, src, save_dir, prefix, save_car, save_smoke)
    
    # 检测视频流
    def run_stream(src):
        if src.count('||') != 4:
            print(src, '格式不正确')
            return

        user, pwd, ip, port, channel = src.split('||')
        prefix = "{}_{}".format(ip, channel)

        pool.submit(run, src, save_dir, prefix, save_car, save_smoke)

    if isinstance(test_src, str):
        test_src = [test_src]

    for src in test_src:
        if path.isdir(src):
            for p, ds, fs in os.walk(src):
                videos = [i for i in fs if i[-4:].lower() in ('.mp4', '.avi')]
                for video in videos:
                    video = path.join(p, video)
                    run_file(video)
        elif path.isfile(src):
            run_file(src)
        else:
            run_stream(src)

    pool.shutdown()
    if pack:
        print('正在打包...')
        packResult(save_dir, pack_dir)
    print('检测完成')


if __name__ == '__main__':
    from fire import Fire
    Fire(main)
