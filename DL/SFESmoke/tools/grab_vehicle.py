import os
from os import path
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

import cv2

from SFE.SmokeDetector import SmokeDetector, TrackObject


OUTPUT_DIR = "./output"


def __getOnDelCallback(save_path, prefix, pool: ThreadPoolExecutor):
    if prefix:
        prefix = f"{prefix}_"
    else:
        prefix = ""

    os.makedirs(save_path, exist_ok=True)

    def on_del(track: TrackObject):
        # Vehicle
        idx = int(len(track.list) / 2)
        fr = track.list[idx]

        img = fr.car_img
        car_type = fr.is_car

        fn = f"{prefix}{track.id}_{car_type}.jpg"
        sd = path.join(save_path, str(car_type))
        os.makedirs(sd, exist_ok=True)
        pool.submit(cv2.imwrite, path.join(sd, fn), img)

    return on_del


def grab(video_path):
    """
    检测视频中的所有车辆并按照分类保存到指定文件夹`output`目录
    - video_path: 视频目录
    """
    from auth import getAuthCode

    video_path = path.abspath(video_path)
    sm = SmokeDetector(video_path, auth_code=getAuthCode())

    dn, fn = path.split(video_path)
    dn = path.basename(dn)
    fn = path.splitext(fn)[0]
    prefix = f"{dn}_{fn}"

    pool = ThreadPoolExecutor()

    setattr(TrackObject, "__del__", __getOnDelCallback(OUTPUT_DIR, prefix, pool))

    while sm.nextFrame()[0] is not None:
        pass

    del sm
    pool.shutdown()
    print(video_path, "done")


def grabAll(video_path):
    """ 
    遍历指定目录中的所有视频(avi、mp4), 并把视频中的所有车辆按照分类
    保存到指定文件夹`output`目录
    - video_path: 视频目录
    """
    pool = ProcessPoolExecutor()
    for p, _, fl in os.walk(video_path):
        for f in fl:
            if f[-4:].lower() in [".avi", ".mp4"]:
                pool.submit(grab, path.join(p, f))
    pool.shutdown()


if __name__ == "__main__":
    from fire import Fire
    Fire({
        "grab": grab,
        "grabAll": grabAll
    })
