# uncompyle6 version 3.2.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: .\tools\grab_vehicle.py
# Compiled at: 2018-11-02 11:51:23
# Size of source mod 2**32: 1541 bytes
import os
from os import path
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import cv2
from SFE.SmokeDetector import SmokeDetector, TrackObject
OUTPUT_DIR = './output'

def getOnDelCallback(save_path, prefix, pool):
    if prefix:
        prefix = f'''{prefix}_'''
    else:
        prefix = ''
    os.makedirs(save_path, exist_ok=True)

    def on_del(track):
        idx = int(len(track.list) / 2)
        fr = track.list[idx]
        img = fr.car_img
        car_type = fr.is_car
        fn = f'''{prefix}{(track.id)}_{car_type}.jpg'''
        pool.submit(cv2.imwrite, path.join(save_path, fn), img)

    return on_del


def grab(video_path):
    from auth import getAuthCode
    video_path = path.abspath(video_path)
    sm = SmokeDetector(video_path, auth_code=getAuthCode())
    dn, fn = path.split(video_path)
    dn = path.basename(dn)
    fn = path.splitext(fn)[0]
    prefix = f'''{dn}_{fn}'''
    pool = ThreadPoolExecutor()
    setattr(TrackObject, '__del__', getOnDelCallback(OUTPUT_DIR, prefix, pool))
    while sm.nextFrame()[0] is not None:
        pass

    del sm
    pool.shutdown()
    print(video_path, 'done')


def main(video_path):
    pool = ProcessPoolExecutor()
    for p, dl, fl in os.walk(video_path):
        for f in fl:
            if f[-4:].lower() in ('.avi', '.mp4'):
                pool.submit(grab, path.join(p, f))

    pool.shutdown()


if __name__ == '__main__':
    from fire import Fire
    Fire(main)
# okay decompiling tool\grab_vehicle.pyc
