# uncompyle6 version 3.2.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: .\SFE\__main__.py
# Compiled at: 2018-11-02 11:51:19
# Size of source mod 2**32: 896 bytes
import sys, os
from os import path
import shutil, fire
__site_packages = [i for i in sys.path if i.endswith('site-packages') or i.endswith('dist-packages')][0]
__install_path = path.join(__site_packages, 'SFE')
__LIB_PATH = '/usr/lib'

def install():
    uninstall(False)
    shutil.copytree('SFE', __install_path)
    if sys.platform != 'win32':
        os.system(('cp -u SFE/thirdparty/lib/* {}').format(__LIB_PATH))
    print(__install_path)


def uninstall(rmlib=True):
    try:
        import SFE
        base = path.dirname(path.abspath(SFE.__file__))
        if sys.platform != 'win32':
            if rmlib:
                rm = ('rm -f {}').format((' ').join([path.join(__LIB_PATH, i) for i in os.listdir(path.join(base, 'thirdparty', 'lib'))]))
                os.system(rm)
        shutil.rmtree(base)
    except:
        pass


fire.Fire({'install':install, 
 'uninstall':uninstall})
# okay decompiling SFE\__main__.pyc
