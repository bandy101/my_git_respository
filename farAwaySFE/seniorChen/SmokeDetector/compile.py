import sys
from compileall import py_compile
import os
from os import path
from glob import glob
import shutil


def copy(path_list, dest_dir, is_dest_base=False):
    ''' 将文件复制到指定文件夹
    - *path_list*: 要复制的文件列表 需要为相对路劲
    - *dest_dir*: 要保存的目录
    - *is_dest_base*: 是否保存到保存目录根部, 为`False`时按照`path`的目录结构复制, 如`1/2/3`将复制到`dest_dir/1/2/3`
    '''
    for src in path_list:
        if is_dest_base:
            dst = path.join(dest_dir, path.basename(src))
        else:
            dst = path.join(dest_dir, src)

        if path.isdir(src):
            print(f"copy directory {src} to {dst}")
            shutil.copytree(src, dst)
        else:
            print(f"copy file {src} to {dst}")
            dst_dir = path.split(dst)[0]
            os.makedirs(dst_dir, exist_ok=True)
            shutil.copy(src, dst)


type_list = ('win', 'linux')
dest_list = [f'dest_{i}' for i in type_list]

for dest_type, dest_dir in zip(type_list, dest_list):
    # 清除目标目录
    if path.exists(dest_dir):
        shutil.rmtree(dest_dir)

    # 编译Python文件 ----------------------------------------------------
    for p, ds, fs in os.walk("."):
        # 删除缓存目录
        if '__pycache__' in ds:
            shutil.rmtree(path.join(p, '__pycache__'))
        # 跳过 . 开头的文件夹和thirdparty、资源目录目录
        if ((p != "." and path.basename(p).startswith(".")) or
                "thirdparty" in p or
                'resource' in p):
            continue
        # 编译文件
        ddir = path.join(dest_dir, p)
        for f in fs:
            if not f.endswith(".py") or f == "compile.py":
                continue
            s = path.join(p, f)
            d = path.join(ddir, f + "c")

            print(f"compile {s} to {d}")
            py_compile.compile(s, d, doraise=True)

    # 复制文件、目录 保持目录结构 -------------------------------------------
    # 模型文件
    copy_list = glob('resource/*.h5')

    # 第三方包
    if dest_type == 'win':
        copy_list += glob('SFE/thirdparty/*.pyd')
    elif dest_type == 'linux':
        copy_list += ["SFE/thirdparty"]

    # 实施复制
    copy(copy_list, dest_dir)

    # 复制文件、目录到根目录 -------------------------------------------------
    # 运行库
    copy_list = []
    if dest_type == 'win':
        copy_list += glob("SFE/thirdparty/VideoStream/*.dll")    # 海康
        copy_list += ['SFE/thirdparty/EasyPR/thplateid/TH_PLATEID.dll']   # 车牌识别
        copy_list += glob('SFE/thirdparty/opencv/*')                 # OpenCV
    elif dest_type == 'linux':
        copy_list += glob("SFE/thirdparty/VideoStream/*.so")     # 海康
    copy_list += ["SFE/thirdparty/VideoStream/HCNetSDKCom"]  # 海康

    # 车牌识别模型
    copy_list += ["SFE/thirdparty/EasyPR/model"]

    # 主程序配置目录
    # copy_list += ["configure"]

    # 实施复制
    copy(copy_list, dest_dir, True)

    # 清除无用文件 -------------------------------------------------------------
    del_list = []
    del_list += glob(f'{dest_dir}/HCNetSDKCom/*.lib')
    if dest_type == 'win':
        del_list += glob(f'{dest_dir}/HCNetSDKCom/*.so')
    elif dest_type == 'linux':
        del_list += glob(f'{dest_dir}/HCNetSDKCom/*.dll')
        del_list += glob(f'{dest_dir}/SFE/thirdparty/*.pyd')
        del_list += glob(f'{dest_dir}/SFE/thirdparty/VideoStream/*.lib')
        del_list += glob(f'{dest_dir}/SFE/thirdparty/VideoStream/HCNetSDKCom/*.dll')
        del_list += glob(f'{dest_dir}/SFE/thirdparty/VideoStream/HCNetSDKCom/*.lib')
        del_list += glob(f'{dest_dir}/SFE/thirdparty/VideoStream/HCNetSDKCom/*.dll')
        del_list.append(f'{dest_dir}/SFE/thirdparty/opencv')

    for f in del_list:
        print(f'clean file {f}')
        if path.isfile(f):
            os.remove(f)
        elif path.isdir(f):
            shutil.rmtree(f)

    print(f"done {dest_type}")
