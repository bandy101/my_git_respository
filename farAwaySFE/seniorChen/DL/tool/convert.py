# uncompyle6 version 3.2.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: .\tools\convert.py
# Compiled at: 2018-11-02 11:51:23
# Size of source mod 2**32: 3516 bytes
import os
from os import path
import shutil
from threading import Thread
from queue import Queue
from time import sleep
import tarfile, numpy as np, cv2

def convert():
    while 1:
        is_np = False
        src, dest, flag, flip = queue.get()
        image = cv2.imread(src, flag)
        if image is None:
            image = cv2.imdecode(np.fromfile(src, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
            if image is None:
                print(src)
                continue
                if flag == cv2.IMREAD_GRAYSCALE:
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                is_np = True
            image = cv2.resize(image, size)
            if is_np:
                cv2.imencode('.jpg', image)[1].tofile(dest)
            else:
                cv2.imwrite(dest, image)
            if flip:
                image = cv2.flip(image, 1)
                p, fn = path.split(dest)
                dest = path.join(p, 'f_' + fn)
                if is_np:
                    cv2.imencode('.jpg', image)[1].tofile(dest)
                else:
                    cv2.imwrite(dest, image)


queue = Queue()
for i in range(20):
    (Thread(target=convert, daemon=True)).start()

def getSrcPath():
    while 1:
        src_path = input('������Ҫ��������ԴĿ¼:')
        if not path.isdir(src_path):
            print('Ŀ¼������, ����������')
            continue
        return path.abspath(src_path)


def getDsetPath(dest_path='./dest'):
    dest_path = input('���������ݱ���Ŀ¼(Ĭ��Ϊ ./dest):') or dest_path
    if path.isdir(dest_path):
        shutil.rmtree(dest_path)
    return path.abspath(dest_path)


def getSize(size='128*128'):
    while True:
        size = input('���������ݵ������С(��ʽΪwidth*height, Ĭ��Ϊ128*128):') or size
        try:
            size = map(int, size.split('*'))
            return tuple(size)
        except:
            print('�������ݸ�ʽ����, ����������')


def isGray():
    v = input('��ȷ�����ͼƬ�Ƿ�Ϊ�Ҷ�ͼ, Ĭ��Ϊ��, ����Ϊ��:')
    return v != ''


def isFlip():
    v = input('�Ƿ�����ˮƽ��ת��ͼƬ?Ĭ��Ϊ��, ����Ϊ��:')
    return v != ''


try:
    while True:
        src_path = getSrcPath()
        dest_path = getDsetPath()
        size = getSize()
        is_gray = isGray()
        is_gray = cv2.IMREAD_GRAYSCALE if is_gray else cv2.IMREAD_COLOR
        is_flip = isFlip()
        for p, dir_list, file_list in os.walk(src_path):
            print(('������� {} �е��ļ�...').format(p))
            dest_dir = p.replace(src_path, dest_path)
            for dir_name in dir_list:
                os.makedirs(path.join(dest_dir, dir_name), exist_ok=True)

            fn_fmt = ('>0{}').format(len(str(len(file_list))))
            for idx, fn in enumerate(file_list):
                src = path.join(p, fn)
                ext = path.splitext(fn)[1]
                dest = path.join(dest_dir, ('{idx:{fn_fmt}}{ext}').format(idx=idx, fn_fmt=fn_fmt, ext=ext))
                queue.put((src, dest, is_gray, is_flip))

        while not queue.empty():
            print(('ʣ���ļ���: {:<10}').format(queue.qsize()), end='\r')
            sleep(0.1)

        print('�������, ����ѹ���ļ�...')
        with tarfile.open(('{}.tar.gz').format(dest_path), 'w:gz') as (tar):
            tar.add(dest_path, path.split(dest_path)[1])
        print('ѹ�����')
        print('-' * 100)

except (KeyboardInterrupt, EOFError):
    pass
# okay decompiling tool\convert.pyc
