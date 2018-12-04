import sys
import os
from os import path
import shutil
import fire

__site_packages = [i for i in sys.path if i.endswith("site-packages") or i.endswith("dist-packages")][0]
__install_path = path.join(__site_packages, "SFE")
__LIB_PATH = "/usr/lib"


def install():
    uninstall(False)
    shutil.copytree("SFE", __install_path)
    if sys.platform != "win32":
        os.system("cp -u SFE/thirdparty/lib/* {}".format(__LIB_PATH))

    print(__install_path)


def uninstall(rmlib=True):
    try:
        import SFE
        base = path.dirname(path.abspath(SFE.__file__))
        if base == path.dirname(path.abspath(__file__)):
            return
        if sys.platform != "win32" and rmlib:
            rm = "rm -f {}".format(" ".join([path.join(__LIB_PATH, i) for i in os.listdir(path.join(base, "thirdparty", "lib"))]))
            os.system(rm)
        shutil.rmtree(base)
    except:
        pass


fire.Fire({
    "install": install,
    "uninstall": uninstall,
})
