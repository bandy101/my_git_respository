# uncompyle6 version 3.2.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: .\tools\test_video.py
# Compiled at: 2018-11-02 11:51:23
# Size of source mod 2**32: 4321 bytes
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
from auth import getAuthCode

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
            with tarfile.open(fn, 'w:gz') as (tar):
                tar.add(pp, pd)


def run(video, save_dir, prefix, save_car, save_smoke):
    """
    - *video*: ��Ƶ����·��
    - *save_dir*: �ļ�����Ŀ¼
    - *prefix*: �����ļ�ǰ׺
    - *save_car*: �Ƿ񱣴泵��ͼƬ
    - *save_smoke*: �Ƿ񱣴����ͼƬ
    """
    pool = ThreadPoolExecutor()

    def save(self):
        save_list = [i for i in self.list if i.is_smoke]
        for idx, result in enumerate(save_list):
            fn = ('{prefix}{id}_{idx}.jpg').format(prefix=prefix + '_' if prefix else '', id=self.id, idx=idx)
            if save_car:
                fd = path.join(save_dir, 'car', str(result.is_car))
                os.makedirs(fd, exist_ok=True)
                fp = path.join(fd, fn)
                try:
                    pool.submit(cv2.imwrite, fp, result.car_img)
                except:
                    pass

                if save_smoke:
                    if result.is_car:
                        fd = path.join(save_dir, 'smoke')
                        os.makedirs(fd, exist_ok=True)
                        fp = path.join(fd, fn)
                        try:
                            pool.submit(cv2.imwrite, fp, result.smoke_img)
                        except:
                            pass

    setattr(TrackObject, '__del__', save)
    sm = SmokeDetector(video, fix=False, only_car=False, auth_code=getAuthCode())
    while 1:
        frame, tracks, save_list = sm.nextFrame()
        if frame is None:
            break

    del sm
    sleep(1)
    pool.shutdown()
    print(video, 'done')


def main(test_src, save_dir='./result', clean=True, save_car=True, save_smoke=True, pack=False, pack_dir='/FTP/result'):
    """ ����ָ����Ƶ�ļ�
    - test_src str/tuple: ��ƵԴ
    - save_dir str[./result]: ���������Ŀ¼
    - clean bool[True]: �Ƿ�����ձ���Ŀ¼
    - save_car bool[True]: ���泵��ͼƬ
    - save_smoke bool[True]: �������ͼƬ
    - pack bool[False]: �Ƿ��������
    - pack_dir str[/FTP/result]: ����ļ�����·��
    """
    if clean:
        if path.isdir(save_dir):
            shutil.rmtree(save_dir)
    pool = ProcessPoolExecutor(min(4, os.cpu_count()))

    def run_file(src):
        src = path.abspath(src)
        src_path, src_file = path.split(src)
        prefix = ('{}_{}').format(path.basename(src_path), path.splitext(src_file)[0])
        pool.submit(run, src, save_dir, prefix, save_car, save_smoke)

    def run_stream(src):
        if src.count('||') != 4:
            print(src, '��ʽ����ȷ')
            return
        user, pwd, ip, port, channel = src.split('||')
        prefix = ('{}_{}').format(ip, channel)
        pool.submit(run, src, save_dir, prefix, save_car, save_smoke)

    if isinstance(test_src, str):
        test_src = [
         test_src]
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
        print('���ڴ��...')
        packResult(save_dir, pack_dir)
    print('������')


if __name__ == '__main__':
    from fire import Fire
    Fire(main)
# okay decompiling tool\test_video.pyc
