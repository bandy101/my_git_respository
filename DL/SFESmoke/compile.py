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
            print("copy directory {} to {}".format(src, dst))
            shutil.copytree(src, dst)
        elif path.exists(src):
            print("copy file {} to {}".format(src, dst))
            dst_dir = path.split(dst)[0]
            os.makedirs(dst_dir, exist_ok=True)
            shutil.copy(src, dst)
        else:
            print("不存在", src)


type_list = ['win', 'linux']
dest_list = ["release/dest_{}".format(i) for i in type_list]

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
        if (
                (p != "." and path.basename(p).startswith(".")) or
                "thirdparty" in p or
                'resource' in p or
                "release" in p
        ):
            continue

        # 编译文件
        ddir = path.join(dest_dir, p)
        for f in fs:
            if not f.endswith(".py") or f == "compile.py":
                continue

            s = path.join(p, f)
            d = path.join(ddir, f + "c")

            print("compile {} to {}".format(s, d))
            py_compile.compile(s, d, doraise=True)

    src = path.join("SFE", "thirdparty", "__init__.py")
    dst = path.join(dest_dir, src + "c")
    py_compile.compile(src, dst, doraise=True)

    # 复制资源文件 --------------------------------------------------------
    copy_list = glob('SFE/resource/*.h5')
    copy_list.append("server/config")
    copy_list.append("server/server.json")
    copy_list.append("server/DBModel/db_uri")
    copy_list.append("server/web_static")
    copy(copy_list, dest_dir)

    # 第三方包 ------------------------------------------------------------
    thirdparty_base_dir = path.join("SFE", "thirdparty")
    thirdparty_dir = path.join(thirdparty_base_dir, dest_type)
    copy_list = [path.join(thirdparty_dir, i) for i in os.listdir(thirdparty_dir)]
    copy(copy_list, path.join(dest_dir, thirdparty_base_dir), True)

    if dest_type == "linux":
        # 海康库
        copy_list = glob(path.join(thirdparty_dir, "VideoStream", "*.so"))
        copy_list += glob(path.join(thirdparty_dir, "VideoStream", "HCNetSDKCom", "*.so"))
        copy_list.append(path.join(thirdparty_dir, "Thplateid", "thplateid", "libthplateid.so"))
        copy(copy_list, path.join(dest_dir, thirdparty_base_dir, "lib"), True)

    print("done {}".format(dest_type))
