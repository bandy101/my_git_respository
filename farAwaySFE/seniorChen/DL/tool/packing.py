# uncompyle6 version 3.2.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: .\tools\packing.py
# Compiled at: 2018-11-02 11:51:23
# Size of source mod 2**32: 1466 bytes
import tarfile, os
from os import path
from concurrent.futures import ProcessPoolExecutor

def save(fn, args):
    with tarfile.open(fn, 'w:gz') as (tar):
        for srcname, arcname in args:
            tar.add(srcname, arcname)


def main(src, dest='./result', count=100):
    """ ���ָ��Ŀ¼�¸���վ�����Ƶ
    - src str: վ�㱣��Ŀ¼
    - dest str["./result"]: ����ļ�����Ŀ¼
    - count int[100]: ÿ��վ����ౣ�����Ƶ��
    """
    if not path.isdir(src):
        raise AssertionError('վ��Ŀ¼������')
    os.makedirs(dest, exist_ok=True)
    pool = ProcessPoolExecutor()
    for station_id in os.listdir(src):
        record_dir = path.join(src, station_id, 'record')
        if not path.isdir(record_dir):
            continue
        record_list = os.listdir(record_dir)
        if len(record_list) > count:
            i = len(record_list) // count
            record_list = [v for k, v in enumerate(record_list) if k % i == 0][:count]
        save_name = path.join(dest, station_id + '.tgz')
        save_args = []
        for record in record_list:
            srcname = path.join(record_dir, record, 'video.mp4')
            arcname = path.join(station_id, record + '.mp4')
            save_args.append((srcname, arcname))

        if len(save_args) == 0:
            continue
        pool.submit(save, save_name, save_args)

    pool.shutdown()


if __name__ == '__main__':
    from fire import Fire
    Fire(main)
# okay decompiling tool\packing.pyc
